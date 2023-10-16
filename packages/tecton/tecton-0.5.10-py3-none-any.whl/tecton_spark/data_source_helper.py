"""Helper module for creating spark data source operations such as creating DataFrames and
registering temp views. Methods within this class should exclusively operate on proto
representations of the data model.
"""
import json
import os
import time
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

import pendulum
from pyspark.sql import DataFrame
from pyspark.sql import functions
from pyspark.sql import SparkSession
from pyspark.sql.functions import coalesce
from pyspark.sql.functions import to_timestamp
from pyspark.sql.types import ArrayType
from pyspark.sql.types import DateType
from pyspark.sql.types import MapType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType

import tecton_spark.errors_spark
from tecton_core import conf
from tecton_core import function_deserialization
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.filter_context import FilterContext
from tecton_core.id_helper import IdHelper
from tecton_proto.args.data_source_config_pb2 import INITIAL_STREAM_POSITION_LATEST
from tecton_proto.args.data_source_config_pb2 import INITIAL_STREAM_POSITION_TRIM_HORIZON
from tecton_proto.args.data_source_config_pb2 import INITIAL_STREAM_POSITION_UNSPECIFIED
from tecton_proto.data.batch_data_source_pb2 import BatchDataSource
from tecton_proto.data.batch_data_source_pb2 import FileDataSourceFormat
from tecton_proto.data.stream_data_source_pb2 import StreamDataSource
from tecton_proto.data.virtual_data_source_pb2 import VirtualDataSource
from tecton_spark.data_source_credentials import get_kafka_secrets
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper

INITIAL_STREAM_POSITION_STR_TO_ENUM = {
    "latest": INITIAL_STREAM_POSITION_LATEST,
    "trim_horizon": INITIAL_STREAM_POSITION_TRIM_HORIZON,
}

INITIAL_STREAM_POSITION_ENUM_TO_STR: Dict[str, Optional[str]] = {
    v: k for k, v in INITIAL_STREAM_POSITION_STR_TO_ENUM.items()
}
INITIAL_STREAM_POSITION_ENUM_TO_STR[INITIAL_STREAM_POSITION_UNSPECIFIED] = None

KAFKA_DEFAULT_MAX_OFFSETS_PER_TRIGGER = 100000

KAFKA_STARTING_OFFSET_CONFIG_KEYS = {"startingOffsetsByTimestamp", "startingOffsets"}

# Set of temporal Kafka consumer settings that will be set by the environment variables set in the
# cluster's `textproto` files.
#
# Defines maximum number of records (across all partitions) from Kafka to be consumed by a micro-batch.
KAFKA_MAX_OFFSETS_PER_TRIGGER_ENV = "KAFKA_MAX_OFFSETS_PER_TRIGGER"
# Option to set starting timestamps for each Kafka partitions so that all of the Kafka's retention
# data is not processed. It's only relevant for the fist streaming job before the checkpoint exists on S3.
KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV = "KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST"
# Only necessary when KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV is set.
KAFKA_NUM_PARTITIONS_ENV = "KAFKA_NUM_PARTITIONS"


def _is_running_on_emr() -> bool:
    import os

    return "EMR_RELEASE_LABEL" in os.environ


def _validate_data_source_proto(data_source: BatchDataSource):
    if data_source.HasField("hive_table"):
        assert data_source.hive_table.HasField("database"), "Invalid HiveTableDataSource: no database provided"
        assert data_source.hive_table.HasField("table"), "Invalid HiveTableDataSource: no table provided"
    elif data_source.HasField("file"):
        pass
    elif data_source.HasField("redshift_db"):
        redshift = data_source.redshift_db
        assert redshift.HasField("endpoint"), "Invalid RedshiftDataSource: no endpoint provided"
        assert redshift.HasField("table") or redshift.HasField(
            "query"
        ), "Invalid RedshiftDataSource: no table or query provided"
    elif data_source.HasField("snowflake"):
        snowflake = data_source.snowflake.snowflakeArgs
        required_args = ["url", "database", "schema", "warehouse"]
        for arg in required_args:
            assert snowflake.HasField(arg), f"Invalid SnowflakeDataSource: no {arg} provided"
        assert snowflake.HasField("table") or snowflake.HasField(
            "query"
        ), "Invalid SnowflakeDataSource: no table or query provided"
    else:
        assert False, "BatchDataSource must set hive_table, file, redshift_db, or snowflake"


def _get_raw_hive_table_dataframe(spark: SparkSession, database: str, table: str) -> DataFrame:
    spark.sql("USE {}".format(database))
    return spark.table(table)


