from datetime import datetime
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pendulum
import pypika
from pypika import AliasedQuery
from pypika import analytics as an
from pypika import Case
from pypika import Database
from pypika import Field
from pypika import NULL
from pypika import Query
from pypika import Table
from pypika.functions import Cast
from pypika.terms import LiteralValue
from pypika.terms import Term

from tecton_core import conf
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_core.offline_store import get_offline_store_partition_params
from tecton_core.offline_store import PartitionType
from tecton_core.offline_store import TIME_PARTITION
from tecton_core.offline_store import timestamp_to_partition_date_str
from tecton_core.offline_store import timestamp_to_partition_epoch
from tecton_core.pipeline_sql_builder import PipelineSqlBuilder
from tecton_core.query.aggregation_plans import AGGREGATION_PLANS
from tecton_core.query.aggregation_plans import QueryWindowSpec
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.sql_compat import convert_epoch_seconds_to_feature_store_format_version
from tecton_core.query.sql_compat import convert_epoch_term_in_seconds
from tecton_core.query.sql_compat import CustomQuery
from tecton_core.query.sql_compat import date_add
from tecton_core.query.sql_compat import default_case
from tecton_core.query.sql_compat import from_unixtime
from tecton_core.query.sql_compat import LastValue
from tecton_core.query.sql_compat import Query
from tecton_core.query.sql_compat import struct
from tecton_core.query.sql_compat import struct_extract
from tecton_core.query.sql_compat import to_timestamp
from tecton_core.query.sql_compat import to_unixtime
from tecton_core.query_consts import ANCHOR_TIME
from tecton_core.schema import Schema
from tecton_core.time_utils import convert_duration_to_seconds
from tecton_core.time_utils import convert_epoch_to_datetime
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.data.feature_view_pb2 import MaterializationTimeRangePolicy


@attrs.frozen
class OdfvPipelineNode(QueryNode):
    """
    Evaluates an odfv pipeline on top of an input containing columns prefixed '_udf_internal' to be used as dependent feature view inputs. The _udf_internal contract is
    documented in pipeline_helper.py
    The input may also have other feature values. This ensures we can match multiple odfv features to the right rows based on request context without joining them.
    In order to make this possible, a namespace is also passed through at this point to ensure the odfv features do not conflict with other features.
    """

    input_node: NodeRef
    feature_definition_wrapper: FeatureDefinitionWrapper
    namespace: str

    @property
    def columns(self) -> Tuple[str, ...]:
        sep = self.feature_definition_wrapper.namespace_separator
        return tuple(
            list(self.input_node.columns)
            + [f"{self.namespace}{sep}{name}" for name in self.feature_definition_wrapper.view_schema.column_names()]
        )

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return f"Evaluate on-demand feature view pipeline '{self.feature_definition_wrapper.name}'"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class FeatureViewPipelineNode(QueryNode):
    inputs_map: Dict[str, NodeRef]
    feature_definition_wrapper: FeatureDefinitionWrapper

    # Needed for correct behavior by tecton_sliding_window udf if it exists in the pipeline
    feature_time_limits: Optional[pendulum.Period]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.feature_definition_wrapper.view_schema.column_names()

    @property
    def schedule_interval(self) -> pendulum.Duration:
        # Note: elsewhere we set this to pendulum.Duration(seconds=fv_proto.materialization_params.schedule_interval.ToSeconds())
        # but that seemed wrong for bwafv
        return self.feature_definition_wrapper.batch_materialization_schedule

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple(self.inputs_map.values())

    @property
    def input_names(self) -> Optional[List[str]]:
        return list(self.inputs_map.keys())

    def as_str(self):
        s = f"Evaluate feature view pipeline '{self.feature_definition_wrapper.name}'"
        if self.feature_time_limits:
            s += f" with feature time limits [{self.feature_time_limits.start}, {self.feature_time_limits.end})"
        return s

    def _to_query(self) -> pypika.Query:
        # maps input names to unique strings
        unique_inputs_map = {k: f"{k}_{id(self)}" for k in self.inputs_map}
        queries = PipelineSqlBuilder(
            pipeline=self.feature_definition_wrapper.pipeline,
            id_to_transformation={t.id: t for t in self.feature_definition_wrapper.transformations},
            materialization_context=BoundMaterializationContext._create_from_period(
                self.feature_time_limits,
                self.schedule_interval,
            ),
            renamed_inputs_map=unique_inputs_map,
        ).get_queries()
        # the base query is the query from the root of the pipeline (at the end of the list)
        res = CustomQuery(queries[-1][0])
        # add CTE for each of the inputs, aliased to the unique name
        for k in unique_inputs_map:
            res = res.with_(self.inputs_map[k]._to_query(), unique_inputs_map[k])
        for t_node in queries[:-1]:
            query, alias = t_node
            res = res.with_(CustomQuery(query), alias)
        return res


@attrs.frozen
class DataSourceScanNode(QueryNode):
    """Scans a batch data source and applies the given time range filter, or reads a stream source.

    Attributes:
        ds: The data source to be scanned or read.
        ds_node: The DataSourceNode (proto object, not QueryNode) corresponding to the data source. Used for rewrites.
        is_stream: If True, the data source is a stream source.
        start_time: The start time to be applied.
        end_time: The end time to be applied.
    """

    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        if self.ds.type == DataSourceType.STREAM_WITH_BATCH:
            # TODO(brian) - mypy complains this is a Tuple[Any,...]
            return tuple(str(f.name) for f in self.ds.stream_source.spark_schema.fields)
        elif self.ds.type in (DataSourceType.PUSH_NO_BATCH, DataSourceType.PUSH_WITH_BATCH):
            return tuple(str(f.name) for f in self.ds.schema.tecton_schema.columns)
        elif self.ds.type == DataSourceType.BATCH:
            return tuple(str(f.name) for f in self.ds.batch_source.spark_schema.fields)
        else:
            raise NotImplementedError

    # MyPy has a known issue on validators https://mypy.readthedocs.io/en/stable/additional_features.html#id1
    @is_stream.validator  # type: ignore
    def check_no_time_filter(self, _, is_stream: bool):
        if is_stream and (self.start_time is not None or self.end_time is not None):
            raise ValueError("Raw data filtering cannot be run on a stream source")

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    def as_str(self):
        verb = "Read stream source" if self.is_stream else "Scan data source"
        s = f"{verb} '{self.ds.name}'"
        if self.start_time and self.end_time:
            s += f" and apply time range filter [{self.start_time}, {self.end_time})"
        elif self.start_time:
            s += f" and filter by start time {self.start_time}"
        elif self.end_time:
            s += f" and filter by end time {self.end_time}"
        elif not self.is_stream:
            # No need to warn for stream sources since they don't support time range filtering.
            s += ". WARNING: there is no time range filter so all rows will be returned. This can be very inefficient."
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            s += f". WARNING: since start time >= end time, no rows will be returned."
        return s

    def _to_query(self) -> pypika.Query:
        if self.is_stream:
            raise NotImplementedError
        source = self.ds.batch_source
        if hasattr(source, "table") and source.table:
            from_str = Database(source.database)
            if hasattr(source, "schema") and source.schema:
                from_str = from_str.__getattr__(source.schema)
            from_str = from_str.__getattr__(source.table)
        elif hasattr(source, "query") and source.query:
            from_str = CustomQuery(source.query)
        else:
            raise NotImplementedError
        return Query().from_(from_str).select("*")


