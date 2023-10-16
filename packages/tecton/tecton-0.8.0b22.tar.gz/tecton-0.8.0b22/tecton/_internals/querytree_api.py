import logging
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
import pendulum
from pyspark import sql as pyspark_sql

from tecton import types as sdk_types
from tecton._internals import errors
from tecton._internals import rewrite
from tecton._internals import time_utils
from tecton._internals import type_utils
from tecton._internals import utils
from tecton.framework.data_frame import TectonDataFrame
from tecton.framework.dataset import Dataset
from tecton_core import data_types
from tecton_core import errors as core_errors
from tecton_core import feature_set_config
from tecton_core import query_consts
from tecton_core import schema
from tecton_core import specs
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.query import builder
from tecton_core.query import node_interface
from tecton_core.query import nodes
from tecton_core.query import sql_compat
from tecton_core.time_utils import align_time_downwards
from tecton_proto.common import schema_pb2
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2
from tecton_spark.spark_helper import check_spark_version
from tecton_spark.time_utils import convert_epoch_to_datetime
from tecton_spark.time_utils import convert_timestamp_to_epoch


logger = logging.getLogger(__name__)


def get_historical_features_for_feature_service(
    feature_service_spec: specs.FeatureServiceSpec,
    feature_set_config: feature_set_config.FeatureSetConfig,
    spine: Union[pyspark_sql.DataFrame, pd.DataFrame, TectonDataFrame, str],
    timestamp_key: Optional[str],
    from_source: bool,
    save: bool,
    save_as: Optional[str],
) -> TectonDataFrame:
    timestamp_required = spine is not None and any(
        _should_infer_timestamp_of_spine(fd, timestamp_key) for fd in feature_set_config.feature_definitions
    )

    _check_spine_type(spine)

    if timestamp_required:
        timestamp_key = timestamp_key or utils.infer_timestamp(spine)

    if isinstance(spine, pd.DataFrame):
        spine_schema = feature_set_config.spine_schema
        if timestamp_key is not None:
            spine_schema += schema.Schema.from_dict({timestamp_key: data_types.TimestampType()})
        spine = TectonDataFrame._create_from_pandas_with_schema(spine, spine_schema)
    elif isinstance(spine, str):
        spine = TectonDataFrame._create_with_snowflake_sql(spine)
    elif not isinstance(spine, TectonDataFrame):
        spine = TectonDataFrame._create(spine)

    if spine:
        utils.validate_spine_dataframe(spine, timestamp_key, feature_set_config.request_context_keys)

    user_data_node_metadata = {}
    # TODO: Create a SpineNode with a param of timestamp_key instead of using UserSpecifiedNode.
    if timestamp_key:
        user_data_node_metadata["timestamp_key"] = timestamp_key
    tree = builder.build_feature_set_config_querytree(
        feature_set_config,
        nodes.UserSpecifiedDataNode(spine, user_data_node_metadata).as_ref(),
        timestamp_key,
        from_source,
    )

    df = TectonDataFrame._create(tree)
    if save or save_as is not None:
        return Dataset._create(
            df=df,
            save_as=save_as,
            workspace=feature_service_spec.workspace,
            feature_service_id=feature_service_spec.id,
            spine=spine,
            timestamp_key=timestamp_key,
        )
    else:
        return df


def get_historical_features_for_feature_definition(
    feature_definition: FeatureDefinitionWrapper,
    spine: Optional[Union[pyspark_sql.DataFrame, pd.DataFrame, TectonDataFrame, str]],
    timestamp_key: Optional[str],
    start_time: Optional[Union[pendulum.DateTime, datetime]],
    end_time: Optional[Union[pendulum.DateTime, datetime]],
    entities: Optional[Union[pyspark_sql.DataFrame, pd.DataFrame, TectonDataFrame]],
    from_source: bool,
    save: bool,
    save_as: Optional[str],
    mock_data_sources: Dict[str, pyspark_sql.DataFrame],
) -> TectonDataFrame:
    if not feature_definition.is_on_demand:
        check_spark_version(feature_definition.fv_spec.batch_cluster_config)

    _check_spine_type(spine)

    if spine is not None:
        if _should_infer_timestamp_of_spine(feature_definition, timestamp_key):
            timestamp_key = utils.infer_timestamp(spine)
        if isinstance(spine, pd.DataFrame):
            fd_schema = feature_definition.spine_schema
            if timestamp_key is not None:
                fd_schema += schema.Schema.from_dict({timestamp_key: data_types.TimestampType()})
            spine = TectonDataFrame._create_from_pandas_with_schema(spine, schema=fd_schema)
        elif isinstance(spine, str):
            spine = TectonDataFrame._create_with_snowflake_sql(spine)
        elif not isinstance(spine, TectonDataFrame):
            spine = TectonDataFrame._create(spine)
        qt = _point_in_time_get_historical_features_for_feature_definition(
            feature_definition, spine, timestamp_key, from_source
        )
    else:
        if entities is not None:
            if not isinstance(entities, TectonDataFrame):
                entities = TectonDataFrame._create(entities)
            assert set(entities._dataframe.columns).issubset(
                set(feature_definition.join_keys)
            ), f"Entities should only contain columns that can be used as Join Keys: {feature_definition.join_keys}"

        qt = _time_range_get_historical_features_for_feature_definition(
            feature_definition,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=from_source,
        )

    rewrite.MockDataRewrite(mock_data_sources).rewrite(qt)

    df = TectonDataFrame._create(qt)

    if save or save_as is not None:
        return Dataset._create(
            df=df,
            save_as=save_as,
            workspace=feature_definition.workspace,
            feature_definition_id=feature_definition.id,
            spine=spine,
            timestamp_key=timestamp_key,
        )
    return df


