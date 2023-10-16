import tempfile
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import pandas
import pendulum
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery

import tecton
from tecton._internals import errors
from tecton._internals.feature_views.aggregations import construct_full_tafv_df
from tecton._internals.rewrite import MockDataRewrite
from tecton.run_api_consts import AGGREGATION_LEVEL_DISABLED
from tecton.run_api_consts import AGGREGATION_LEVEL_FULL
from tecton.run_api_consts import AGGREGATION_LEVEL_PARTIAL
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME
from tecton.run_api_consts import SUPPORTED_AGGREGATION_LEVEL_VALUES
from tecton.tecton_context import TectonContext
from tecton_core import conf
from tecton_core import logger as logger_lib
from tecton_core import time_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.id_helper import IdHelper
from tecton_core.query.builder import ANCHOR_TIME
from tecton_core.query.builder import build_get_full_agg_features
from tecton_core.query.builder import build_pipeline_querytree
from tecton_core.query.builder import build_run_querytree
from tecton_core.query.builder import WINDOW_END_COLUMN_NAME
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import ConvertEpochToTimestamp
from tecton_core.query.nodes import DataNode
from tecton_core.query.nodes import RenameColsNode
from tecton_proto.args.feature_view_pb2 import BackfillConfigMode
from tecton_proto.data import feature_view_pb2
from tecton_spark import materialization_plan
from tecton_spark.partial_aggregations import construct_partial_time_aggregation_df
from tecton_spark.partial_aggregations import partial_aggregate_column_renames
from tecton_spark.partial_aggregations import rename_partial_aggregate_columns
from tecton_spark.pipeline_helper import get_all_input_ds_id_map
from tecton_spark.pipeline_helper import get_all_input_keys
from tecton_spark.pipeline_helper import pipeline_to_dataframe
from tecton_spark.pipeline_helper import run_mock_odfv_pipeline
from tecton_spark.spark_helper import check_spark_version
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper

logger = logger_lib.get_logger("InteractiveRunApi")


def resolve_times(
    fd: FeatureDefinition,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    aggregation_level: str,
    framework_version: FrameworkVersion,
) -> Tuple[datetime, datetime, pendulum.Period]:
    fv_proto = fd.feature_view_proto

    schedule_interval = fd.min_scheduling_interval

    if framework_version == FrameworkVersion.FWV5:
        # If feature_start_time and/or feature_end_time time is missing, default to one schedule_interval.
        if feature_start_time is None and feature_end_time is None:
            # If both timestamp are missing, align to the most recent, complete schedule interval aligned with the
            # epoch. This is a realistic materialization period.
            feature_end_time = time_utils.align_time_downwards(datetime.now(), schedule_interval)
            feature_start_time = time_utils.align_time_downwards(datetime.now() - schedule_interval, schedule_interval)
        elif feature_start_time is None:
            feature_start_time = feature_end_time - schedule_interval
        elif feature_end_time is None:
            feature_end_time = feature_start_time + schedule_interval

        if feature_end_time <= feature_start_time:
            raise errors.END_TIME_BEFORE_START_TIME(feature_start_time, feature_end_time)

        _warn_incorrect_time_range_size(fd, feature_start_time, feature_end_time, aggregation_level)

        return feature_start_time, feature_end_time, pendulum.period(feature_start_time, feature_end_time)

    # Smart default feature_start_time and feature_end_time if unset.
    if feature_end_time is None:
        feature_end_time = pendulum.now()
    if feature_start_time is None:
        feature_start_time = feature_end_time - schedule_interval

    if isinstance(feature_start_time, pendulum.DateTime):
        feature_start_time = datetime.utcfromtimestamp(feature_start_time.timestamp())
    if isinstance(feature_end_time, pendulum.DateTime):
        feature_end_time = datetime.utcfromtimestamp(feature_end_time.timestamp())

    # If doing a "full" aggregation, move back the feature_start_time by the
    # duration to ensure we have enough data.
    if aggregation_level == AGGREGATION_LEVEL_FULL:
        max_aggregation = max((f.window.seconds for f in fd.trailing_time_window_aggregation.features))
        first_tile_time = feature_start_time - pendulum.duration(seconds=max_aggregation)
        feature_time_limits_aligned = _align_times(first_tile_time, feature_end_time, fv_proto, schedule_interval)
    else:
        feature_time_limits_aligned = _align_times(feature_start_time, feature_end_time, fv_proto, schedule_interval)

    _validate_feature_time_for_backfill_config(
        fv_proto, feature_start_time, feature_end_time, feature_time_limits_aligned
    )

    return feature_start_time, feature_end_time, feature_time_limits_aligned


