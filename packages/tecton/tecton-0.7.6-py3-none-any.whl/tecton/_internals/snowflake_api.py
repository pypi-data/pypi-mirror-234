import typing
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas
import pendulum

from tecton._internals.mock_source_utils import validate_batch_mock_inputs
from tecton.framework.data_frame import TectonDataFrame
from tecton.snowflake_context import SnowflakeContext
from tecton_core import conf
from tecton_core import schema_derivation_utils as core_schema_derivation_utils
from tecton_core import specs
from tecton_core.errors import TectonSnowflakeNotImplementedError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_core.time_utils import get_timezone_aware_datetime
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_snowflake import schema_derivation_utils
from tecton_snowflake import sql_helper


if typing.TYPE_CHECKING:
    import snowflake.snowpark


def get_historical_features(
    feature_set_config: FeatureSetConfig,
    spine: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, TectonDataFrame, str]] = None,
    timestamp_key: Optional[str] = None,
    include_feature_view_timestamp_columns: bool = False,
    from_source: Optional[bool] = None,
    save: bool = False,
    save_as: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    entities: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, TectonDataFrame]] = None,
    append_prefix: bool = True,  # Whether to append the prefix to the feature column name
) -> TectonDataFrame:
    # TODO(TEC-6991): Dataset doesn't really work with snowflake as it has spark dependency.
    # Need to rewrite it with snowflake context or remove this param for snowflake.
    if save or save_as is not None:
        msg = "save is not supported for Snowflake"
        raise TectonSnowflakeNotImplementedError(msg)

    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
        if entities is not None:
            # Convert entities to a snowflake dataframe
            if isinstance(entities, pandas.DataFrame):
                entities = TectonDataFrame._create(entities).to_snowpark()()
            elif isinstance(entities, TectonDataFrame):
                entities = entities.to_snowpark()()

        return TectonDataFrame._create_with_snowflake(
            sql_helper.get_historical_features_with_snowpark(
                spine=spine,
                session=SnowflakeContext.get_instance().get_session(),
                timestamp_key=timestamp_key,
                feature_set_config=feature_set_config,
                include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                append_prefix=append_prefix,
                from_source=from_source,
            )
        )
    else:
        if timestamp_key is None and spine is not None:
            msg = "timestamp_key must be specified using Snowflake without Snowpark"
            raise TectonSnowflakeNotImplementedError(msg)
        if entities is not None:
            msg = "entities is only supported for Snowflake with Snowpark enabled"
            raise TectonSnowflakeNotImplementedError(msg)
        return TectonDataFrame._create(
            sql_helper.get_historical_features(
                spine=spine,
                connection=SnowflakeContext.get_instance().get_connection(),
                timestamp_key=timestamp_key,
                feature_set_config=feature_set_config,
                include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
                start_time=start_time,
                end_time=end_time,
                append_prefix=append_prefix,
                from_source=from_source,
            )
        )


def run_batch(
    fd: FeatureDefinition,
    mock_inputs: Dict[str, pandas.DataFrame],
    feature_start_time: datetime,
    feature_end_time: datetime,
    aggregation_level: Optional[str],
) -> TectonDataFrame:
    validate_batch_mock_inputs(mock_inputs, fd)
    mock_sql_inputs = None

    feature_start_time = get_timezone_aware_datetime(feature_start_time)
    feature_end_time = get_timezone_aware_datetime(feature_end_time)

    if fd.is_temporal_aggregate:
        for feature in fd.fv_spec.aggregate_features:
            aggregate_function = sql_helper.AGGREGATION_PLANS[feature.function]
            if not aggregate_function:
                msg = f"Unsupported aggregation function {feature.function} in snowflake pipeline"
                raise TectonSnowflakeNotImplementedError(msg)

    session = None
    connection = None
    if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
        session = SnowflakeContext.get_instance().get_session()
    else:
        connection = SnowflakeContext.get_instance().get_connection()

    if mock_inputs:
        mock_sql_inputs = {
            key: sql_helper.generate_sql_table_from_pandas_df(
                df=df, session=session, connection=connection, table_name=f"_TT_TEMP_INPUT_{key.upper()}_TABLE"
            )
            for (key, df) in mock_inputs.items()
        }

    # Validate input start and end times. Set defaults if None.
    sql_str = sql_helper.generate_run_batch_sql(
        feature_definition=fd,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        aggregation_level=aggregation_level,
        mock_sql_inputs=mock_sql_inputs,
        materialization_context=BoundMaterializationContext._create_internal(
            pendulum.instance(feature_start_time),
            pendulum.instance(feature_end_time),
            fd.fv_spec.batch_schedule,
        ),
        session=session,
        from_source=True,  # For run() we don't use materialized data
    )
    if session is not None:
        return TectonDataFrame._create_with_snowflake(session.sql(sql_str))
    else:
        cur = connection.cursor()
        cur.execute(sql_str, _statement_params={"SF_PARTNER": "tecton-ai"})
        return TectonDataFrame._create(cur.fetch_pandas_all())


def get_dataframe_for_data_source(
    data_source: specs.DataSourceSpec,
    start_time: datetime = None,
    end_time: datetime = None,
) -> TectonDataFrame:
    if not conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
        msg = "get_dataframe is only supported with Snowpark enabled"
        raise TectonSnowflakeNotImplementedError(msg)

    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    session = SnowflakeContext.get_instance().get_session()
    return TectonDataFrame._create_with_snowflake(
        sql_helper.get_dataframe_for_data_source(session, data_source.batch_source, start_time, end_time)
    )


# For notebook driven development
def derive_batch_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
) -> spark_schema_pb2.SparkSchema:
    if not ds_args.HasField("snowflake_ds_config"):
        msg = f"Invalid batch source args: {ds_args}"
        raise ValueError(msg)

    connection = SnowflakeContext.get_instance().get_connection()
    return schema_derivation_utils.get_snowflake_schema(ds_args, connection)


def derive_view_schema_for_feature_view(
    feature_view_args: feature_view__args_pb2.FeatureViewArgs,
    transformation_specs: List[specs.TransformationSpec],
    data_source_specs: List[specs.DataSourceSpec],
) -> schema_pb2.Schema:
    connection = SnowflakeContext.get_instance().get_connection()
    session = None
    if conf.get_bool("ALPHA_SNOWFLAKE_SNOWPARK_ENABLED"):
        session = SnowflakeContext.get_instance().get_session()

    return schema_derivation_utils.get_feature_view_view_schema(
        feature_view_args, transformation_specs, data_source_specs, connection, session
    )


def derive_materialization_schema_for_feature_view(
    view_schema: schema_pb2.Schema,
    feature_view_args: feature_view__args_pb2.FeatureViewArgs,
) -> schema_pb2.Schema:
    is_aggregate = len(feature_view_args.materialized_feature_view_args.aggregations) > 0
    if not is_aggregate:
        return view_schema

    materialization_schema = core_schema_derivation_utils.compute_aggregate_materialization_schema_from_view_schema(
        view_schema, feature_view_args, is_spark=False
    )

    # Make column name uppercase.
    for column in materialization_schema.columns:
        column.name = column.name.upper()
    return materialization_schema