def get_non_dsf_raw_dataframe(
    spark: SparkSession, data_source: BatchDataSource, called_for_schema_computation=False
) -> DataFrame:
    """Returns a DataFrame of the raw, untranslated data defined by the given BatchDataSource proto.

    :param spark: Spark session.
    :param data_source: BatchDataSource proto. BatchDataSource must not be a data source function (spark_batch_config).
    :param called_for_schema_computation: If set, optimizations are applied for faster schema computations.
                                          i.e. FileDSConfig.schema_uri is used to avoid expensive partition discovery.

    :return: The DataFrame for the raw data.
    """

    assert not is_data_source_function(
        data_source
    ), "get_raw_dataframe can not be used with data source function (spark_batch_config)."

    _validate_data_source_proto(data_source)
    if data_source.HasField("hive_table"):
        df = _get_raw_hive_table_dataframe(spark, data_source.hive_table.database, data_source.hive_table.table)
    elif data_source.HasField("redshift_db"):
        df = get_redshift_dataframe(
            spark,
            data_source.redshift_db.endpoint,
            data_source.redshift_db.temp_s3,
            table=data_source.redshift_db.table,
            query=data_source.redshift_db.query,
        )
    elif data_source.HasField("snowflake"):
        df = get_snowflake_dataframe(
            spark,
            data_source.snowflake.snowflakeArgs.url,
            data_source.snowflake.snowflakeArgs.database,
            data_source.snowflake.snowflakeArgs.schema,
            data_source.snowflake.snowflakeArgs.warehouse,
            data_source.snowflake.snowflakeArgs.role,
            data_source.snowflake.snowflakeArgs.table,
            data_source.snowflake.snowflakeArgs.query,
        )
    else:
        # FileDataSource
        reader = spark.read
        uri = data_source.file.uri
        if called_for_schema_computation and data_source.file.HasField("schema_uri"):
            # Setting basePath includes the path-based partitions in the DataFrame schema.
            # https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#partition-discovery
            reader = reader.option("basePath", data_source.file.uri)
            uri = data_source.file.schema_uri

        if data_source.file.HasField("schema_override"):
            schema = SparkSchemaWrapper.from_proto(data_source.file.schema_override)
            reader = reader.schema(schema.unwrap())

        if data_source.file.format == FileDataSourceFormat.FILE_DATA_SOURCE_FORMAT_JSON:
            action = lambda: reader.json(uri)
        elif data_source.file.format == FileDataSourceFormat.FILE_DATA_SOURCE_FORMAT_PARQUET:
            action = lambda: reader.parquet(uri)
        elif data_source.file.format == FileDataSourceFormat.FILE_DATA_SOURCE_FORMAT_CSV:
            action = lambda: reader.csv(uri, header=True)
        else:
            raise AssertionError(f"Unsupported file format '{data_source.file.format}'")

        df = tecton_spark.errors_spark.handleDataAccessErrors(action, data_source.file.uri)
        if data_source.file.convert_to_glue_format:
            df = convert_json_like_schema_to_glue_format(spark, df)

    return df


def get_table_dataframe(
    spark: SparkSession, data_source: BatchDataSource, called_for_schema_computation=False
) -> DataFrame:
    """Returns a DataFrame for a table defined by given BatchDataSource proto.

    :param spark: Spark session.
    :param data_source: BatchDataSource proto. BatchDataSource must not be a data source function (spark_batch_config).
    :param called_for_schema_computation: If set, optimizations are applied for faster schema computations.
                                          i.e. FileDSConfig.schema_uri is used to avoid expensive partition discovery.

    :return: The DataFrame created from the data source.
    """

    assert not is_data_source_function(
        data_source
    ), "get_table_dataframe can not be used with data source function (spark_batch_config)."

    df = get_non_dsf_raw_dataframe(spark, data_source, called_for_schema_computation)
    if data_source.HasField("raw_batch_translator"):
        translator_fn = function_deserialization.from_proto(data_source.raw_batch_translator)
        df = translator_fn(df)
    if data_source.HasField("timestamp_column_properties"):
        ts_format = None
        if data_source.timestamp_column_properties.HasField("format"):
            ts_format = data_source.timestamp_column_properties.format
        df = apply_timestamp_column(df, data_source.timestamp_column_properties.column_name, ts_format)

    return df