def _warn_incorrect_time_range_size(
    fd: FeatureDefinition, start_time: datetime, end_time: datetime, aggregation_level: Optional[str]
):
    fv_proto = fd.feature_view_proto
    time_range = end_time - start_time
    if fd.is_temporal_aggregate:
        if fd.is_continuous_temporal_aggregate:
            # There should not be any time range warnings for continuous aggregates.
            return
        slide_interval = fv_proto.temporal_aggregate.slide_interval.ToTimedelta()
        if aggregation_level == AGGREGATION_LEVEL_FULL:
            max_aggregation = max((f.window.ToTimedelta() for f in fd.trailing_time_window_aggregation.features))
            if time_range < max_aggregation:
                logger.warning(
                    f"Run time range ({start_time}, {end_time}) is smaller than the maximum aggregation size: {max_aggregation}. This may lead to incorrect aggregate feature values."
                )
            if time_range.total_seconds() % slide_interval.total_seconds() != 0:
                logger.warning(
                    f"Run time range ({start_time}, {end_time}) is not a multiple of the aggregation_interval: {slide_interval}. This may lead to incorrect aggregate feature values, since Tecton pre-aggregates data in smaller time windows based on the aggregation_interval size."
                )
        elif aggregation_level == AGGREGATION_LEVEL_PARTIAL:
            if time_range.total_seconds() % slide_interval.total_seconds() != 0:
                logger.warning(
                    f"Run time range ({start_time}, {end_time}) is not a multiple of the aggregation_interval: {slide_interval}. This may lead to incorrect aggregate feature values, since Tecton pre-aggregates data in smaller time windows based on the aggregation_interval size."
                )
    elif fd.is_incremental_backfill and time_range != fd.min_scheduling_interval:
        logger.warning(
            f"Run time range ({start_time}, {end_time}) is not equivalent to the batch_schedule: {fd.min_scheduling_interval}. This may lead to incorrect feature values since feature views with incremental_backfills typically implicitly rely on the materialization range being equivalent to the batch_schedule."
        )


def run_batch(
    fd: FeatureDefinition,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]],
    framework_version: FrameworkVersion,
    aggregate_tiles: Optional[bool] = None,
    aggregation_level: Optional[str] = None,
) -> "tecton.interactive.data_frame.TectonDataFrame":
    check_spark_version(fd.fv.materialization_params.batch_materialization)
    if conf.get_bool("QUERYTREE_ENABLED"):
        return _querytree_run_batch(
            fd=fd,
            feature_start_time=feature_start_time,
            feature_end_time=feature_end_time,
            mock_inputs=mock_inputs,
            framework_version=framework_version,
            aggregate_tiles=aggregate_tiles,
            aggregation_level=aggregation_level,
        )

    return _legacy_run_batch(
        fd=fd,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        mock_inputs=mock_inputs,
        framework_version=framework_version,
        aggregate_tiles=aggregate_tiles,
        aggregation_level=aggregation_level,
    )