@attrs.frozen
class RawDataSourceScanNode(QueryNode):
    """Scans a data source without applying the post processor.

    Attributes:
        ds: The data source to be scanned.
    """

    ds: specs.DataSourceSpec

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(f.name for f in self.ds.batch_source.spark_schema.fields)

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    def as_str(self):
        if self.is_stream:
            return f"Read stream {self.ds.name}"
        else:
            return f"Scan data source '{self.ds.name} without applying a post processor"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class OfflineStoreScanNode(QueryNode):
    """
    Fetch values from offline store
    """

    feature_definition_wrapper: FeatureDefinitionWrapper
    time_filter: Optional[pendulum.Period] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        offline_store_config = self.feature_definition_wrapper.offline_store_config
        store_type = offline_store_config.WhichOneof("store_type")
        cols = self.feature_definition_wrapper.materialization_schema.column_names()
        if self.feature_definition_wrapper.is_temporal and store_type == "parquet":
            # anchor time is not included in m13n schema for bfv/sfv
            cols.append(default_case(ANCHOR_TIME))
        return cols

    def as_str(self):
        s = f"Scan offline store for '{self.feature_definition_wrapper.name}'"
        if self.time_filter:
            s += f" with feature time limits [{self.time_filter.start}, {self.time_filter.end}]"
        return s

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    @property
    def store_type(self) -> str:
        return self.feature_definition_wrapper.offline_store_config.WhichOneof("store_type")

    def _to_query(self) -> pypika.Query:
        workspace_prefix = self.feature_definition_wrapper.workspace.replace("-", "_")
        where_conds = self._get_partition_filters()
        fields = self._get_select_fields()
        q = Query().from_(Table(f"{workspace_prefix}__{self.feature_definition_wrapper.name}")).select(*fields)
        for w in where_conds:
            q = q.where(w)
        return q

    def _get_partition_filters(self) -> List[Term]:
        # Whenever the partition filtering logic is changed, also make sure the changes are applied to the spark
        # version in tecton_spark/offline_store.py

        if not self.time_filter:
            return []
        partition_params = get_offline_store_partition_params(self.feature_definition_wrapper)
        partition_col = Field(partition_params.partition_by)
        if partition_params.partition_by == ANCHOR_TIME or (
            partition_params.partition_by == TIME_PARTITION and partition_params.partition_type == PartitionType.EPOCH
        ):
            partition_col = Cast(partition_col, "bigint")

        partition_filters = []
        partition_lower_bound = None
        partition_upper_bound = None
        if partition_params.partition_type == PartitionType.DATE_STR:
            if self.time_filter.start:
                partition_lower_bound = timestamp_to_partition_date_str(self.time_filter.start, partition_params)
            if self.time_filter.end:
                partition_upper_bound = timestamp_to_partition_date_str(self.time_filter.end, partition_params)
        elif partition_params.partition_type == PartitionType.EPOCH:
            if self.time_filter.start:
                partition_lower_bound = timestamp_to_partition_epoch(
                    self.time_filter.start,
                    partition_params,
                    self.feature_definition_wrapper.is_continuous,
                    self.feature_definition_wrapper.get_feature_store_format_version,
                )
            if self.time_filter.end:
                partition_upper_bound = timestamp_to_partition_epoch(
                    self.time_filter.end,
                    partition_params,
                    self.feature_definition_wrapper.is_continuous,
                    self.feature_definition_wrapper.get_feature_store_format_version,
                )

        if partition_lower_bound:
            partition_filters.append(partition_col >= partition_lower_bound)
        if partition_upper_bound:
            partition_filters.append(partition_col <= partition_upper_bound)
        return partition_filters

    def _get_select_fields(self) -> List[Term]:
        offline_store_config = self.feature_definition_wrapper.offline_store_config
        store_type = offline_store_config.WhichOneof("store_type")
        fields = []
        for col in self.columns:
            if col == TIME_PARTITION:
                continue
            elif col == ANCHOR_TIME:
                # Only parquet store and bwafv delta store have _anchor_time column
                # we probably dont need to actually keep this column in the general parquet case
                if store_type == "parquet" or self.feature_definition_wrapper.is_temporal_aggregate:
                    fields.append(Cast(Field(ANCHOR_TIME), "bigint").as_(ANCHOR_TIME))
            else:
                fields.append(col)
        return fields