def get_redshift_dataframe(
    spark: SparkSession, endpoint: str, temp_s3: str, table: Optional[str] = None, query: Optional[str] = None
) -> DataFrame:
    """Returns a DataFrame for a Redshift table defined by given RedshiftDataSource proto.

    :param table: The table name in redshift
    :param temp_s3: The s3 URI for temp data
    :param endpoint: The connection endpoint for redshift (without user or password)
    :param spark: Spark session.

    :return: The DataFrame created from the data source.
    """

    if _is_running_on_emr():
        spark_format = "io.github.spark_redshift_community.spark.redshift"
    else:
        spark_format = "com.databricks.spark.redshift"

    params = {"user": conf.get_or_none("REDSHIFT_USER"), "password": conf.get_or_none("REDSHIFT_PASSWORD")}
    full_connection_string = f"jdbc:redshift://{endpoint};user={params['user']};password={params['password']}"

    df_reader = (
        spark.read.format(spark_format)
        .option("url", full_connection_string)
        .option("tempdir", temp_s3)
        .option("forward_spark_s3_credentials", "true")
    )

    if table and query:
        raise AssertionError(f"Should only specify one of table and query sources for redshift")
    if not table and not query:
        raise AssertionError(f"Missing both table and query sources for redshift, exactly one must be present")

    if table:
        df_reader = df_reader.option("dbtable", table)
    else:
        df_reader = df_reader.option("query", query)

    df = df_reader.load()
    return df


def get_snowflake_dataframe(
    spark: SparkSession,
    url: str,
    database: str,
    schema: str,
    warehouse: str,
    role: Optional[str] = None,
    table: Optional[str] = None,
    query: Optional[str] = None,
) -> DataFrame:
    """Returns a DataFrame for a Snowflake table defined by given SnowflakeDataSource proto.

    :param spark: Spark session.
    :param url: The table name in Snowflake

    :return: The DataFrame created from the data source.
    """

    if table and query:
        raise AssertionError(f"Should only specify one of table and query sources for Snowflake")
    if not table and not query:
        raise AssertionError(f"Missing both table and query sources for Snowflake, exactly one must be present")

    user = conf.get_or_none("SNOWFLAKE_USER")
    password = conf.get_or_none("SNOWFLAKE_PASSWORD")
    if not user or not password:
        raise AssertionError(
            "Snowflake user and password not configured. Instructions at https://docs.tecton.ai/v2/setting-up-tecton/03g-connecting-snowflake.html"
        )

    options = {
        "sfUrl": url,
        "sfUser": user,
        "sfPassword": password,
        "sfDatabase": database,
        "sfSchema": schema,
        "sfWarehouse": warehouse,
        "APPLICATION": "tecton-ai",
    }

    if role:
        options["sfRole"] = role

    df_reader = spark.read.format("snowflake").options(**options)

    if table:
        df_reader = df_reader.option("dbtable", table)
    else:
        df_reader = df_reader.option("query", query)

    df = df_reader.load()
    return df


def apply_timestamp_column(df: DataFrame, ts_column: str, ts_format: Optional[str]) -> DataFrame:
    # Verify the raw source's timestamp column is of type "string"
    column_names = df.schema.names
    if ts_column not in column_names:
        raise AssertionError(f"Timestamp Column '{ts_column}' not found in schema. Found: {column_names}")

    ts_type = df.schema[ts_column].dataType.jsonValue()
    if ts_type != "timestamp":
        assert (
            ts_type == "string"
        ), f"Timestamp Column '{ts_column}' has type '{ts_type}', expected 'string' or 'timestamp'"
        # Apply timestamp transform

        # Here we use coalesce to first try transforming string to timestamp using the user provided format,
        # and if it doesn't work we'll instead let Spark figure it out.
        # Ideally, if the user provided format didn't work, we would not fallback to the Spark default. However, it
        # would be difficult to remove this behavior, and it's hard to imagine a scenario where this would be a problem
        # other than being a bit too "magical". Ref: https://tecton.atlassian.net/browse/TEC-6611
        df = df.withColumn(ts_column, coalesce(to_timestamp(df[ts_column], ts_format), to_timestamp(df[ts_column])))

    return df


def apply_partition_and_timestamp_filter(
    df: DataFrame,
    data_source: BatchDataSource,
    start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
) -> DataFrame:
    """Applies a partition and timestamp filters if the respective column names are set.

    :return: The DataFrame with filter applied.
    """

    # backward compatibility. If we wanted to deprecate, this could be replaced by
    # datetime_partition_columns containing [col_name, "%Y-%m-%d", 24 * 60 * 60]
    if data_source.HasField("date_partition_column"):
        date_partition_column = functions.col(data_source.date_partition_column)
        if start_time:
            date_start = start_time.to_date_string()
            df = df.where(date_start <= date_partition_column)
        if end_time:
            date_end = end_time.to_date_string()
            df = df.where(date_partition_column <= date_end)
    # add datetime partition filters
    elif len(data_source.datetime_partition_columns) > 0:
        partition_filter = _build_partition_filter(data_source.datetime_partition_columns, start_time, end_time)
        if partition_filter is not None:
            df = df.where(partition_filter)
    # add timestamp filter
    if data_source.HasField("timestamp_column_properties"):
        ts_column = functions.col(data_source.timestamp_column_properties.column_name)
        if start_time:
            df = df.where(ts_column >= start_time)
        if end_time:
            df = df.where(ts_column < end_time)

    return df