def _build_run_batch_querytree(
    fd: FeatureDefinition,
    feature_end_time: datetime,
    feature_time_limits_aligned: pendulum.Period,
    aggregation_level: Optional[str],
) -> "tecton.interactive.data_frame.TectonDataFrame":
    """Build run_batch query tree

    This assumes that inputs are validated already and is general (should not
    handle mocking data). Using mock data is considered a query tree rewrite.

    Any extra querytree nodes in this function should simply be a display-level
    modification (like field rename, type change, etc).
    """
    spark = TectonContext.get_instance()._spark
    fv_proto = fd.feature_view_proto
    if fd.is_temporal:
        # Standard materialization run querytree
        qt = build_run_querytree(fd, for_stream=False, feature_data_time_limits=feature_time_limits_aligned)
        return RenameColsNode(qt, {ANCHOR_TIME: None}).as_ref()
    elif fd.is_temporal_aggregate:
        if aggregation_level == AGGREGATION_LEVEL_PARTIAL:
            # Standard materialization run querytree
            qt = build_run_querytree(
                fd,
                for_stream=False,
                feature_data_time_limits=feature_time_limits_aligned,
                include_window_end_time=True,
                aggregation_anchor_time=feature_end_time,
            )
            if fd.is_continuous_temporal_aggregate:
                renames = {
                    ANCHOR_TIME: None,
                    **partial_aggregate_column_renames(
                        slide_interval_string=fd.get_aggregate_slide_interval_string,
                        trailing_time_window_aggregation=fd.trailing_time_window_aggregation,
                    ),
                }
            else:
                qt = ConvertEpochToTimestamp(
                    qt, {col: fd.get_feature_store_format_version for col in (ANCHOR_TIME, WINDOW_END_COLUMN_NAME)}
                ).as_ref()
                renames = {
                    ANCHOR_TIME: DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME,
                    WINDOW_END_COLUMN_NAME: DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME,
                    **partial_aggregate_column_renames(
                        slide_interval_string=fd.get_aggregate_slide_interval_string,
                        trailing_time_window_aggregation=fd.trailing_time_window_aggregation,
                    ),
                }
            return RenameColsNode(qt, renames).as_ref()
        elif aggregation_level == AGGREGATION_LEVEL_DISABLED:
            return build_pipeline_querytree(fd, for_stream=False, feature_data_time_limits=feature_time_limits_aligned)
        elif aggregation_level == AGGREGATION_LEVEL_FULL:
            qt = build_get_full_agg_features(
                fd,
                spine=None,
                from_source=True,
                feature_data_time_limits=feature_time_limits_aligned,
                respect_feature_start_time=False,
                aggregation_anchor_time=feature_end_time,
            )
            qt = ConvertEpochToTimestamp(qt, {ANCHOR_TIME: fd.get_feature_store_format_version}).as_ref()
            return RenameColsNode(qt, {ANCHOR_TIME: fd.trailing_time_window_aggregation.time_key}).as_ref()

    raise Exception("Unsupported batch query tree")


def _querytree_run_batch(
    fd: FeatureDefinition,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]],
    framework_version: FrameworkVersion,
    aggregate_tiles: Optional[bool] = None,
    aggregation_level: Optional[str] = None,
) -> "tecton.interactive.data_frame.DataFrame":
    fv_proto = fd.feature_view_proto
    aggregation_level = validate_and_get_aggregation_level(fd, aggregate_tiles, aggregation_level)

    # Validate that mock_inputs' keys.
    validate_batch_mock_inputs_keys(mock_inputs, fv_proto)

    feature_start_time, feature_end_time, feature_time_limits_aligned = resolve_times(
        fd, feature_start_time, feature_end_time, aggregation_level, framework_version
    )

    qt = _build_run_batch_querytree(fd, feature_end_time, feature_time_limits_aligned, aggregation_level)

    input_ds_id_map = get_all_input_ds_id_map(fd.pipeline.root)
    mock_data_sources = {input_ds_id_map[key]: NodeRef(DataNode(mock_inputs[key])) for key in mock_inputs.keys()}
    MockDataRewrite(mock_data_sources).rewrite(qt)

    return tecton.interactive.data_frame.TectonDataFrame._create(qt)