@attrs.frozen
class JoinNode(QueryNode):
    """Join two inputs.

    Attributes:
        left: The left input of the join.
        right: The right input of the join.
        join_cols: The columns to join on.
        how: The type of join. For example, 'inner' or 'left'. This will be passed directly to pyspark.
    """

    left: NodeRef
    right: NodeRef
    join_cols: List[str]
    how: str

    @property
    def columns(self) -> Tuple[str, ...]:
        right_nonjoin_cols = set(self.right.columns) - set(self.join_cols)
        return tuple(list(self.left.columns) + list(right_nonjoin_cols))

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.left, self.right)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["left", "right"]

    def as_str(self):
        return f"{self.how.capitalize()} join on {self.join_cols}:"

    def _to_query(self) -> pypika.Query:
        left_q = self.left.node._to_query()
        if not conf.get_bool("QUERYTREE_SHORT_SQL_ENABLED"):
            right_q = self.right.node._to_query()
        else:
            right_q = Table(self._get_view_name())

        join_q = Query().from_(left_q)
        if self.how == "inner":
            join_q = join_q.inner_join(right_q)
        elif self.how == "left":
            join_q = join_q.left_join(right_q)
        elif self.how == "right":
            join_q = join_q.right_join(right_q)
        elif self.how == "outer":
            join_q = join_q.outer_join(right_q)
        else:
            raise NotImplementedError(f"Join Type {self.how} has not been implemented")
        return join_q.using(*self.join_cols).select("*")

    def get_sql_views(self) -> List[Tuple[str, str]]:
        if not conf.get_bool("QUERYTREE_SHORT_SQL_ENABLED"):
            return []
        view_sql = self.right.node.to_sql()
        return [(self._get_view_name(), view_sql)]

    def _get_view_name(self) -> str:
        return self.right.node.__class__.__name__ + "_" + str(id(self.right.node)) + "_" + "view"


@attrs.frozen
class WildcardJoinNode(QueryNode):
    """Outer join two inputs, ensuring that columns being NULL doesn't duplicate rows.

    This behavior is important for wildcards to ensure that we don't grow duplicate NULL wildcard matches.

    Attributes:
        left: The left input of the join.
        right: The right input of the join.
        join_cols: The columns to join on.
    """

    left: NodeRef
    right: NodeRef
    join_cols: List[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        right_nonjoin_cols = set(self.right.columns) - set(self.join_cols)
        return tuple(list(self.left.columns) + list(right_nonjoin_cols))

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.left, self.right)

    def as_str(self, verbose: bool):
        return f"Outer join (include nulls)" + (f" on {self.join_cols}:" if verbose else ":")

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class EntityFilterNode(QueryNode):
    """Filters the feature data by the entities with respect to a set of entity columns.

    Attributes:
        feature_data: The features to be filtered.
        entities: The entities to filter by.
        entity_cols: The set of entity columns to filter by.
    """

    feature_data: NodeRef
    entities: NodeRef
    entity_cols: List[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.feature_data.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.feature_data, self.entities)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["feature_data", "entities"]

    def as_str(self):
        return f"Filter feature data by entities with respect to {self.entity_cols}:"

    def _to_query(self) -> pypika.Query:
        feature_data = self.feature_data._to_query()
        entities = self.entities._to_query()
        return Query().from_(feature_data).inner_join(entities).on_field(*self.entity_cols).select(*self.columns)


@attrs.frozen
class AsofJoinInputContainer:
    node: NodeRef
    timestamp_field: str  # spine or feature timestamp
    effective_timestamp_field: Optional[str] = None
    prefix: Optional[str] = None
    # The right side of asof join needs to know a schema to typecast
    # back to original types in snowflake, because the asof implementation loses
    # types in the middle.
    schema: Optional[Schema] = None