# Generate filter on time_range with at most OR of 2 filters.
# This means we could end up scanning more partitions than necessary, but number extra scanned will be at most
# 3x.
# Worst case: time_range = 367 days across 3 years, we scan entire 3 years.
#             time_range = 365 days, we scan up to 2 years including that 1 year range
#             time_range = 28.1 days, we could scan all of January + February + March = 90 days
#
# 2 cases to consider
# Example: partition cols y, m, d, h: in both examples, the time range is between day and month, so we don't add any
# filters on hour, even though it would be possible to scan some fewer partitions if we did
# (A)Time range: 2020 Jan 10 10:00:00 AM - 2020 Jan 15 5:00:00 AM
#  --> (y = start.year & m = start.month & d >= start.day & d <= end.day)
# (B)Time range: 2019 Dec 21 10:00:00 AM - 2020 Jan 10 5:00:00 AM
#  --> ((y = start.year & m = start.month & d >= start.day) | (y = end.year & m = end.month & d <= end.day))
def _build_partition_filter(
    datetime_partition_columns,
    start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
):
    if not start_time and not end_time:
        return None

    range_duration = end_time - start_time if start_time and end_time else None

    # Filters relating to start_time and end_time
    start_filters = []
    end_filters = []
    # Common filter that applies to the entire range
    common_filters = []

    # sort partition columns by the number of seconds they represent from highest to lowest
    partitions_high_to_low = sorted(datetime_partition_columns, key=lambda c: c.minimum_seconds, reverse=True)
    for partition in partitions_high_to_low:
        partition_col = functions.col(partition.column_name)
        partition_value_at_start = _partition_value_for_time(partition, start_time) if start_time else None
        partition_value_at_end = _partition_value_for_time(partition, end_time) if end_time else None
        # If partition's datepart minimum length is >= range_duration secs, we can be sure that 2 or fewer equality filters are enough to cover all possible times in time_limits
        # If range_duration is None/unbounded, always use range filter
        if range_duration and partition.minimum_seconds >= range_duration.total_seconds():
            if partition_value_at_start == partition_value_at_end:
                common_filters.append(partition_col == partition_value_at_start)
            else:
                start_filters.append(partition_col == partition_value_at_start)
                end_filters.append(partition_col == partition_value_at_end)
        # Otherwise, we need to use a range filter
        else:
            start_range_filter = partition_col >= partition_value_at_start if partition_value_at_start else None
            end_range_filter = partition_col <= partition_value_at_end if partition_value_at_end else None

            # Case A: there are only common filters
            if len(start_filters) == 0:
                if start_range_filter is not None:
                    common_filters.append(start_range_filter)
                if end_range_filter is not None:
                    common_filters.append(end_range_filter)
                # we can't combine range filters on multiple columns, so break and ignore any smaller columns
                break
            # Case B
            else:
                if start_range_filter is not None:
                    start_filters.append(start_range_filter)
                if end_range_filter is not None:
                    end_filters.append(end_range_filter)
                # we can't combine range filters on multiple columns, so break and ignore any smaller columns
                break

    common_filter = _and_filters_in_list(common_filters)
    start_filter = _and_filters_in_list(start_filters)
    end_filter = _and_filters_in_list(end_filters)
    return common_filter & (start_filter | end_filter)


def _partition_value_for_time(partition, time):
    fmt = partition.format_string
    # On mac/linux strftime supports these formats, but
    # Windows python does not
    # Zero-padded formats are safe for a string comparison. Otherwise we need to compare ints
    # As long as the values returned here are ints, the column will be implicitly converted if needed.
    if fmt == "%-Y":
        return time.year
    elif fmt == "%-m":
        return time.month
    elif fmt == "%-d":
        return time.day
    elif fmt == "%-H":
        return time.hour
    return time.strftime(fmt)


def _and_filters_in_list(filter_list):
    if len(filter_list) == 0:
        return functions.lit(True)
    else:
        from functools import reduce

        return reduce(lambda x, y: x & y, filter_list)


def get_table_column_and_partition_names(spark: SparkSession, data_source: "HiveDSConfig") -> Tuple[Set[str], Set[str]]:  # type: ignore
    """Returns a tuple of (set of column names, set of partition names) for the given BatchDataSource."""
    _validate_data_source_proto(data_source)
    database = data_source.hive_table.database
    table = data_source.hive_table.table
    pandas_df = spark.sql(f"DESCRIBE TABLE {database}.{table}").toPandas()
    column_names = set(pandas_df[~pandas_df.col_name.str.startswith("#")].col_name)
    partition_index = pandas_df.index[pandas_df["col_name"] == "# Partition Information"]
    if partition_index.size > 0:
        partition_info = pandas_df[partition_index[0] :]
        partition_names = set(partition_info[~partition_info.col_name.str.startswith("#")].col_name)
    else:
        partition_names = set()

    return column_names, partition_names


