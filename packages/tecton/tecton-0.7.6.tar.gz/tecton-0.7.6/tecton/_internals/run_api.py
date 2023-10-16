import logging
import tempfile
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas
import pendulum
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery

import tecton
from tecton._internals import errors
from tecton._internals import mock_source_utils
from tecton._internals.rewrite import MockDataRewrite
from tecton.run_api_consts import AGGREGATION_LEVEL_DISABLED
from tecton.run_api_consts import AGGREGATION_LEVEL_FULL
from tecton.run_api_consts import AGGREGATION_LEVEL_PARTIAL
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME
from tecton.run_api_consts import SUPPORTED_AGGREGATION_LEVEL_VALUES
from tecton.tecton_context import TectonContext
from tecton_core import time_utils
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.query.builder import ANCHOR_TIME
from tecton_core.query.builder import WINDOW_END_COLUMN_NAME
from tecton_core.query.builder import build_get_full_agg_features
from tecton_core.query.builder import build_materialization_querytree
from tecton_core.query.builder import build_pipeline_querytree
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import ConvertEpochToTimestampNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.sql_compat import default_case
from tecton_proto.args import pipeline_pb2
from tecton_proto.data import feature_view_pb2
from tecton_spark import materialization_plan
from tecton_spark.partial_aggregations import partial_aggregate_column_renames
from tecton_spark.pipeline_helper import get_all_input_keys
from tecton_spark.pipeline_helper import get_fco_ids_to_input_keys
from tecton_spark.pipeline_helper import run_mock_odfv_pipeline
from tecton_spark.spark_helper import check_spark_version


logger = logging.getLogger(__name__)


def maybe_warn_incorrect_time_range_size(
    fd: FeatureDefinition, start_time: datetime, end_time: datetime, aggregation_level: Optional[str]
):
    time_range = end_time - start_time
    if fd.is_temporal_aggregate:
        if fd.is_continuous:
            # There should not be any time range warnings for continuous aggregates.
            return
        slide_interval = fd.aggregate_slide_interval.ToTimedelta()
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
    elif fd.is_incremental_backfill and time_range != fd.batch_materialization_schedule:
        logger.warning(
            f"Run time range ({start_time}, {end_time}) is not equivalent to the batch_schedule: {fd.batch_materialization_schedule}. This may lead to incorrect feature values since feature views with incremental_backfills typically implicitly rely on the materialization range being equivalent to the batch_schedule."
        )


def run_batch(
    fd: FeatureDefinition,
    feature_start_time: datetime,
    feature_end_time: datetime,
    mock_data_sources: Dict[str, NodeRef],
    framework_version: FrameworkVersion,
    aggregation_level: Optional[str],
) -> "tecton.framework.data_frame.TectonDataFrame":
    if not fd.is_on_demand:
        check_spark_version(fd.fv_spec.batch_cluster_config)

    return _querytree_run_batch(
        fd=fd,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        mock_data_sources=mock_data_sources,
        framework_version=framework_version,
        aggregation_level=aggregation_level,
    )