@attrs.frozen
class AsofJoinNode(QueryNode):
    """
    A "basic" asof join on 2 inputs
    """

    left_container: AsofJoinInputContainer
    right_container: AsofJoinInputContainer
    join_cols: List[str]

    _right_struct_col: ClassVar[str] = "_right_values_struct"

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(
            list(self.left_container.node.columns)
            + [
                f"{self.right_container.prefix}_{col}"
                for col in self.right_container.node.columns
                if col not in (self.join_cols)
            ]
        )

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.left_container.node, self.right_container.node)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["left", "right"]

    def as_str(self):
        return f"Left asof join right, where the join condition is right.{self.right_container.effective_timestamp_field} <= left.{self.left_container.timestamp_field}"

    def _to_query(self) -> pypika.Query:
        ASOF_JOIN_TIMESTAMP_COL_1 = "_ASOF_JOIN_TIMESTAMP_1"
        ASOF_JOIN_TIMESTAMP_COL_2 = "_ASOF_JOIN_TIMESTAMP_2"
        IS_LEFT = "IS_LEFT"
        left_df = self.left_container.node._to_query()
        right_df = self.right_container.node._to_query()
        # The left and right dataframes are unioned together and sorted using 2 columns.
        # The spine will use the spine timestamp and the features will be ordered by their
        # (effective_timestamp, feature_timestamp) because multiple features can have the same effective
        # timestamp. We want to return the closest feature to the spine timestamp that also satisfies
        # the condition => effective timestamp <= spine timestamp.
        # The ASOF_JOIN_TIMESTAMP_COL_1 and ASOF_JOIN_TIMESTAMP_COL_2 columns will be used for sorting.
        left_name = self.left_container.node.node.__class__.__name__ + "_" + str(id(self.left_container.node))
        right_name = self.right_container.node.node.__class__.__name__ + "_" + str(id(self.right_container.node))
        left_df = (
            Query()
            .with_(left_df, left_name)
            .from_(AliasedQuery(left_name))
            .select(
                Table(left_name).star,
                Field(self.left_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_1),
                Field(self.left_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_2),
            )
        )
        right_df = (
            Query()
            .with_(right_df, right_name)
            .from_(AliasedQuery(right_name))
            .select(
                Field(self.right_container.effective_timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_1),
                Field(self.right_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_2),
                Table(right_name).star,
            )
        )

        # includes both fv join keys and the temporal asof join key
        timestamp_join_cols = [ASOF_JOIN_TIMESTAMP_COL_1, ASOF_JOIN_TIMESTAMP_COL_2]
        common_cols = self.join_cols + timestamp_join_cols
        left_nonjoin_cols = [col for col in self.left_container.node.columns if col not in common_cols]
        # we additionally include the right time field though we join on the left's time field.
        # This is so we can see how old the row we joined against is and later determine whether to exclude on basis of ttl
        right_nonjoin_cols = [
            col for col in self.right_container.node.columns if col not in set(self.join_cols + timestamp_join_cols)
        ]
        left_full_cols = (
            [LiteralValue(True).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [Field(x) for x in left_nonjoin_cols]
            + [NULL.as_(self._right_struct_col)]
        )
        mapping = {f"{self.right_container.prefix}_{x}": Field(x) for x in right_nonjoin_cols}
        right_full_cols = (
            [LiteralValue(False).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [NULL.as_(x) for x in left_nonjoin_cols]
            + [struct(right_nonjoin_cols).as_(self._right_struct_col)]
        )
        left_df = Query().from_(left_df).select(*left_full_cols)
        right_df = Query().from_(right_df).select(*right_full_cols)
        union = left_df.union(right_df)
        right_window_funcs = []
        # Also order by IS_LEFT because we want spine rows to be after feature rows if
        # timestamps are the same
        order_by_fields = timestamp_join_cols + [IS_LEFT]
        right_window_funcs.append(
            LastValue(Field(self._right_struct_col))
            .over(*[Field(x) for x in self.join_cols])
            .orderby(*[Field(x) for x in order_by_fields])
            .rows(an.Preceding(), an.CURRENT_ROW)
            .ignore_nulls()
            .as_(self._right_struct_col)
        )

        # We use the right side of asof join to find the latest values to augment to the rows from the left side.
        # Then, we drop the right side's rows.
        res = Query().from_(union).select(*(common_cols + left_nonjoin_cols + right_window_funcs + [Field(IS_LEFT)]))
        assert self.right_container.schema is not None
        right_fields = struct_extract(
            self._right_struct_col,
            right_nonjoin_cols,
            [f"{self.right_container.prefix}_{name}" for name in right_nonjoin_cols],
            self.right_container.schema.to_dict(),
        )
        res = Query().from_(res).select(*(common_cols + left_nonjoin_cols + right_fields)).where(Field(IS_LEFT))
        return res


@attrs.frozen
class AsofJoinFullAggNode(QueryNode):
    """
    Asof join full agg rollup
    """

    spine: NodeRef
    partial_agg_node: NodeRef
    fdw: FeatureDefinitionWrapper

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.spine, self.partial_agg_node)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["spine", "partial_aggregates"]

    def as_str(self):
        return f"Spine asof join partial aggregates, where the join condition is partial_aggregates._anchor_time <= spine._anchor_time and partial aggregates are rolled up to compute full aggregates"

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.spine.columns) + self.fdw.features)

    def _get_aggregations(self, window_order_col: str, partition_cols: List[str]) -> List[Term]:
        time_aggregation = self.fdw.trailing_time_window_aggregation
        feature_store_format_version = self.fdw.get_feature_store_format_version
        aggregations = []
        for feature in time_aggregation.features:
            # We do + 1 since RangeBetween is inclusive, and we do not want to include the last row of the
            # previous tile. See https://github.com/tecton-ai/tecton/pull/1110
            window_duration = pendulum.Duration(seconds=feature.window.ToSeconds())
            if self.fdw.is_continuous:
                tile_interval = 1
            else:
                tile_interval = self.fdw.get_tile_interval_for_version
            earliest_anchor_time = (
                convert_timedelta_for_version(window_duration, feature_store_format_version) - tile_interval
            )
            # Adjust earliest_anchor_time by * 2 + 1 to account for the changes to TECTON_WINDOW_ORDER_COL
            earliest_anchor_time = an.Preceding(earliest_anchor_time * 2 + 1)
            aggregation_plan = AGGREGATION_PLANS.get(feature.function)
            names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            query_window_spec = QueryWindowSpec(
                partition_cols=partition_cols,
                order_by_col=window_order_col,
                range_start=earliest_anchor_time,
                range_end=an.CURRENT_ROW,
            )
            aggregations.append(
                aggregation_plan.full_aggregation_query_term(names, query_window_spec).as_(feature.output_feature_name)
            )
        return aggregations

    def _to_query(self) -> pypika.Query:
        left_df = self.spine.node._to_query()
        right_df = self.partial_agg_node.node._to_query()
        join_keys = self.fdw.join_keys
        timestamp_join_cols = [ANCHOR_TIME]
        common_cols = join_keys + timestamp_join_cols
        left_nonjoin_cols = list(set(self.spine.node.columns) - set(common_cols))
        left_prefix = "_tecton_left"
        right_nonjoin_cols = list(set(self.partial_agg_node.node.columns) - set(join_keys + timestamp_join_cols))
        IS_LEFT = "_tecton_is_left"

        # Since the spine and feature rows are unioned together, the spine rows must be ordered after the feature rows
        # when they have the same ANCHOR_TIME for window aggregation to be correct. Window aggregation does not allow
        # ordering using two columns when range between is used. So we adjust the spine row ANCHOR_TIME by * 2 + 1, and the
        # feature row ANCHOR_TIME by * 2. Range between values will also be adjusted due to these changes.
        TECTON_WINDOW_ORDER_COL = "_tecton_window_order_col"
        left_full_cols = (
            [LiteralValue(True).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [Field(x).as_(f"{left_prefix}_{x}") for x in left_nonjoin_cols]
            + [NULL.as_(x) for x in right_nonjoin_cols]
            + [(Field(ANCHOR_TIME) * 2 + 1).as_(TECTON_WINDOW_ORDER_COL)]
        )
        right_full_cols = (
            [LiteralValue(False).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [NULL.as_(f"{left_prefix}_{x}") for x in left_nonjoin_cols]
            + [Field(x) for x in right_nonjoin_cols]
            + [(Field(ANCHOR_TIME) * 2).as_(TECTON_WINDOW_ORDER_COL)]
        )
        left_df = Query().from_(left_df).select(*left_full_cols)
        right_df = Query().from_(right_df).select(*right_full_cols)
        union = left_df.union(right_df)

        aggregations = self._get_aggregations(TECTON_WINDOW_ORDER_COL, join_keys)
        output_columns = (
            common_cols
            + [Field(f"{left_prefix}_{x}").as_(x) for x in left_nonjoin_cols]
            + aggregations
            + [Field(IS_LEFT)]
        )
        res = Query().from_(union).select(*output_columns)
        return Query().from_(res).select(*[Field(c) for c in self.columns]).where(Field(IS_LEFT))


@attrs.frozen
class AsofWildcardExplodeNode(QueryNode):
    """
    Coverts a spine missing the wildcard join_key into a spine that has all
    values of the wildcard join_keys that should be returned by the feature
    query for BWAFV/SWAFV.

    E.g. Let's say FV has fully bound join_key `A` and wildcard join_key `C`.
    For every row `[a_0, anchor_0]` from the spine, we will have the following rows in the
    returned dataframe:
       [a_0  c_1  anchor_0]
       [a_0  c_2  anchor_0]
        .    .    .
       [a_0  c_k  anchor_0]
    where (`c_1`, ..., `c_k`) represent all the wildcard join_key values such that, the following row is
    present inside `right`:
        [a_0, c_i, anchor_i]
    and:
        anchor_0 - max_feature_agg_period (or ttl) < anchor_i <= anchor_0.
    """

    left: NodeRef
    left_ts: str
    right: NodeRef
    right_ts: str
    fdw: FeatureDefinitionWrapper

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.left, self.right)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["left", "right"]

    def as_str(self):
        return f"Left asof wildcard match and explode right, where the join condition is left._anchor_time - ttl + 1 < right._anchor_time <= left._anchor_time."

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.left.columns) + [self.fdw.wildcard_join_key])

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class PartialAggNode(QueryNode):
    """Performs partial aggregations.

    Should only be used on WAFVs.

    For non-continuous WAFV, the resulting dataframe will have an anchor time column that represents the start times of
    the tiles. For a continuous SWAFV, since there are no tiles, the resulting dataframe will have an anchor time column
    that is just a copy of the input timestamp column. And it will also call it "_anchor_time".

    Attributes:
        input_node: The input node to be transformed.
        fdw: The feature view to be partially aggregated.
        window_start_column_name: The name of the anchor time column.
        window_end_column_name: If set, a column will be added to represent the end times of the tiles, and it will
            have name `window_end_column_name`. This is ignored for continuous mode.
        aggregation_anchor_time: If set, it will be used to determine the offset for the tiles.
    """

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper = attrs.field()
    window_start_column_name: str
    window_end_column_name: Optional[str] = None
    aggregation_anchor_time: Optional[datetime] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        cols = self.fdw.materialization_schema.column_names()
        # TODO(Felix) this is janky
        if self.window_end_column_name is not None and not self.fdw.is_continuous:
            cols.append(self.window_end_column_name)
        return cols

    @fdw.validator
    def check_is_aggregate(self, _, value):
        if not value.is_temporal_aggregate:
            raise ValueError("Cannot construct a PartialAggNode using a non-aggregate feature view.")

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        actions = [
            f"Perform partial aggregations with column '{self.window_start_column_name}' as the start time of tiles."
        ]
        if self.window_end_column_name:
            actions.append(f"Add column '{self.window_end_column_name}' as the end time of tiles.")
        if self.aggregation_anchor_time:
            actions.append(
                f"Align column '{self.fdw.timestamp_key}' to the offset determined by {self.aggregation_anchor_time}."
            )
        return " ".join(actions)

    def _to_query(self) -> pypika.Query:
        q = Query().from_(self.input_node._to_query())
        time_aggregation = self.fdw.trailing_time_window_aggregation
        timestamp_field = Field(time_aggregation.time_key)

        agg_cols = self._get_partial_agg_columns()
        join_cols = [Field(join_key) for join_key in self.fdw.join_keys]
        if not time_aggregation.is_continuous:
            slide_seconds = time_aggregation.aggregation_slide_period.seconds
            anchor_time_offset_seconds = 0
            if self.aggregation_anchor_time:
                # Compute the offset from the epoch such that anchor_time aligns to an interval boundary of size
                # aggregation_slide_period. i.e. `epoch + offset + (X * slide_period) = anchor_time`, where X is
                # an integer.
                anchor_time_epoch_secs = int(self.aggregation_anchor_time.timestamp())
                anchor_time_offset_seconds = anchor_time_epoch_secs % slide_seconds

            adjusted_time_key_field = to_unixtime(timestamp_field) - anchor_time_offset_seconds
            window_start = (
                to_unixtime(from_unixtime(adjusted_time_key_field - (adjusted_time_key_field % slide_seconds)))
                + anchor_time_offset_seconds
            )
            window_end = (
                to_unixtime(
                    from_unixtime(adjusted_time_key_field - (adjusted_time_key_field % slide_seconds) + slide_seconds)
                )
                + anchor_time_offset_seconds
            )

            window_start = convert_epoch_seconds_to_feature_store_format_version(
                window_start, self.fdw.get_feature_store_format_version
            )
            window_end = convert_epoch_seconds_to_feature_store_format_version(
                window_end, self.fdw.get_feature_store_format_version
            )

            select_cols = agg_cols + join_cols + [window_start.as_(self.window_start_column_name)]
            group_by_cols = join_cols + [window_start]
            group_by_cols.append(window_end)
            q = q.groupby(*group_by_cols)
            if self.window_end_column_name:
                select_cols.append(window_end.as_(self.window_end_column_name))
        else:
            # Continuous
            select_cols = agg_cols + join_cols + [timestamp_field, Field(time_aggregation.time_key).as_(ANCHOR_TIME)]
        res = q.select(*select_cols)
        return res

    def _get_partial_agg_columns(self):
        time_aggregation = self.fdw.trailing_time_window_aggregation
        agg_cols = []
        output_columns = set()
        for feature in time_aggregation.features:
            aggregation_plan = AGGREGATION_PLANS.get(feature.function)
            if time_aggregation.is_continuous:
                agg_query_terms = aggregation_plan.continuous_aggregation_query_terms(feature.input_feature_name)
            else:
                agg_query_terms = aggregation_plan.partial_aggregation_query_terms(feature.input_feature_name)

            for column_name, aggregated_column in zip(
                aggregation_plan.materialized_column_names(feature.input_feature_name),
                agg_query_terms,
            ):
                if column_name in output_columns:
                    continue
                output_columns.add(column_name)
                agg_cols.append(aggregated_column.as_(column_name))
        return agg_cols