def create_kinesis_stream_reader(
    spark: SparkSession,
    stream_name: str,
    region: str,
    initial_stream_position: Optional[str],
    data_source_options: List[StreamDataSource.Option],
    option_overrides: Optional[Dict[str, str]],
) -> DataFrame:
    """
    Returns a DataFrame representing a Kinesis stream reader.

    :param data_source_options: Spark options specified in the data source definition.
    :param option_overrides: Spark options that should override options set implicitly (e.g. ``stream_name``) or
        explicitly  (e.g. ``options``) by the data source definition.
    """
    options = {"streamName": stream_name}
    if _is_running_on_emr():
        options.update(
            {
                "endpointUrl": f"https://kinesis.{region}.amazonaws.com",
                "kinesis.client.describeShardInterval": "30s",
                "startingPosition": initial_stream_position,
            }
        )
    else:
        options.update({"region": region, "shardFetchInterval": "30s", "initialPosition": initial_stream_position})

    databricks_to_qubole_map = {
        "awsaccesskey": "awsAccessKeyId",
        "rolearn": "awsSTSRoleARN",
        "rolesessionname": "awsSTSSessionName",
    }
    lowercase_data_source_options = {option.key.lower(): option.value for option in data_source_options}
    for option in data_source_options:
        if option.key.lower() in databricks_to_qubole_map and _is_running_on_emr():
            if option.key.lower() == "rolearn" and "rolesessionname" not in lowercase_data_source_options:
                # this field must be supplied if we use roleArn for qubole kinesis reader
                options["awsSTSSessionName"] = "tecton-materialization"
            options[databricks_to_qubole_map[option.key.lower()]] = option.value
        else:
            options[option.key] = option.value

    if option_overrides:
        options.update(option_overrides)

    reader = spark.readStream.format("kinesis").options(**options)
    return reader.load()


def create_kafka_stream_reader(
    spark: SparkSession,
    kafka_bootstrap_servers: str,
    topics: str,
    data_source_options: List[StreamDataSource.Option],
    option_overrides: Optional[Dict[str, str]],
    ssl_keystore_location: Optional[str] = None,
    ssl_keystore_password_secret_id: Optional[str] = None,
    ssl_truststore_location: Optional[str] = None,
    ssl_truststore_password_secret_id: Optional[str] = None,
    security_protocol: Optional[str] = None,
) -> DataFrame:
    """Returns a Kafka stream reader.

    :param data_source_options: Spark options specified in the data source definition.
    :param option_overrides: Spark options that should override options set implicitly (e.g. ``topics``) or explicitly
        (e.g. ``options``) by the data source definition.
    """
    options = {o.key: o.value for o in data_source_options}
    options["kafka.bootstrap.servers"] = kafka_bootstrap_servers
    options["subscribe"] = topics
    # Kafka by default consumes all the exisitng data into a single micro-batch, that can overwhelm
    # the Spark cluster during backfilling from a stream for the first time.
    # Set the default number of records to be read per micro-batch (across all partitions).
    options["maxOffsetsPerTrigger"] = str(KAFKA_DEFAULT_MAX_OFFSETS_PER_TRIGGER)
    if all(key not in options for key in KAFKA_STARTING_OFFSET_CONFIG_KEYS):
        # Don't override startingOffsets if it or similar option is set
        # explicitly in the data source definition.
        options["startingOffsets"] = "earliest"
    options = _populate_kafka_consumer_options(topics, options)

    if ssl_keystore_location:
        local_keystore_loc, local_keystore_password = get_kafka_secrets(
            ssl_keystore_location, ssl_keystore_password_secret_id
        )
        options["kafka.ssl.keystore.location"] = local_keystore_loc
        if local_keystore_password:
            options["kafka.ssl.keystore.password"] = local_keystore_password
    if ssl_truststore_location:
        local_truststore_loc, local_truststore_password = get_kafka_secrets(
            ssl_truststore_location, ssl_truststore_password_secret_id
        )
        options["kafka.ssl.truststore.location"] = local_truststore_loc
        if local_truststore_password:
            options["kafka.ssl.truststore.password"] = local_truststore_password
    if security_protocol:
        options["kafka.security.protocol"] = security_protocol

        # Hack: dynamic PLAIN SASL_SSL authentication when the
        # authentication is unset. Approved usage for Square until Data Source
        # Functions is launched.
        # TODO(TEC-9976): remove once Square is on Data Source Functions.
        if (
            security_protocol == "SASL_SSL"
            and options.get("kafka.sasl.mechanism") == "PLAIN"
            and options.get("kafka.sasl.jaas.config") is None
        ):
            sasl_username = conf.get_or_none("SECRET_TECTON_KAFKA_SASL_USERNAME")
            sasl_password = conf.get_or_none("SECRET_TECTON_KAFKA_SASL_PASSWORD")
            kafka_sasl_jaas_config = f"kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username='{sasl_username}' password='{sasl_password}';"
            options["kafka.sasl.jaas.config"] = kafka_sasl_jaas_config

    if option_overrides:
        options.update(option_overrides)

    reader = spark.readStream.format("kafka").options(**options)
    return reader.load()