def _legacy_run_batch(
    fd: FeatureDefinition,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]],
    framework_version: FrameworkVersion,
    aggregate_tiles: Optional[bool] = None,
    aggregation_level: Optional[str] = None,
) -> "tecton.interactive.data_frame.TectonDataFrame":
    fv_proto = fd.feature_view_proto
    spark = TectonContext.get_instance()._spark
    aggregation_level = validate_and_get_aggregation_level(fd, aggregate_tiles, aggregation_level)

    # Validate that mock_inputs' keys.
    input_ds_id_map = get_all_input_ds_id_map(fd.pipeline.root)
    validate_batch_mock_inputs_keys(mock_inputs, fv_proto)

    feature_start_time, feature_end_time, feature_time_limits_aligned = resolve_times(
        fd, feature_start_time, feature_end_time, aggregation_level, framework_version
    )

    # Convert any Pandas dataFrame mock_inputs to Spark, validate schema columns.
    # TODO(raviphol): Consider refactor this under pipeline_helper._node_to_value
    data_sources = fd.data_sources
    for key in mock_inputs.keys():
        ds = _get_ds_by_id(data_sources, input_ds_id_map[key])
        spark_schema = _get_spark_schema(ds)

        if isinstance(mock_inputs[key], pandas.DataFrame):
            mock_inputs[key] = spark.createDataFrame(mock_inputs[key])

        _validate_input_dataframe_schema(input_name=key, dataframe=mock_inputs[key], spark_schema=spark_schema)

    # Execute Spark pipeline to get output DataFrame.
    materialized_spark_df = pipeline_to_dataframe(
        spark,
        pipeline=fd.pipeline,
        consume_streaming_data_sources=False,
        data_sources=data_sources,
        transformations=fd.transformations,
        feature_time_limits=feature_time_limits_aligned,
        schedule_interval=pendulum.Duration(seconds=fv_proto.materialization_params.schedule_interval.ToSeconds()),
        passed_in_inputs=mock_inputs,
    )

    is_fwv5 = framework_version == FrameworkVersion.FWV5
    if is_fwv5:
        # Filter the unaggregated pipeline output. This matches the logic used during materialization.
        materialized_spark_df = materialized_spark_df.filter(
            (materialized_spark_df[fd.timestamp_key] >= feature_start_time)
            & (materialized_spark_df[fd.timestamp_key] < feature_end_time)
        )

    if aggregation_level == "partial":
        # Aggregate the output rows into corresponding aggregate-tiles.
        materialized_spark_df = construct_partial_time_aggregation_df(
            df=materialized_spark_df,
            join_keys=fd.join_keys,
            time_aggregation=fd.trailing_time_window_aggregation,
            version=fv_proto.feature_store_format_version,
            window_start_column_name=DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME,
            window_end_column_name=DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME,
            convert_to_epoch=False,
            aggregation_anchor_time=feature_end_time if is_fwv5 else None,
        )
        if fd.is_continuous_temporal_aggregate:
            # Drop the anchor time, it's redundant with the `timestamp` column and doesn't need to be user facing.
            materialized_spark_df = materialized_spark_df.drop("_anchor_time")

        # Intermediate-rollup output columns will be renamed to use the similar pattern as final aggregated columns.
        materialized_spark_df = rename_partial_aggregate_columns(
            df=materialized_spark_df,
            slide_interval_string=fd.get_aggregate_slide_interval_string,
            trailing_time_window_aggregation=fd.trailing_time_window_aggregation,
        )
    elif aggregation_level == AGGREGATION_LEVEL_FULL:
        # Aggregate the output rows into corresponding aggregate-tiles.
        materialized_spark_df = construct_partial_time_aggregation_df(
            df=materialized_spark_df,
            join_keys=fd.join_keys,
            time_aggregation=fd.trailing_time_window_aggregation,
            version=fv_proto.feature_store_format_version,
            aggregation_anchor_time=feature_end_time if is_fwv5 else None,
        )
        # Perform final rollup from aggregate tiles up to each result window.
        materialized_spark_df = construct_full_tafv_df(
            spark=spark,
            time_aggregation=fd.trailing_time_window_aggregation,
            join_keys=fd.join_keys,
            feature_store_format_version=fv_proto.feature_store_format_version,
            tile_interval=fd.get_tile_interval,
            all_partial_aggregations_df=materialized_spark_df,
            use_materialized_data=False,
        )

    # Partial aggregation does not have a timestamp column.
    if aggregation_level != "partial" and not is_fwv5:
        # Filter output rows which are not within feature time range.
        materialized_spark_df = materialized_spark_df.filter(
            materialized_spark_df[fd.timestamp_key] >= feature_start_time
        )
        materialized_spark_df = materialized_spark_df.filter(materialized_spark_df[fd.timestamp_key] < feature_end_time)

    return tecton.interactive.data_frame.TectonDataFrame._create(materialized_spark_df)