@attrs.frozen
class AddAnchorTimeNode(QueryNode):
    """Augment a dataframe with an anchor time column that represents the batch materialization window.

    This is useful for preparing a dataframe for materialization, as the materialization logic requires an anchor time
    column for BFVs and BWAFVs. BWAFVs are handled as a special case elsewhere, so this node should only be used on
    BFVs. The anchor time is the start time of the materialization window, so it is calculated as
    window('timestamp_field', batch_schedule).start.

    Attributes:
        input_node: The input node to be transformed.
        feature_store_format_version: The feature store format version for the FV, which determines whether its
            timestamp is in seconds or nanoseconds.
        batch_schedule: The batch materialization schedule for the feature view, with units determined by `feature_store_format_version`.
        timestamp_field: The column name of the feature timestamp field.
    """

    input_node: NodeRef
    feature_store_format_version: int
    batch_schedule: int
    timestamp_field: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns + [default_case(ANCHOR_TIME)]

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return (
            "Add anchor time column '_anchor_time' to represent the materialization window. "
            f"It is calculated as window('{self.timestamp_field}', batch_schedule).start where batch_schedule = "
            f"{convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)} seconds."
        )

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        secs = convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)
        anchor_field = (to_unixtime(Field(self.timestamp_field)) - to_unixtime(Field(self.timestamp_field)) % secs).as_(
            default_case(ANCHOR_TIME)
        )
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*", anchor_field)