# This is a short term fix to unblock Kafka customers. We will replace these with proper FCO configurations.
# This function sets 2 Kafka consumer options `maxOffsetsPerTrigger` and `startingOffsetsByTimestamp` that
# are gatekept by the Environment variables set into the Spark cluster.
#  - The `maxOffsetsPerTrigger` represents the max number of records read into a SSS micro-batch.
#  - The `startingOffsetsByTimestamp` dynamically overrides the starting timestamps on the Kafka partitions
#    to limit the amount of data read from the Kafka data source.
def _populate_kafka_consumer_options(topics: str, kafka_options: Dict[str, Any]) -> Dict[str, Any]:
    max_offsets = os.environ.get(KAFKA_MAX_OFFSETS_PER_TRIGGER_ENV)
    if max_offsets is not None:
        assert str.isdigit(max_offsets), f"{KAFKA_MAX_OFFSETS_PER_TRIGGER_ENV} must be a string encoded integer"
        kafka_options["maxOffsetsPerTrigger"] = max_offsets

    num_hours_to_process = os.environ.get(KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV)
    if num_hours_to_process is not None:
        assert str.isdigit(
            num_hours_to_process
        ), f"{KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV} must be a string encoded integer"
        num_partitions = os.environ.get(KAFKA_NUM_PARTITIONS_ENV)
        assert num_partitions is not None and str.isdigit(
            num_partitions
        ), f"{KAFKA_NUM_PARTITIONS_ENV} missing/invalid when {KAFKA_STARTING_OFFSETS_NUM_HOURS_IN_THE_PAST_ENV} is set"
        # `startingOffsetsByTimestamp` needs unix timestamps in millis per partition number.
        current_ts = int(time.time())
        starting_ts = (current_ts - int(num_hours_to_process) * 3600) * 1000
        ts_per_partition = {str(partition): starting_ts for partition in range(int(num_partitions))}
        topic_names = topics.split(",")
        starting_offsets_by_ts = {topic_name: ts_per_partition for topic_name in topic_names}
        kafka_options["startingOffsetsByTimestamp"] = json.dumps(starting_offsets_by_ts)

    return kafka_options


def get_non_dsf_raw_stream_dataframe(
    spark: SparkSession, stream_data_source: StreamDataSource, option_overrides: Optional[Dict[str, str]] = None
) -> DataFrame:
    """Returns a DataFrame representing the raw stream data.

    :param spark: Spark session.
    :param stream_data_source: StreamDataSource proto. StreamDataSource must not be a data source function (spark_stream_config).
    :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set by
        the data source.

    :return: The DataFrame for the raw stream data source.
    """
    if stream_data_source.HasField("kinesis_data_source"):
        kinesis_data_source = stream_data_source.kinesis_data_source
        initial_stream_position = _get_initial_stream_position(stream_data_source)
        df = create_kinesis_stream_reader(
            spark,
            kinesis_data_source.stream_name,
            kinesis_data_source.region,
            initial_stream_position,
            stream_data_source.options,
            option_overrides,
        )
    elif stream_data_source.HasField("kafka_data_source"):
        kafka_data_source = stream_data_source.kafka_data_source
        df = create_kafka_stream_reader(
            spark,
            kafka_data_source.bootstrap_servers,
            kafka_data_source.topics,
            stream_data_source.options,
            option_overrides,
            ssl_keystore_location=kafka_data_source.ssl_keystore_location,
            ssl_keystore_password_secret_id=kafka_data_source.ssl_keystore_password_secret_id,
            ssl_truststore_location=kafka_data_source.ssl_truststore_location,
            ssl_truststore_password_secret_id=kafka_data_source.ssl_truststore_password_secret_id,
            security_protocol=kafka_data_source.security_protocol,
        )
    else:
        raise ValueError("Unknown stream data source type")
    return df


def get_stream_dataframe(
    spark: SparkSession, stream_data_source: StreamDataSource, option_overrides: Optional[Dict[str, str]] = None
) -> DataFrame:
    """Returns a DataFrame representing a stream data source *without* any options specified.
    Use get_stream_dataframe_with_options to get a DataFrame with stream-specific options.

    :param spark: Spark session.
    :param stream_data_source: StreamDataSource proto. StreamDataSource must not be a data source function (spark_stream_config).
    :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set by
        the data source.

    :return: The DataFrame created from the data source.
    """
    assert not is_data_source_function(
        stream_data_source
    ), "get_stream_dataframe can not be used with data source function (spark_stream_config)."

    df = get_non_dsf_raw_stream_dataframe(spark, stream_data_source, option_overrides)
    translator_fn = function_deserialization.from_proto(stream_data_source.raw_stream_translator)
    return translator_fn(df)


