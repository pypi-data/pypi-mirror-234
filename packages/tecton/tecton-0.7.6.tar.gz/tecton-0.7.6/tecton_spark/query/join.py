import logging
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

import attrs
import pendulum
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.window as spark_window

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query_consts import ANCHOR_TIME
from tecton_core.schema import Schema
from tecton_core.time_utils import convert_proto_duration_for_version
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.query.node import SparkExecNode


logger = logging.getLogger(__name__)


@attrs.frozen
class JoinSparkNode(SparkExecNode):
    """
    A basic left join on 2 inputs
    """

    left: SparkExecNode
    right: SparkExecNode
    join_cols: List[str]
    how: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)
        return left_df.join(right_df, how=self.how, on=self.join_cols)


@attrs.frozen
class WildcardJoinSparkNode(SparkExecNode):
    left: SparkExecNode
    right: SparkExecNode
    join_cols: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)

        left_columns = [getattr(left_df, col) for col in left_df.columns if col not in self.join_cols]
        right_columns = [getattr(right_df, col) for col in right_df.columns if col not in self.join_cols]

        left_df = left_df.withColumn("_tecton_join_cols", F.struct(self.join_cols))
        right_df = right_df.withColumn("_tecton_join_cols", F.struct(self.join_cols))

        return left_df.join(right_df, how="outer", on=["_tecton_join_cols"]).select(
            "_tecton_join_cols.*", *left_columns, *right_columns
        )


@attrs.frozen
class AsofJoinInputSparkContainer:
    node: SparkExecNode
    timestamp_field: str  # spine or feature timestamp
    effective_timestamp_field: Optional[str]
    prefix: Optional[str]
    schema: Optional[Schema]


@attrs.frozen
class _AsofJoinerAndWindowAggregator:
    """
    Implements an asof join + window aggregate, with the left side being the
    'spine' and the right side being used for the aggregate value.

    There are a few ways this behavior can be implemented, but by test the best
    performing method has been to union the two inputs and use a window
    function over the unioned DataFrame to do the calculation.

    This can be used for a traditional asof join by using a `last` window func on the unioned dataframe:
        last(col) OVER (PARTITION BY partition_cols ORDER BY timestamp_cols RANGE BETWEEN unbounded preceding AND current row)

    This is also used by the full aggregate rollup (which uses more complicated set of window specs and rollup functions). Example 1h count rollup:
        sum(count_col) OVER (PARTITION BY partition_cols ORDER BY timestamp_cols RANGE BETWEEN 3600 AND current row)
    """

    _left_df: pyspark.sql.DataFrame
    _right_df: pyspark.sql.DataFrame
    timestamp_cols: Tuple[str, ...]
    partition_cols: Tuple[str, ...]
    _use_window_range_between_value: bool

    _timestamp_prefix: ClassVar[str] = "_tecton_asof_join_timestamp"
    _left_prefix: ClassVar[str] = "_tecton_left"
    _is_left_column_name: ClassVar[str] = "IS_LEFT"
    _tecton_window_range_between_order_col: ClassVar[str] = "_tecton_window_range_between_order_col"

    @classmethod
    def create(
        cls,
        left_df: pyspark.sql.DataFrame,
        right_df: pyspark.sql.DataFrame,
        left_ts_cols: Sequence[str],
        right_ts_cols: Sequence[str],
        partition_cols: Sequence[str],
        use_window_range_between_value: bool,
    ):
        if len(left_ts_cols) != len(right_ts_cols):
            msg = f"Timestamp columns are not equal length: left({left_ts_cols}), right({right_ts_cols})"
            raise RuntimeError(msg)

        timestamp_cols = [f"{cls._timestamp_prefix}_{i}" for i in range(len(left_ts_cols))]

        for new_col, old_col in zip(timestamp_cols, left_ts_cols):
            left_df = left_df.withColumn(new_col, F.col(old_col))

        for new_col, old_col in zip(timestamp_cols, right_ts_cols):
            right_df = right_df.withColumn(new_col, F.col(old_col))

        return cls(
            left_df=left_df,
            right_df=right_df,
            timestamp_cols=tuple(timestamp_cols),
            partition_cols=tuple(partition_cols),
            use_window_range_between_value=use_window_range_between_value,
        )

    @property
    def common_cols(self) -> List[str]:
        return list(self.timestamp_cols) + list(self.partition_cols)

    @property
    def left_nonjoin_cols(self) -> List[str]:
        return [c for c in self._left_df.columns if c not in set(self.common_cols)]

    @property
    def _right_nonjoin_cols(self) -> List[str]:
        return [c for c in self._right_df.columns if c not in set(self.common_cols)]

    def _union(self) -> pyspark.sql.DataFrame:
        # schemas have to match exactly so that the 2 dataframes can be unioned together.
        left_full_cols = (
            [F.lit(True).alias(self._is_left_column_name)]
            + [F.col(x) for x in self.common_cols]
            + [F.col(x).alias(f"{self._left_prefix}_{x}") for x in self.left_nonjoin_cols]
            + [F.lit(None).alias(x) for x in self._right_nonjoin_cols]
        )
        right_full_cols = (
            [F.lit(False).alias(self._is_left_column_name)]
            + [F.col(x) for x in self.common_cols]
            + [F.lit(None).alias(f"{self._left_prefix}_{x}") for x in self.left_nonjoin_cols]
            + [F.col(x) for x in self._right_nonjoin_cols]
        )

        if self._use_window_range_between_value:
            # we want left rows to be sorted after right rows if timestamps are the same. But when using "window range between"
            # only 1 column can be used for sorting. As a workaround, we multiply the left rows by * 2 and then add 1. The right
            # rows will be multiplied by 2 only. This will ensure the left rows will be sorted after the right rows.
            left_full_cols.append(
                (F.col(self.timestamp_cols[0]).cast("long") * 2 + 1).alias(self._tecton_window_range_between_order_col)
            )
            right_full_cols.append(
                (F.col(self.timestamp_cols[0]).cast("long") * 2).alias(self._tecton_window_range_between_order_col)
            )

        left_df = self._left_df.select(left_full_cols)
        right_df = self._right_df.select(right_full_cols)
        return left_df.union(right_df)

    def join_and_aggregate(self, aggregations: List[pyspark.sql.Column]) -> pyspark.sql.DataFrame:
        union = self._union()

        # We use the right side of asof join to calculate the aggregate values to augment to the rows from the left side.
        # Then, we drop the right side's rows.
        output_columns = (
            self.common_cols
            + [F.col(f"{self._left_prefix}_{x}").alias(x) for x in self.left_nonjoin_cols]
            + aggregations
            + [self._is_left_column_name]
        )
        selected = union.select(output_columns)
        return selected.filter(self._is_left_column_name).drop(self._is_left_column_name, *self.timestamp_cols)

    def get_range_between_window_spec(self, range_between_start, range_between_end):
        if range_between_start == spark_window.Window.unboundedPreceding:
            order_by_cols = list(self.timestamp_cols) + [self._is_left_column_name]
        else:
            order_by_cols = [self._tecton_window_range_between_order_col]

        window_spec = (
            spark_window.Window.partitionBy(list(self.partition_cols))
            .orderBy([F.col(c).asc() for c in order_by_cols])
            .rangeBetween(range_between_start, range_between_end)
        )
        return window_spec