def _check_spine_type(spine):
    """
    Checks that the spine is a supported type for the given dialect.
    """
    if isinstance(spine, str) and sql_compat.dialect() not in (sql_compat.Dialect.SNOWFLAKE, sql_compat.Dialect.DUCKDB):
        msg = "Using SQL str as `spine` is only supported with Snowflake."
        raise TypeError(msg)


def _should_infer_timestamp_of_spine(
    feature_definition: FeatureDefinitionWrapper,
    timestamp_key: Optional[str],
):
    if feature_definition.is_on_demand:
        # If the ODFV does not depend on any materialized feature definitions, then there is no need to infer a
        # timestamp key.
        return (
            timestamp_key is None
            and utils.get_num_dependent_fv(feature_definition.pipeline.root, visited_inputs={}) > 0
        )
    else:
        return timestamp_key is None


def _point_in_time_get_historical_features_for_feature_definition(
    feature_definition: FeatureDefinitionWrapper,
    spine: TectonDataFrame,
    timestamp_key: Optional[str],
    from_source: bool,
) -> node_interface.NodeRef:
    if feature_definition.is_on_demand:
        utils.validate_spine_dataframe(spine, timestamp_key, feature_definition.request_context_keys)
    else:
        utils.validate_spine_dataframe(spine, timestamp_key)

    dac = FeatureDefinitionAndJoinConfig.from_feature_definition(feature_definition)
    user_data_node_metadata = {}
    if timestamp_key:
        user_data_node_metadata["timestamp_key"] = timestamp_key

    qt = builder.build_spine_join_querytree(
        dac,
        nodes.UserSpecifiedDataNode(spine, user_data_node_metadata).as_ref(),
        timestamp_key,
        from_source,
        use_namespace_feature_prefix=sql_compat.dialect() != sql_compat.Dialect.SNOWFLAKE,
    )

    return qt


def _most_recent_tile_end_time(fd: FeatureDefinitionWrapper, timestamp: datetime) -> int:
    """Computes the most recent tile end time which is ready to be computed.

    :param timestamp: The timestamp in python datetime format
    :return: The timestamp in seconds of the greatest ready tile end time <= timestamp.
    """
    # Account for data delay
    timestamp = timestamp - fd.max_source_data_delay
    if fd.min_scheduling_interval:
        timestamp = align_time_downwards(timestamp, fd.min_scheduling_interval)
    return convert_timestamp_to_epoch(timestamp, fd.get_feature_store_format_version)