def _build_run_batch_querytree(
    fd: FeatureDefinition,
    feature_end_time: datetime,
    feature_time_limits_aligned: pendulum.Period,
    aggregation_level: Optional[str],
) -> NodeRef:
    """Build run_batch query tree

    This assumes that inputs are validated already and is general (should not
    handle mocking data). Using mock data is considered a query tree rewrite.

    Any extra querytree nodes in this function should simply be a display-level
    modification (like field rename, type change, etc).
    """
    if fd.is_temporal:
        qt = build_materialization_querytree(fd, for_stream=False, feature_data_time_limits=feature_time_limits_aligned)
        # For a BFV, the materialization querytree is an `AddAnchorTimeNode` wrapped around exactly what we want, so we
        # just extract the input node.
        assert isinstance(qt.node, AddAnchorTimeNode)
        return qt.node.inputs[0]
    elif fd.is_temporal_aggregate:
        if aggregation_level == AGGREGATION_LEVEL_PARTIAL:
            qt = build_materialization_querytree(
                fd,
                for_stream=False,
                feature_data_time_limits=feature_time_limits_aligned,
                include_window_end_time=True,
                aggregation_anchor_time=feature_end_time,
            )
            if fd.is_continuous:
                renames = {
                    **partial_aggregate_column_renames(
                        slide_interval_string=fd.get_aggregate_slide_interval_string,
                        trailing_time_window_aggregation=fd.trailing_time_window_aggregation,
                    ),
                }
                drop = [default_case(ANCHOR_TIME)]
            else:
                # The `PartialAggNode` returned by `build_materialization_querytree` converts timestamps to epochs. We convert back
                # from epochs to timestamps since timestamps are more readable.
                qt = ConvertEpochToTimestampNode(
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
                drop = []
            return RenameColsNode(qt, mapping=renames, drop=drop).as_ref()
        elif aggregation_level == AGGREGATION_LEVEL_DISABLED:
            return build_pipeline_querytree(fd, for_stream=False, feature_data_time_limits=feature_time_limits_aligned)
        elif aggregation_level == AGGREGATION_LEVEL_FULL:
            qt = build_get_full_agg_features(
                fd,
                from_source=True,
                feature_data_time_limits=feature_time_limits_aligned,
                aggregation_anchor_time=feature_end_time,
                respect_feature_start_time=False,
            )
            return qt

    msg = "Unsupported batch query tree"
    raise Exception(msg)


def _querytree_run_batch(
    fd: FeatureDefinition,
    feature_start_time: datetime,
    feature_end_time: datetime,
    mock_data_sources: Dict[str, NodeRef],
    framework_version: FrameworkVersion,
    aggregation_level: Optional[str],
) -> "tecton.framework.data_frame.DataFrame":
    aggregation_level = validate_and_get_aggregation_level(fd, aggregation_level)

    feature_time_limits_aligned = pendulum.period(feature_start_time, feature_end_time)

    qt = _build_run_batch_querytree(fd, feature_end_time, feature_time_limits_aligned, aggregation_level)

    MockDataRewrite(mock_data_sources).rewrite(qt)

    return tecton.framework.data_frame.TectonDataFrame._create(qt)


def run_stream(fd: FeatureDefinition, output_temp_table: str) -> StreamingQuery:
    check_spark_version(fd.fv_spec.stream_cluster_config)
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
            .outputMode("update")
            .start()
        )


def run_ondemand(
    fd: FeatureDefinition, fv_name: str, mock_inputs: Dict[str, Union[Dict[str, Any], pandas.DataFrame, DataFrame]]
) -> Union[Dict[str, Any], "tecton.framework.data_frame.TectonDataFrame"]:
    for key in mock_inputs:
        if isinstance(mock_inputs[key], DataFrame):
            mock_inputs[key] = mock_inputs[key].toPandas()

    # Validate that all the mock_inputs matchs with FV inputs, and that num rows match across all mock_inputs.
    validate_ondemand_mock_inputs(mock_inputs, fd.pipeline, fd)

    # Execute ODFV pipeline to get output DataFrame.
    output = run_mock_odfv_pipeline(
        pipeline=fd.pipeline,
        transformations=fd.transformations,
        name=fv_name,
        mock_inputs=mock_inputs,
    )
    if isinstance(output, pandas.DataFrame):
        output = tecton.framework.data_frame.TectonDataFrame._create(output)

    return output


def validate_and_get_aggregation_level(fd: FeatureDefinition, aggregation_level: Optional[str]) -> str:
    # Set default aggregation_level value.
    if aggregation_level is None:
        if fd.is_temporal_aggregate:
            aggregation_level = AGGREGATION_LEVEL_FULL
        else:
            aggregation_level = AGGREGATION_LEVEL_DISABLED

    if aggregation_level not in SUPPORTED_AGGREGATION_LEVEL_VALUES:
        msg = "aggregation_level"
        raise errors.FV_INVALID_ARG_VALUE(msg, str(aggregation_level), str(SUPPORTED_AGGREGATION_LEVEL_VALUES))

    return aggregation_level