@attrs.frozen
class AddRetrievalAnchorTimeNode(QueryNode):
    """Augment a dataframe with an anchor time column that represents the most recent features available for retrieval.

    This node should only be used on WAFVs.

    The column will be an epoch column with units determined by `feature_store_format_version`.

    For continuous SWAFV, features are not aggregated, so the anchor time column is simply a copy of the retrieval
    timestamp column.

    For non-continuous WAFV, features are aggregated in tiles, so the anchor time column represents the most recent tile
    available for retrieval. At time t, the most recent tile available for retrieval is equivalent to the most recent
    tile for which any feature row has an effective timestamp that is less than t. Thus for non-continuous WAFV, this
    node is conceptually the opposite of `AddEffectiveTimestampNode`.

    For example, consider feature retrieval for a BWAFV at time t. Let T = t - data_delay. Then the most recent
    materialization job ran at time T - (T % batch_schedule), so the most recent tile available for retrieval is the
    last tile that was materialized by that job, which has anchor time T - (T % batch_schedule) - tile_interval.

    Similarly, consider feature retrieval for a SWAFV at time T. Since there is no data delay, the most recent
    materialization job ran at time T - (T % tile_interval), so the most recent tile available for retrieval is the
    last tile that was materialized by that job, which has anchor time T - (T % tile_interval) - tile_interval.

    Attributes:
        input_node: The input node to be transformed.
        name: The name of the feature view.
        feature_store_format_version: The feature store format version for the FV, which determines whether its
            timestamp is in seconds or nanoseconds.
        batch_schedule: The batch materialization schedule for the feature view, with units determined by `feature_store_format_version`.
            Only used for BWAFVs.
        tile_interval: The tile interval for the feature view, with units determined by `feature_store_format_version`.
        timestamp_field: The column name of the retrieval timestamp field.
        is_stream: If True, the WAFV is a SWAFV.
        data_delay_seconds: The data delay for the feature view, in seconds.
    """

    input_node: NodeRef
    name: str
    feature_store_format_version: int
    batch_schedule: int
    tile_interval: int
    timestamp_field: str
    is_stream: bool
    data_delay_seconds: Optional[int] = 0

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.input_node.columns) + [ANCHOR_TIME])

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        base = (
            "Add anchor time column '_anchor_time' to represent the most recent feature data available for retrieval. "
            "The time at which feature data becomes available for retrieval depends on two factors: the frequency at "
            "which the feature view is materialized, and the data delay. "
        )

        if self.tile_interval == 0:  # Continuous
            return (
                base
                + f"Since '{self.name}' is a stream feature view with aggregations in continuous mode, the anchor time "
                + f"column is just a copy of the timestamp column '{self.timestamp_field}'."
            )
        elif self.is_stream:
            return (
                base
                + f"Since '{self.name} is a stream feature view with aggregations in time interval mode, feature data "
                + "is stored in tiles. Each tile has size equal to the tile interval, which is "
                + f"{convert_duration_to_seconds(self.tile_interval, self.feature_store_format_version)} seconds. "
                + f"The anchor time column contains the start time of the most recent tile available for retrieval. "
                + f"It is calculated as '{self.timestamp_field}' - ('{self.timestamp_field}' % tile_interval) "
                + f"- tile_interval."
            )
        else:
            if self.data_delay_seconds > 0:
                data_delay_seconds = f"Let T = '{self.timestamp_field}' - data_delay where data_delay = {self.data_delay_seconds} seconds. "
            else:
                data_delay_seconds = f"Let T be the timestamp column '{self.timestamp_field}'. "

            return (
                base
                + f"Since '{self.name}' is a batch feature view with aggregations, feature data is stored in tiles. "
                + "Each tile has size equal to the tile interval, which is "
                f"{convert_duration_to_seconds(self.tile_interval, self.feature_store_format_version)} seconds. "
                + f"The anchor time column contains the start time of the most recent tile available for retrieval. "
                + data_delay_seconds
                + f"The anchor time column is calculated as T - (T % batch_schedule) - tile_interval where batch_schedule = "
                f"{convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)} seconds."
            )

    def _to_query(self) -> pypika.Query:
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        input_query = self.input_node._to_query()
        data_delay_seconds = self.data_delay_seconds or 0
        anchor_time_field = convert_epoch_seconds_to_feature_store_format_version(
            to_unixtime(date_add("second", -data_delay_seconds, Field(self.timestamp_field))),
            self.feature_store_format_version,
        )
        if self.tile_interval == 0:
            return (
                Query()
                .with_(input_query, uid)
                .from_(AliasedQuery(uid))
                .select("*", anchor_time_field.as_(default_case(ANCHOR_TIME)))
            )
        # For stream, we use the tile interval for bucketing since the data is available as soon as
        # the aggregation interval ends.
        # For BAFV, we use the batch schedule to get the last tile written.
        if self.is_stream:
            anchor_time_field = anchor_time_field - anchor_time_field % self.tile_interval - self.tile_interval
        else:
            anchor_time_field = anchor_time_field - anchor_time_field % self.batch_schedule - self.tile_interval
        return (
            Query()
            .with_(input_query, uid)
            .from_(AliasedQuery(uid))
            .select("*", anchor_time_field.as_(default_case(ANCHOR_TIME)))
        )