def get_stream_dataframe_with_options(
    spark: SparkSession, stream_data_source: StreamDataSource, option_overrides: Optional[Dict[str, str]] = None
) -> DataFrame:
    """Returns a DataFrame representing a stream data source with additional options:
        - drop duplicate column names
        - initial stream position

    :param spark: Spark session.
    :param stream_data_source: StreamDataSource proto. StreamDataSource must not be a data source function (spark_stream_config).
    :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set by
        the data source.

    :return: The DataFrame created from the data source.
    """
    assert not is_data_source_function(
        stream_data_source
    ), "get_stream_dataframe_with_options can not be used with data source function (spark_stream_config)."

    df = get_stream_dataframe(spark, stream_data_source, option_overrides)

    dedup_columns = [column for column in stream_data_source.deduplication_column_names]
    if dedup_columns:
        df = df.dropDuplicates(dedup_columns)

    return df


def _get_watermark(stream_data_source: StreamDataSource) -> str:
    """Returns watermark as an "N seconds" string for the streaming data source.

    :param stream_data_source: StreamDataSource proto.

    :return: The watermark duration in seconds in string format.
    :rtype: String
    """
    return "{} seconds".format(stream_data_source.stream_config.watermark_delay_threshold.seconds)


def _get_initial_stream_position(stream_data_source: StreamDataSource) -> Optional[str]:
    """Returns initial stream position as a string (e.g. "latest") for the streaming data source.

    :param stream_data_source: StreamDataSource proto.

    :return: The initial stream position in string format.
    """
    return INITIAL_STREAM_POSITION_ENUM_TO_STR[stream_data_source.stream_config.initial_stream_position]


# should not be invoked directly by public SDK. Use TectonContext wrapper instead
def register_temp_views_for_feature_definition(
    spark: SparkSession,
    feature_definition: FeatureDefinition,
    data_sources: List[VirtualDataSource],
    register_stream: bool,
    raw_data_time_limits: Optional[pendulum.Period] = None,
):
    """Registers spark temp views per DataSource based on a FeatureView proto.

    :param spark: Spark session.
    :param feature_definition: FeatureDefinition interface implementing class.
    :param data_sources: Data source protos
    :param register_stream: If true, a stream DataFrame will be registered for streaming DSs instead of batch.
    :param raw_data_time_limits: The raw data time limits for the batch data source.
    """
    ds_by_id = {IdHelper.to_string(ds.virtual_data_source_id): ds for ds in data_sources}

    for ds_id in feature_definition.data_source_ids:
        register_temp_view_for_data_source(
            spark,
            ds_by_id[ds_id],
            register_stream,
            raw_data_time_limits=raw_data_time_limits,
        )


# should not be invoked directly by public SDK. Use TectonContext wrapper instead
def register_temp_view_for_data_source(
    spark: SparkSession,
    data_source: VirtualDataSource,
    register_stream: bool,
    raw_data_time_limits: Optional[pendulum.Period] = None,
    name: str = None,
    called_for_schema_computation: bool = False,
):
    """Registers a spark temp view for the data source.
    :param spark: Spark session.
    :param data_source: DataSource proto.
    :param register_stream: If true, a stream DataFrame will be registered for streaming DataSources instead of batch.
    :param raw_data_time_limits: If set, a data frame will filter on the time limits based on any partition columns that exist.
    :param name: If set, use this name for the temp view. Defaults to DS name.
    :param called_for_schema_computation: Indicates if method is being invoked to compute a schema.
    """
    if not register_stream and raw_data_time_limits:
        validate_data_source_timestamp_present_for_feature_view(data_source)
    df = get_ds_dataframe(
        spark,
        data_source,
        register_stream,
        start_time=raw_data_time_limits.start if raw_data_time_limits else None,
        end_time=raw_data_time_limits.end if raw_data_time_limits else None,
        called_for_schema_computation=called_for_schema_computation,
    )
    df.createOrReplaceTempView(data_source.fco_metadata.name if name is None else name)