# Validate that mock_inputs keys are exact match with expected inputs.
def validate_ondemand_mock_inputs(
    mock_inputs: Dict[str, Union[Dict[str, Any], pandas.DataFrame]],
    pipeline: pipeline_pb2.Pipeline,
    odfv_fd: Optional[FeatureDefinition] = None,
):
    """Validate the mock_inputs for `run` or `test_run` match expected inputs.

    If a feature definition is passed, this will additionally check inputs against batch feature view schemas.
    """
    expected_input_names = get_all_input_keys(pipeline.root)
    mock_inputs_keys = set(mock_inputs.keys())
    if mock_inputs_keys != expected_input_names:
        raise errors.FV_INVALID_MOCK_INPUTS(list(mock_inputs_keys), list(expected_input_names))

    # Get num row for all FV mock_inputs with DF types, to validate that they match.
    input_df_row_counts = set()
    for input in mock_inputs.values():
        if isinstance(input, pandas.DataFrame):
            input_df_row_counts.add(len(input.index))
    if len(input_df_row_counts) > 1:
        raise errors.FV_INVALID_MOCK_INPUTS_NUM_ROWS(input_df_row_counts)

    # Can only validate batch feature view inputs if the schema is known
    if odfv_fd is not None:
        validate_mock_bfv_inputs_to_odfv(mock_inputs, odfv_fd)


def validate_mock_bfv_inputs_to_odfv(
    mock_inputs: Dict[str, Union[Dict[str, Any], pandas.DataFrame]], odfv_fd: FeatureDefinition
):
    """Validate the mock data used to represent batch feature view materialized data for `run()` and `test_run()`.

    Unlike other mock data checks, because there's no way for us to easily identify what features are needed in the
    ODFV, we expect all features in the upstream BFV to be present.
    """
    from tecton_core import feature_set_config

    # Extract input names (from pipeline) and map to feature view schemas (from FDW)
    dependent_fvs = feature_set_config.find_dependent_feature_set_items(
        odfv_fd.fco_container, odfv_fd.pipeline.root, visited_inputs={}, fv_id=odfv_fd.id
    )
    fv_ids_to_fvs = {fv.feature_definition.id: fv for fv in dependent_fvs}
    fco_ids_to_input_keys = get_fco_ids_to_input_keys(odfv_fd.pipeline.root)
    input_name_to_features = {}
    for fv_id, fv in fv_ids_to_fvs.items():
        input_name = fco_ids_to_input_keys[fv_id]
        input_name_to_features[input_name] = fv.features

    # Validate some required fields in the mock data schemas.
    for key, mock_df in mock_inputs.items():
        if key not in input_name_to_features:
            continue
        input_columns = mock_source_utils.get_pandas_or_spark_df_or_dict_columns(mock_df)
        # Check columns match BFV
        dependent_columns = input_name_to_features[key]
        unexpected_columns = [col for col in input_columns if col not in dependent_columns]
        if len(unexpected_columns) > 0:
            msg = f"Unexpected columns: {unexpected_columns} found in mock inputs. Expected columns from the Feature View {key}, such as: '{dependent_columns}'"
            raise TectonValidationError(msg)
        missing_columns = [col for col in dependent_columns if col not in input_columns]
        if len(missing_columns) > 0:
            logger.warning(
                f"ODFV {odfv_fd.name} has a dependency on the Feature View {key}. Features '{missing_columns}' of this "
                f"Feature View are not found. Available columns: '{input_columns}'"
            )


def _get_ds_by_id(data_sources, id: str):
    for ds in data_sources:
        if ds.id == id:
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