def run_stream(fd: FeatureDefinition, output_temp_table: str) -> StreamingQuery:
    check_spark_version(fd.fv.materialization_params.stream_materialization)
    plan = materialization_plan.get_stream_materialization_plan(
        spark=TectonContext.get_instance()._spark,
        feature_definition=fd,
    )
    spark_df = plan.online_store_data_frame
    with tempfile.TemporaryDirectory() as d:
        return (
            spark_df.writeStream.format("memory")
            .queryName(output_temp_table)
            .option("checkpointLocation", d)
            .outputMode("append")
            .start()
        )


def run_ondemand(
    fd: FeatureDefinition, fv_name: str, mock_inputs: Dict[str, Union[Dict[str, Any], pandas.DataFrame, DataFrame]]
) -> Union[Dict[str, Any], "tecton.interactive.data_frame.TectonDataFrame"]:
    fv_proto = fd.feature_view_proto
    for key in mock_inputs:
        if isinstance(mock_inputs[key], DataFrame):
            mock_inputs[key] = mock_inputs[key].toPandas()

    # Validate that all the mock_inputs matchs with FV inputs, and that num rows match across all mock_inputs.
    validate_ondemand_mock_inputs_keys(mock_inputs, fv_proto)

    # Execute ODFV pipeline to get output DataFrame.
    output = run_mock_odfv_pipeline(
        pipeline=fd.pipeline,
        transformations=fd.transformations,
        name=fv_name,
        mock_inputs=mock_inputs,
    )
    if isinstance(output, pandas.DataFrame):
        output = tecton.interactive.data_frame.TectonDataFrame._create(output)

    return output


def validate_and_get_aggregation_level(
    fd: FeatureDefinition, aggregate_tiles: Optional[bool], aggregation_level: Optional[str]
) -> str:
    if aggregate_tiles is not None:
        if aggregation_level:
            raise errors.FV_INVALID_ARG_COMBO(["aggregate_tiles", "aggregation_level"])
        logger.warning("aggregate_tiles is deprecated - please use aggregation_level instead.")
        aggregation_level = AGGREGATION_LEVEL_PARTIAL if aggregate_tiles else AGGREGATION_LEVEL_DISABLED

    # Set default aggregation_level value.
    if aggregation_level is None:
        if fd.is_temporal_aggregate and not fd.trailing_time_window_aggregation.is_continuous:
            aggregation_level = AGGREGATION_LEVEL_FULL
        else:
            aggregation_level = AGGREGATION_LEVEL_DISABLED

    if aggregation_level not in SUPPORTED_AGGREGATION_LEVEL_VALUES:
        raise errors.FV_INVALID_ARG_VALUE(
            "aggregation_level", str(aggregation_level), str(SUPPORTED_AGGREGATION_LEVEL_VALUES)
        )

    return aggregation_level