@attrs.frozen
class AsofJoinSparkNode(SparkExecNode):
    """
    A "basic" asof join on 2 inputs.
    LEFT asof_join RIGHT has the following behavior:
        For each row on the left side, find the latest (but <= in time) matching (by join key) row on the right side, and associate the right side's columns to that row.
    The result is a dataframe with the same number of rows as LEFT, with additional columns. These additional columns are prefixed with f"{right_prefix}_". This is the built-in behavior of the tempo library.

    """

    left_container: AsofJoinInputSparkContainer
    right_container: AsofJoinInputSparkContainer
    join_cols: List[str]

    _right_struct_col: ClassVar[str] = "_right_values_struct"

    def _structify_right(self, right_df, struct_col_name: str):
        # we additionally include the right time field though we join on the left's time field.
        # This is so we can see how old the row we joined against is and later determine whether to exclude on basis of ttl
        right_nonjoin_cols = list(set(right_df.columns) - set(self.join_cols))
        # wrap fields on the right in a struct. This is to work around null feature values and ignorenulls
        # used during joining/window function.
        cols_to_wrap = [F.col(c).alias(f"{self.right_container.prefix}_{c}") for c in right_nonjoin_cols]
        right_df = right_df.withColumn(struct_col_name, F.struct(*cols_to_wrap))
        return right_df

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left_container.node.to_dataframe(spark)
        right_df = self.right_container.node.to_dataframe(spark)

        right_df = self._structify_right(right_df, self._right_struct_col)

        # The left and right dataframes are unioned together and sorted using 2 columns.
        # The spine will use the spine timestamp and the features will be ordered by their
        # (effective_timestamp, feature_timestamp) because multiple features can have the same effective
        # timestamp. We want to return the closest feature to the spine timestamp that also satisfies
        # the condition => effective timestamp <= spine timestamp.
        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=left_df,
            right_df=right_df,
            left_ts_cols=[self.left_container.timestamp_field, self.left_container.timestamp_field],
            right_ts_cols=[self.right_container.effective_timestamp_field, self.right_container.timestamp_field],
            partition_cols=self.join_cols,
            use_window_range_between_value=False,
        )
        window_spec = join_spec.get_range_between_window_spec(
            spark_window.Window.unboundedPreceding, spark_window.Window.currentRow
        )
        aggregations = [
            F.last(F.col(self._right_struct_col), ignorenulls=True).over(window_spec).alias(self._right_struct_col)
        ]
        spine_with_features_df = join_spec.join_and_aggregate(aggregations)

        # unwrap the struct to return the fields
        final_df = spine_with_features_df.select(
            self.join_cols + join_spec.left_nonjoin_cols + [f"{self._right_struct_col}.*"]
        )
        return final_df