def _time_range_get_historical_features_for_feature_definition(
    fd: FeatureDefinitionWrapper,
    entities: TectonDataFrame,
    start_time: Optional[Union[pendulum.DateTime, datetime]],
    end_time: Optional[Union[pendulum.DateTime, datetime]],
    from_source: bool,
) -> node_interface.NodeRef:
    if start_time is not None and isinstance(start_time, datetime):
        start_time = pendulum.instance(start_time)
    if end_time is not None and isinstance(end_time, datetime):
        end_time = pendulum.instance(end_time)

    if start_time is not None and fd.feature_start_timestamp is not None and start_time < fd.feature_start_timestamp:
        logger.warning(
            f'The provided start_time ({start_time}) is before "{fd.name}"\'s feature_start_time ({fd.feature_start_timestamp}). No feature values will be returned before the feature_start_time.'
        )
        start_time = fd.feature_start_timestamp

    # TODO(brian): construct the timestamps a bit more directly. This code in
    # general reuses utilities not really meant for the semantics of this API.
    if fd.is_temporal_aggregate or fd.is_temporal:
        # Feature views where materialization is not enabled may not have a feature_start_time.
        _start = start_time or fd.feature_start_timestamp or pendulum.datetime(1970, 1, 1)
        # we need to add 1 to most_recent_anchor since we filter end_time exclusively
        if end_time:
            _end = end_time
        else:
            anchor_time = _most_recent_tile_end_time(fd, pendulum.now("UTC") - fd.min_scheduling_interval)
            _end = convert_epoch_to_datetime(anchor_time, fd.get_feature_store_format_version) + pendulum.duration(
                microseconds=1
            )
    else:
        _start = start_time or pendulum.datetime(1970, 1, 1)
        _end = end_time or pendulum.now("UTC")

    if _start >= _end:
        # TODO(felix): Move this and other instances of validating user inputs to top-level get_historical_features() methods.
        raise core_errors.START_TIME_NOT_BEFORE_END_TIME(_start, _end)
    time_range = pendulum.Period(_start, _end)

    effective_timestamp_field = query_consts.EFFECTIVE_TIMESTAMP

    # TODO(felix): Move this logic to `builder.py` once it does not rely on Spark-specific time util functions.
    if fd.is_temporal or fd.is_feature_table:
        qt = builder.build_get_features(fd, from_source=from_source, feature_data_time_limits=time_range)
        qt = nodes.RenameColsNode(qt, drop=[query_consts.ANCHOR_TIME]).as_ref()
        batch_schedule_seconds = 0 if fd.is_feature_table else fd.batch_materialization_schedule.in_seconds()

        qt = nodes.AddEffectiveTimestampNode(
            qt,
            timestamp_field=fd.timestamp_key,
            effective_timestamp_name=effective_timestamp_field,
            batch_schedule_seconds=batch_schedule_seconds,
            data_delay_seconds=fd.online_store_data_delay_seconds,
            is_stream=fd.is_stream,
            is_temporal_aggregate=False,
        ).as_ref()
    else:
        feature_data_time_limits = time_utils.get_feature_data_time_limits(
            fd=fd,
            spine_time_limits=time_range,
        )
        # TODO(brian): refactor to share more with run api full aggregation
        qt = builder.build_get_full_agg_features(
            fd,
            from_source=from_source,
            feature_data_time_limits=feature_data_time_limits,
            show_effective_time=True,
        )

    # Validate that entities only contains Join Key Columns.
    if entities is not None:
        columns = list(entities.columns)
        entities_df = nodes.SelectDistinctNode(nodes.UserSpecifiedDataNode(entities).as_ref(), columns).as_ref()
        qt = nodes.JoinNode(qt, entities_df, columns, how="right").as_ref()

    qt = nodes.FeatureTimeFilterNode(
        qt,
        feature_data_time_limits=time_range,
        policy=feature_view__data_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE,
        timestamp_field=fd.timestamp_key,
    ).as_ref()

    return qt


def get_fields_list_from_tecton_schema(tecton_schema: schema_pb2.Schema) -> List[sdk_types.Field]:
    """Convert TectonSchema into a list of Tecton Fields."""
    columns_and_types = schema.Schema(tecton_schema).column_name_and_data_types()
    request_schema = []
    for c_and_t in columns_and_types:
        name = c_and_t[0]
        data_type = type_utils.sdk_type_from_tecton_type(c_and_t[1])
        request_schema.append(sdk_types.Field(name, data_type))
    return request_schema


def get_dataframe_for_data_source(
    data_source: specs.DataSourceSpec,
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    apply_translator: bool,
) -> TectonDataFrame:
    if isinstance(data_source.batch_source, (specs.SparkBatchSourceSpec, specs.PandasBatchSourceSpec)):
        if not data_source.batch_source.supports_time_filtering and (start_time or end_time):
            raise errors.DS_INCORRECT_SUPPORTS_TIME_FILTERING

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)
    elif apply_translator:
        timestamp_key = data_source.batch_source.timestamp_field
        if not timestamp_key and (start_time or end_time):
            raise errors.DS_DATAFRAME_NO_TIMESTAMP

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)
    else:
        if start_time is not None or end_time is not None:
            raise errors.DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER

        node = nodes.RawDataSourceScanNode(data_source).as_ref()
        return TectonDataFrame._create(node)