# For single-batch-schedule-interval-per-job backfill, validate the followings.
# - Only support single-tile run.
# - Don't allow passing `feature_start_time` without feature_end_time since it may be confusing that the tile time
#   range goes into the future.
def _validate_feature_time_for_backfill_config(
    fv_proto: feature_view_pb2.FeatureView,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_time_limits_aligned: pendulum.Period,
):
    # TODO(raviphol): Use is_incremental_backfill once D9614 is landed.
    if not fv_proto.HasField("temporal"):
        return
    if not fv_proto.temporal.HasField("backfill_config"):
        return
    backfill_config_mode = fv_proto.temporal.backfill_config.mode
    if backfill_config_mode is not BackfillConfigMode.BACKFILL_CONFIG_MODE_SINGLE_BATCH_SCHEDULE_INTERVAL_PER_JOB:
        return

    if feature_start_time and not feature_end_time:
        raise errors.BFC_MODE_SINGLE_REQUIRED_FEATURE_END_TIME_WHEN_START_TIME_SET

    schedule_interval_seconds = fv_proto.materialization_params.schedule_interval.ToSeconds()
    if schedule_interval_seconds == 0:
        raise errors.INTERNAL_ERROR("Materialization schedule interval not found.")

    num_tile = feature_time_limits_aligned.in_seconds() // schedule_interval_seconds
    if num_tile > 1:
        raise errors.BFC_MODE_SINGLE_INVALID_FEATURE_TIME_RANGE


# Validate that mock_inputs keys are a subset of data sources.
def validate_batch_mock_inputs_keys(mock_inputs, fv_proto):
    expected_input_names = get_all_input_keys(fv_proto.pipeline.root)
    mock_inputs_keys = set(mock_inputs.keys())
    if not mock_inputs_keys.issubset(expected_input_names):
        raise errors.FV_INVALID_MOCK_INPUTS(mock_inputs_keys, expected_input_names)


# Validate that mock_inputs keys are exact match with expected inputs.
def validate_ondemand_mock_inputs_keys(
    mock_inputs: Dict[str, Union[Dict[str, Any], pandas.DataFrame]],
    fv_proto: feature_view_pb2.FeatureView,
):
    expected_input_names = get_all_input_keys(fv_proto.pipeline.root)
    mock_inputs_keys = set(mock_inputs.keys())
    if mock_inputs_keys != expected_input_names:
        raise errors.FV_INVALID_MOCK_INPUTS(mock_inputs_keys, expected_input_names)

    # Get num row for all FV mock_inputs with DF types, to validate that they match.
    input_df_row_counts = set()
    for input in mock_inputs.values():
        if isinstance(input, pandas.DataFrame):
            input_df_row_counts.add(len(input.index))
    if len(input_df_row_counts) > 1:
        raise errors.FV_INVALID_MOCK_INPUTS_NUM_ROWS(input_df_row_counts)


# Check that schema of each mock inputs matches with data sources.
def _validate_input_dataframe_schema(input_name, dataframe: DataFrame, spark_schema):
    columns = sorted(dataframe.columns)
    expected_column_names = sorted([field.name for field in spark_schema.fields])

    # Validate mock input's schema against expected schema.
    if not expected_column_names == columns:
        raise errors.FV_INVALID_MOCK_INPUT_SCHEMA(input_name, set(columns), set(expected_column_names))


def _get_ds_by_id(data_sources, id: str):
    for ds in data_sources:
        if IdHelper.to_string(ds.virtual_data_source_id) == id:
            return ds
    return None


# Align feature start and end times with materialization schedule interval.
def _align_times(
    feature_start_time: datetime,
    feature_end_time: datetime,
    fv_proto: feature_view_pb2.FeatureView,
    schedule_interval: timedelta,
) -> pendulum.Period:
    # Align feature_end_time upward to the nearest materialization schedule interval.
    feature_end_time = time_utils.align_time_upwards(feature_end_time, schedule_interval)

    # Align feature_start_time downward to the nearest materialization schedule interval.
    feature_start_time = time_utils.align_time_downwards(feature_start_time, schedule_interval)
    return pendulum.period(feature_start_time, feature_end_time)


def _get_spark_schema(ds):
    if ds.HasField("batch_data_source"):
        spark_schema = ds.batch_data_source.spark_schema
    elif ds.HasField("stream_data_source"):
        spark_schema = ds.stream_data_source.spark_schema
    else:
        raise errors.INTERNAL_ERROR("DataSource is missing a supporting config")
    return SparkSchemaWrapper.from_proto(spark_schema).unwrap()