@attrs.frozen
class ConvertEpochToTimestampNode(QueryNode):
    """Convert epoch columns to timestamp columns.

    Attributes:
        input_node: The input node to be transformed.
        feature_store_formats: A dictionary mapping column names to feature store format versions. Each column in this
            dictionary will be converted from epoch to timestamp. Its feature store format version determines whether
            the timestamp is in seconds or nanoseconds.
    """

    input_node: NodeRef
    feature_store_formats: Dict[str, int]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return (
            f"Convert columns {list(self.feature_store_formats.keys())} from epoch (either seconds or ns) to timestamp."
        )

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        fields = []
        for col in self.input_node.columns:
            feature_store_format_version = self.feature_store_formats.get(col)
            field = Field(col)
            if feature_store_format_version:
                epoch_field_in_secs = convert_epoch_term_in_seconds(field, feature_store_format_version)
                fields.append(from_unixtime(epoch_field_in_secs).as_(col))
            else:
                fields.append(field)
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*fields)


@attrs.frozen
class RenameColsNode(QueryNode):
    """
    Rename columns according to `mapping`. No action is taken for columns mapped to `None`. Drop columns in `drop`.
    """

    input_node: NodeRef
    mapping: Optional[Dict[str, str]] = attrs.field(default=None)
    drop: Optional[List[str]] = None

    @mapping.validator  # type: ignore
    def check_non_null_keys(self, _, value):
        if value is None:
            return
        for k in value.keys():
            if k is None:
                raise ValueError(f"RenameColsNode mapping should only contain non-null keys. Mapping={value}")

    @property
    def columns(self) -> Tuple[str, ...]:
        cols = self.input_node.columns
        assert cols is not None, self.input_node
        newcols = []
        for col in cols:
            if self.drop and col in self.drop:
                continue
            elif self.mapping and col in self.mapping:
                newcols.append(self.mapping[col])
            else:
                newcols.append(col)
        return tuple(newcols)

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        actions = []
        if self.mapping:
            actions.append(f"Rename columns with map {self.mapping}.")
        if self.drop:
            # NOTE: the order of drop columns is unimportant
            actions.append(f"Drop columns {sorted(self.drop)}.")
        if not actions:
            actions.append("No columns are renamed or dropped.")
        return " ".join(actions)

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        projections = []
        for col in self.input_node.columns:
            if self.drop and col in self.drop:
                continue
            elif self.mapping and col in self.mapping:
                projections.append(Field(col).as_(self.mapping[col]))
            else:
                projections.append(Field(col))
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*projections)


@attrs.frozen
class UserSpecifiedDataNode(QueryNode):
    """Arbitrary data container.

    The executor node will need to typecheck and know how to handle the type of mock data.
    """

    data: DataframeWrapper
    metadata: Optional[Dict[str, Any]] = attrs.field(default=None)

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.data.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    def as_str(self):
        return f"User provided data with columns {'|'.join(self.columns)}"

    def _to_query(self) -> pypika.Query:
        t = self.data._temp_table_name
        return Query().from_(Table(t)).select(*self.columns)


@attrs.frozen
class MockDataSourceScanNode(QueryNode):
    """Provides mock data for a data source and applies the given time range filter.

    Attributes:
        data: The mock data, in the form of a NodeRef.
        ds: The data source being mocked.
        columns: The columns of the data.
        start_time: The start time to be applied.
        end_time: The end time to be applied.
    """

    data: NodeRef
    ds: specs.DataSourceSpec
    columns: Tuple[str]
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.data,)

    def as_str(self):
        s = f"Read mock data source '{self.ds.name}'"
        if self.start_time:
            s += f" and filter by start time {self.start_time}"
        if self.end_time:
            s += f" and filter by end time {self.end_time}"
        return s

    def _to_query(self) -> pypika.Query:
        uid = self.data.node.__class__.__name__ + "_" + str(id(self.data.node))
        input_query = self.data._to_query()
        timestamp_field = Field(self.ds.batch_source.timestamp_field)
        q = Query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*")
        if self.start_time:
            q.where(timestamp_field >= to_timestamp(self.start_time))
        if self.end_time:
            q.where(timestamp_field < to_timestamp(self.end_time))
        return q


@attrs.frozen
class RespectFeatureStartTimeNode(QueryNode):
    """
    Null out all features outside of feature start time

    NOTE: the feature start time is assumed to already be in appropriate units
    for the column: nanoseconds/seconds for anchor time filter, or timestamp
    for timestamp filter
    """

    input_node: NodeRef
    retrieval_time_col: str
    feature_start_time: Union[pendulum.datetime, int]
    features: List[str]
    feature_store_format_version: int

    @classmethod
    def for_anchor_time_column(
        cls, input_node: NodeRef, anchor_time_col: str, fdw: FeatureDefinitionWrapper
    ) -> "RespectFeatureStartTimeNode":
        """
        This factory method is aimed at consolidating logic for
        scenarios where we want to apply this logic to 'anchor
        time' columns.
        """
        start_time_anchor_units = time_utils.convert_timestamp_for_version(
            fdw.feature_start_timestamp, fdw.get_feature_store_format_version
        )

        # TODO: ideally we could join using 'window end' timestamps rather
        # than 'window start' anchor times and avoid this complexity.
        if fdw.is_continuous:
            # No correction needed since the earliest 'anchor time' is the
            # feature start time for continuous.
            ts = start_time_anchor_units
        else:
            # We have to subtract the tile interval from the start time to get
            # the appropriate earliest anchor time.
            ts = start_time_anchor_units - fdw.get_tile_interval_for_version

        # NOTE: this filter is extremely important for correctness.
        #   The offline store contains partial aggregates from _before_ the
        #   feature start time (with the goal of having the feature start
        #   time be the first complete aggregate). This filter ensures that
        #   spine timestamps from before the feature start time, but after
        #   we have partial aggregates in the offline store, receive null
        #   feature values.
        return cls(input_node, anchor_time_col, ts, fdw.features, fdw.get_feature_store_format_version)

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        feature_start_time = (
            convert_epoch_to_datetime(self.feature_start_time, self.feature_store_format_version)
            if isinstance(self.feature_start_time, int)
            else self.feature_start_time
        )
        return (
            f"Respect the feature start time for all rows where '{self.retrieval_time_col}' < {feature_start_time} "
            f"by setting all feature columns for those rows to NULL"
        )

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        if isinstance(self.feature_start_time, int):
            # retrieval_time_col is _anchor_time
            feature_start_time_term = self.feature_start_time
        else:
            feature_start_time_term = to_timestamp(self.feature_start_time)

        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        cond = Field(self.retrieval_time_col) >= feature_start_time_term
        project_list = []
        for c in self.columns:
            if c in self.features:
                newcol = Case().when(cond, Field(c)).else_(NULL).as_(c)
                project_list.append(newcol)
            else:
                project_list.append(Field(c))
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*project_list)