@attrs.frozen
class AsofJoinFullAggSparkNode(SparkExecNode):
    """
    An asof join very similar to AsofJoinNode, but with a change where it does
    the full aggregation rollup (rather than a last).

    NOTE: This should only be used for window aggregates.

    LEFT asof_join RIGHT has the following behavior:
        For each row in the spine, find the matching partial aggregates (by time range)
        and run the appropriate full aggregate over those rows.

    The result is a dataframe with the same number of rows as the spine, with
    additional columns of the fully aggregated features (or null).

    There are a few ways this behavior can be implemented, but by test the best
    performing method has been to union the two inputs and use a window
    function for the aggregates.
    """

    spine: SparkExecNode
    partial_agg_node: SparkExecNode
    fdw: FeatureDefinitionWrapper
    TECTON_AGG_WINDOW_ORDER_COL: ClassVar[str] = "_tecton_agg_window_order_col"

    def _get_aggregations(self, join_spec: _AsofJoinerAndWindowAggregator):
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
                -(convert_timedelta_for_version(window_duration, feature_store_format_version)) + tile_interval
            )
            # Since the spine and feature rows are unioned together, the spine rows must be ordered after the feature rows
            # when they have the same timestamp for window aggregation to be correct. Window aggregation does not allow
            # ordering using two columns when range between is used. As a workaround, we multiply the left rows by (* 2 + 1).
            # The right rows by * 2. This will ensure the left rows will be sorted after the right rows.
            # We need to make an adjustment here to earliest_anchor_time due to these changes.
            earliest_anchor_time = earliest_anchor_time * 2 - 1
            window_spec = join_spec.get_range_between_window_spec(earliest_anchor_time, spark_window.Window.currentRow)
            aggregation_plan = get_aggregation_plan(
                feature.function, feature.function_params, time_aggregation.is_continuous, time_aggregation.time_key
            )
            names = aggregation_plan.materialized_column_names(feature.input_feature_name)

            agg = aggregation_plan.full_aggregation_transform(names, window_spec)

            aggregations.append(agg.alias(feature.output_feature_name))
        return aggregations

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.spine.to_dataframe(spark)
        right_df = self.partial_agg_node.to_dataframe(spark)

        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=left_df,
            right_df=right_df,
            left_ts_cols=[ANCHOR_TIME],
            right_ts_cols=[ANCHOR_TIME],
            partition_cols=self.fdw.join_keys,
            use_window_range_between_value=True,
        )
        aggregations = self._get_aggregations(join_spec)

        return join_spec.join_and_aggregate(aggregations)


@attrs.frozen
class AsofWildcardExplodeSparkNode(SparkExecNode):
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

    left: SparkExecNode
    left_ts: str
    right: SparkExecNode
    right_ts: str
    fdw: FeatureDefinitionWrapper

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)

        partition_cols = [col for col in self.fdw.join_keys if col != self.fdw.wildcard_join_key]
        join_spec = _AsofJoinerAndWindowAggregator.create(
            left_df=left_df,
            right_df=right_df,
            left_ts_cols=[self.left_ts],
            right_ts_cols=[self.right_ts],
            partition_cols=partition_cols,
            use_window_range_between_value=True,
        )

        if self.fdw.is_temporal_aggregate:
            max_aggregation_window = convert_proto_duration_for_version(
                self.fdw.max_aggregation_window, version=self.fdw.get_feature_store_format_version
            )
            if self.fdw.is_continuous:
                tile_interval = 1
            else:
                tile_interval = self.fdw.get_tile_interval_for_version
            earliest_anchor_time = -max_aggregation_window + tile_interval
        else:
            # Add 1 since we expire at `ttl` time
            max_aggregation_window = int(self.fdw.serving_ttl.total_seconds())
            earliest_anchor_time = -max_aggregation_window + 1

        # Since the spine and feature rows are unioned together, the spine rows must be ordered after the feature rows
        # when they have the same timestamp for window aggregation to be correct. Window aggregation does not allow
        # ordering using two columns when range between is used. As a workaround, we multiply the left rows by (* 2 + 1).
        # The right rows by * 2. This will ensure the left rows will be sorted after the right rows.
        # We need to make an adjustment here to earliest_anchor_time due to these changes.
        earliest_anchor_time = earliest_anchor_time * 2 - 1
        window_spec = join_spec.get_range_between_window_spec(earliest_anchor_time, spark_window.Window.currentRow)
        aggregations = [F.collect_set(F.col(self.fdw.wildcard_join_key)).over(window_spec).alias("wildcard_set")]
        df = join_spec.join_and_aggregate(aggregations)
        res = df.withColumn(self.fdw.wildcard_join_key, F.explode_outer(F.col("wildcard_set"))).drop("wildcard_set")

        return res