def get_ds_dataframe(
    spark: SparkSession,
    data_source: VirtualDataSource,
    consume_streaming_data_source: bool,
    start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    called_for_schema_computation=False,
    stream_option_overrides: Optional[Dict[str, str]] = None,
):
    if consume_streaming_data_source and (start_time or end_time):
        raise AssertionError("Can't specify start or end time when consuming streaming data source")

    if consume_streaming_data_source:
        assert data_source.HasField(
            "stream_data_source"
        ), f"Can't consume streaming data source from the BatchDataSource: {data_source.fco_metadata.name}."

        if is_data_source_function(data_source.stream_data_source):
            df = _get_data_source_function_stream_dataframe(spark, data_source.stream_data_source)
        else:
            df = get_stream_dataframe_with_options(spark, data_source.stream_data_source, stream_option_overrides)
    else:
        if is_data_source_function(data_source.batch_data_source):
            df = get_data_source_function_batch_dataframe(
                spark, data_source.batch_data_source, start_time=start_time, end_time=end_time
            )
        else:
            df = get_table_dataframe(
                spark, data_source.batch_data_source, called_for_schema_computation=called_for_schema_computation
            )
            if start_time or end_time:
                df = apply_partition_and_timestamp_filter(df, data_source.batch_data_source, start_time, end_time)

        if data_source.HasField("stream_data_source"):
            schema = data_source.stream_data_source.spark_schema
            cols = [field.name for field in schema.fields]
            df = df.select(*cols)

    return df


def convert_json_like_schema_to_glue_format(spark: SparkSession, df: DataFrame) -> DataFrame:
    """
    Converts a DataFrame schema to lowercase. This assumes JSON so
    MapTypes or Arrays of non-StructTypes are not allowed.

    :param spark: Spark session.
    :param df: DataFrame input.
    :return: DataFrame with lowercase schema.
    """

    def _get_lowercase_schema(datatype):
        if type(datatype) == ArrayType:
            return _get_lowercase_array_schema(datatype)
        elif type(datatype) == StructType:
            return _get_lowercase_structtype_schema(datatype)
        elif type(col.dataType) == MapType:
            raise TypeError("MapType not supported in JSON schema")
        return datatype

    def _get_lowercase_structtype_schema(s) -> StructType:
        assert type(s) == StructType, f"Invalid argument type {type(s)}, expected StructType"
        struct_fields = []
        for col in s:
            datatype = _get_lowercase_schema(col.dataType)
            struct_fields.append(StructField(col.name.lower(), datatype))
        return StructType(struct_fields)

    def _get_lowercase_array_schema(c) -> ArrayType:
        assert (
            type(c.elementType) == StructType
        ), f"Invalid ArrayType element type {type(c)}, expected StructType for valid JSON arrays."
        datatype = c.elementType
        struct_schema = _get_lowercase_structtype_schema(datatype)
        return ArrayType(struct_schema)

    # Simple columns (LongType, StringType, etc) can just be renamed without
    # casting schema.
    # Nested fields within complex columns (ArrayType, StructType) must also be recursively converted
    # to lowercase names, so they must be casted.
    # DateType columns should be converted to StringType to match Glue schemas.
    new_fields = []
    for col in df.schema:
        if type(col.dataType) in [ArrayType, StructType, MapType]:
            t = _get_lowercase_schema(col.dataType)
            new_fields.append(functions.col(col.name).cast(t).alias(col.name.lower()))
        elif type(col.dataType) is DateType:
            new_fields.append(functions.col(col.name).cast(StringType()).alias(col.name.lower()))
        else:
            new_fields.append(functions.col(col.name).alias(col.name.lower()))
    return df.select(new_fields)


def validate_data_source_timestamp_present_for_feature_view(data_source: VirtualDataSource):
    """
    Verifies the batch data_source has the timestamp_column_properties field or supports_time_filtering is True if it is a Data Source Function.

    :param data_source: a VirtualDataSource containing a batch_data_source
    """
    batch_data_source = data_source.batch_data_source
    if not is_data_source_function(batch_data_source) and not batch_data_source.HasField("timestamp_column_properties"):
        raise Exception(f"DataSource {data_source.fco_metadata.name} requires timestamp column name for FeatureView")

    if (
        is_data_source_function(batch_data_source)
        and not batch_data_source.spark_data_source_function.supports_time_filtering
    ):
        raise Exception(
            f"supports_time_filtering for DataSource {data_source.fco_metadata.name} needs to be True for FeatureView"
        )


def is_data_source_function(data_source: Union[BatchDataSource, StreamDataSource]):
    return data_source.HasField("spark_data_source_function")


def get_data_source_function_batch_dataframe(
    spark: SparkSession, data_source: BatchDataSource, start_time: Optional[datetime], end_time: Optional[datetime]
):
    data_source_func = function_deserialization.from_proto(data_source.spark_data_source_function.function)
    if data_source.spark_data_source_function.supports_time_filtering:
        filter_context = FilterContext(start_time, end_time)
        return data_source_func(spark, filter_context)
    return data_source_func(spark)


def _get_data_source_function_stream_dataframe(spark: SparkSession, data_source: StreamDataSource):
    data_source_func = function_deserialization.from_proto(data_source.spark_data_source_function.function)
    return data_source_func(spark)