@attrs.frozen
class RespectTTLNode(QueryNode):
    """
    Null out all features with retrieval time > expiration time.
    """

    input_node: NodeRef
    retrieval_time_col: str
    expiration_time_col: str
    features: List[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return f"Null out any values where '{self.retrieval_time_col}' > '{self.expiration_time_col}'"

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        cond = Field(self.retrieval_time_col) < Field(self.expiration_time_col)
        project_list = []
        for c in self.input_node.columns:
            if c not in self.features:
                project_list.append(Field(c))
            else:
                newcol = Case().when(cond, Field(c)).else_(NULL).as_(c)
                project_list.append(newcol)
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*project_list)


@attrs.frozen
class CustomFilterNode(QueryNode):
    input_node: NodeRef
    filter_str: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    def as_str(self):
        return f"Apply filter: ({self.filter_str})"

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class FeatureTimeFilterNode(QueryNode):
    """Filters the data with respect to the given time limits and materialization policy.

    Attributes:
        input_node: The input node to be transformed.
        feature_data_time_limits: The time limits to be applied.
        policy: The materialization policy to be used.
        timestamp_field: The column name of the feature timestamp field.
    """

    input_node: NodeRef
    feature_data_time_limits: pendulum.Period
    policy: MaterializationTimeRangePolicy
    timestamp_field: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        time_range_str = f"[{self.feature_data_time_limits.start}, {self.feature_data_time_limits.end})"
        if self.policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE:
            return f"Assert all rows in column '{self.timestamp_field}' are in range {time_range_str}"
        else:
            return f"Apply time range filter {time_range_str} to column '{self.timestamp_field}'"

    def _to_query(self) -> pypika.Query:
        if self.policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE:
            # snowflake/athena are post-fwv4
            raise NotImplementedError
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        time_field = Field(self.timestamp_field)
        where_conds = []
        where_conds.append(time_field >= to_timestamp(self.feature_data_time_limits.start))
        where_conds.append(time_field < to_timestamp(self.feature_data_time_limits.end))
        q = Query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*")
        for w in where_conds:
            q = q.where(w)
        return q


@attrs.frozen
class MetricsCollectorNode(QueryNode):
    """
    Collect metrics on features
    """

    input_node: NodeRef

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return "Collect metrics on features"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class AddEffectiveTimestampNode(QueryNode):
    """Augment a dataframe with an effective timestamp.

    The effective timestamp for a given row is the earliest it will be available in the online store for inference.
    For BFVs and BWAFVs, materialization jobs run every `batch_schedule`, so the effective timestamp is calculated as
    window('timestamp_field', batch_schedule).end + data_delay, and is therefore always strictly greater than the
    feature timestamp. For SWAFVs in non-continuous mode, the feature timestamps are aligned to the aggregation window,
    so the effective timestamp is just the feature timestamp. For SFVs, SWAFVs in continuous mode, and feature tables,
    the effective timestamp is also just the feature timestamp.

    Attributes:
        input_node: The input node to be transformed.
        timestamp_field: The column name of the feature timestamp field.
        effective_timestamp_name: The name of the effective timestamp column to be added.
        is_stream: If True, the feature view has a stream data source.
        batch_schedule_seconds: The batch materialization schedule for the feature view, in seconds.
        data_delay_seconds: The data delay for the feature view, in seconds.
        is_temporal_aggregate: If True, the feature view is a WAFV.
    """

    input_node: NodeRef
    timestamp_field: str
    effective_timestamp_name: str
    batch_schedule_seconds: int
    is_stream: bool
    data_delay_seconds: int
    is_temporal_aggregate: bool

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.input_node.columns) + [self.effective_timestamp_name])

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        if self.batch_schedule_seconds == 0 or self.is_stream:
            return f"Add effective timestamp column '{self.effective_timestamp_name}' that is equal to the timestamp column '{self.timestamp_field}'."
        else:
            result = (
                f"Add effective timestamp column '{self.effective_timestamp_name}' that is equal to window('"
                f"{self.timestamp_field}', batch_schedule).end where batch_schedule = "
                f"{self.batch_schedule_seconds} seconds."
            )
            if self.data_delay_seconds > 0:
                result += f" Then add data_delay to the effective timestamp column where data_delay = {self.data_delay_seconds} seconds."
            return result

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        if self.batch_schedule_seconds == 0 or self.is_stream:
            effective_timestamp = Field(self.timestamp_field)
        else:
            timestamp_col = Field(self.timestamp_field)
            # Timestamp of temporal aggregate is end of the anchor time window. Subtract 1 milli
            # to get the correct bucket for batch schedule.
            if self.is_temporal_aggregate:
                timestamp_col = date_add("millisecond", -1, timestamp_col)
            effective_timestamp = from_unixtime(
                to_unixtime(timestamp_col)
                - (to_unixtime(timestamp_col) % self.batch_schedule_seconds)
                + self.batch_schedule_seconds
                + self.data_delay_seconds
            )
        return (
            Query()
            .with_(input_query, uid)
            .from_(AliasedQuery(uid))
            .select("*", effective_timestamp.as_(self.effective_timestamp_name))
        )


@attrs.frozen
class AddDurationNode(QueryNode):
    """Adds a duration to a timestamp field"""

    input_node: NodeRef
    timestamp_field: str
    duration: pendulum.Duration
    new_column_name: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.input_node.columns) + [self.new_column_name])

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return f"Add {self.duration.in_words()} to '{self.timestamp_field}' as new column '{self.new_column_name}'"

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        return (
            Query()
            .with_(input_query, uid)
            .from_(AliasedQuery(uid))
            .select(
                "*",
                date_add("second", int(self.duration.total_seconds()), Field(self.timestamp_field)).as_(
                    self.new_column_name
                ),
            )
        )


@attrs.frozen
class StreamWatermarkNode(QueryNode):
    input_node: NodeRef
    time_column: str
    stream_watermark: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return f"Set Stream Watermark {self.stream_watermark} on the DataFrame"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class SelectDistinctNode(QueryNode):
    input_node: NodeRef
    columns: List[str]

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self):
        return f"Select distinct with columns {self.columns}."

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        fields = [Field(c) for c in self.columns]
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*fields).distinct()
