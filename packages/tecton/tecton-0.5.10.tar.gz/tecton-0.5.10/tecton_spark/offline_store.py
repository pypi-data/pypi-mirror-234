import functools
import itertools
import os
import random
import time
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional
from typing import Union

import pendulum
from py4j.protocol import Py4JJavaError
from pyspark.sql import Column
from pyspark.sql import DataFrame
from pyspark.sql import functions
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import StructType
from pyspark.sql.types import TimestampType
from pyspark.sql.utils import AnalysisException

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.logger import get_logger
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_proto.args import feature_view_pb2 as args_proto
from tecton_spark.partial_aggregations import TEMPORAL_ANCHOR_COLUMN_NAME
from tecton_spark.time_utils import convert_epoch_to_datetime
from tecton_spark.time_utils import convert_timestamp_to_epoch

TIME_PARTITION = "time_partition"
ANCHOR_TIME = "_anchor_time"

DBRICKS_MULTI_CLUSTER_WRITES_ENABLED = "spark.databricks.delta.multiClusterWrites.enabled"
DBRICKS_RUNTIME_VERSION = "DATABRICKS_RUNTIME_VERSION"

DELTA_LOGSTORE_CLASS = "spark.delta.logStore.class"
DYNAMODB_LOGSTORE_CLASS = "io.delta.storage.DynamoDBLogStore"

logger = get_logger("offline_store")


@dataclass
class OfflineStoreParams:
    s3_path: str

    always_store_anchor_column: bool
    """Whether the anchor column should be stored in the Offline Feature Store regardless of whether it is
    required by the storage layer.

    If this is false the anchor column will be dropped from the stored data if it's not needed by the
    OfflineStoreWriter implementation.
    """

    time_column: str
    """The column containing the timestamp value used for time-based partitioning"""

    join_key_columns: List[str]

    is_continuous: bool


def get_offline_store_writer(
    params: OfflineStoreParams, fv_config: args_proto.OfflineFeatureStoreConfig, version: int, spark: SparkSession
):
    """Creates a concrete implementation of OfflineStoreWriter based on fv_config."""
    case = fv_config.WhichOneof("store_type")
    if case == "delta":
        return DeltaWriter(params, fv_config.delta, spark, version)
    elif case == "parquet":
        return ParquetWriter(params, spark, version)
    # Remove default after database migration is complete.
    # raise KeyError(case)
    return ParquetWriter(params, spark, version)


def get_offline_store_reader(spark: SparkSession, fd: FeatureDefinition) -> "OfflineStoreReader":
    case = fd.offline_store_config.WhichOneof("store_type")
    if case == "delta":
        return DeltaReader(spark, fd)
    elif case == "parquet":
        return ParquetReader(spark, fd)
    # Remove default after database migration is complete.
    # raise KeyError(case)
    return ParquetReader(spark, fd)


class OfflineStoreWriter(ABC):
    """Interface for Offline Feature Store writers."""

    @abstractmethod
    def append_dataframe(self, data_frame):
        """Append the rows from data_frame to the Store table. Nothing is overwritten."""
        raise NotImplementedError

    @abstractmethod
    def upsert_dataframe(self, data_frame):
        """Upsert the rows from data_frame to the Store table.

        Rows with matching join keys and time column are overwritten. Other rows are inserted.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_keys(self, data_frame) -> int:
        """Delete rows from the Store table that match the keys inside the data_frame.

        Return number of successfully deleted keys."""
        raise NotImplementedError


class OfflineStoreReader(ABC):
    @abstractmethod
    def read(self, time_limits: pendulum.Period) -> DataFrame:
        raise NotImplementedError


class ParquetWriter(OfflineStoreWriter):
    """Parquet implementation of OfflineStoreWriter"""

    def __init__(self, params: OfflineStoreParams, spark: SparkSession, version: int):
        self._params = params
        self._spark = spark
        self._version = version

    def append_dataframe(self, data_frame):
        if self._params.is_continuous:
            align_duration = convert_timedelta_for_version(pendulum.duration(seconds=86400), self._version)
            aligned_time = _align_timestamp(functions.col(ANCHOR_TIME), functions.lit(align_duration))
            data_frame = data_frame.withColumn(TIME_PARTITION, aligned_time)
            partition_col = TIME_PARTITION
        else:
            partition_col = ANCHOR_TIME

        mode = self._spark.conf.get("spark.sql.sources.partitionOverwriteMode")
        if mode != "dynamic":
            raise ValueError(f"partitionOverWrite mode should be dynamic, Found {mode}")
        data_frame.write.partitionBy(partition_col).parquet(self._params.s3_path, mode="overwrite")

    def upsert_dataframe(self, data_frame):
        raise NotImplementedError()

    def delete_keys(self, data_frame):
        raise NotImplementedError()


class ParquetReader(OfflineStoreReader):
    def __init__(self, spark: SparkSession, fd: FeatureDefinition):
        self._spark = spark
        assert fd.materialization_enabled and fd.writes_to_offline_store
        self._path = fd.materialized_data_path
        self._window = fd.min_scheduling_interval
        self.version = fd.get_feature_store_format_version
        self._fd = fd

    def read(self, time_limits: Optional[pendulum.Period]):
        spark_df = self._spark.read.parquet(self._path)

        # Parquet is partitioned by TIME_PARTITION when is_continuous and ANCHOR_TIME when not.
        # We want to explicitly cast the partition type in case:
        #   `spark.sql.sources.partitionColumnTypeInference.enabled` = "false"
        if self._fd.is_continuous_temporal_aggregate:
            spark_df = spark_df.withColumn(TIME_PARTITION, functions.col(TIME_PARTITION).cast("timestamp"))
        else:
            spark_df = spark_df.withColumn(ANCHOR_TIME, functions.col(ANCHOR_TIME).cast("long"))

        # TODO(TEC-9802): use TIME_PARTITION partition filter for continuous FVs
        if time_limits:
            start_time_epoch = convert_timestamp_to_epoch(time_limits.start, self.version)
            end_time_epoch = convert_timestamp_to_epoch(time_limits.end, self.version)
            if _size_seconds(self._window) == 0:
                start = start_time_epoch
                end = end_time_epoch
            else:
                start = _align_timestamp(start_time_epoch, _size_seconds(self._window))
                end = _align_timestamp(end_time_epoch, _size_seconds(self._window))
            anchor_time_col = functions.col(ANCHOR_TIME)
            spark_df = spark_df.where((start <= anchor_time_col) & (anchor_time_col <= end))
        return spark_df.drop(TIME_PARTITION)


_EXCEPTION_PACKAGES = {
    "com.databricks.sql.transaction.tahoe",  # Used by Databricks
    "org.apache.spark.sql.delta",  # Used by open source
}

_EXCEPTION_CLASSES = {
    "ConcurrentAppendException",
    "ConcurrentDeleteReadException",
    "ConcurrentDeleteDeleteException",
    "ProtocolChangedException",  # This can occur when two txns create the same table concurrently
}

_RETRYABLE_DELTA_EXCEPTIONS = {
    f"{pkg}.{cls}" for pkg, cls in itertools.product(_EXCEPTION_PACKAGES, _EXCEPTION_CLASSES)
}


def _with_delta_retries(f, max_retries=5):
    """Retries the wrapped function upon Deltalake conflict errors."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        from delta.exceptions import (
            ConcurrentAppendException,
            ConcurrentDeleteDeleteException,
            ConcurrentDeleteReadException,
            ConcurrentTransactionException,
            DeltaConcurrentModificationException,
            MetadataChangedException,
            ProtocolChangedException,
        )

        final_exception = None
        for i in range(max_retries):
            try:
                if i > 0:
                    # Add a random delay (with exponential backoff) before the retries to decrease
                    # the chance of recurrent conflicts between the parallel offline store writers.
                    # Possible 10s of seconds of delay is insignificant to the overall job's latency.
                    exponential_coef = 2 ** (i - 1)
                    retry_delay = exponential_coef * random.uniform(0, 1)
                    time.sleep(retry_delay)
                f(*args, **kwargs)
                return
            except Py4JJavaError as e:
                exception_class = e.java_exception.getClass().getCanonicalName()
                if exception_class not in _RETRYABLE_DELTA_EXCEPTIONS:
                    raise e
                final_exception = e
                logger.info(
                    f"Delta transaction failed (attempt {i + 1}/5); retrying",
                    exc_info=True,  # Include information about the exception currently being handled
                )
            except (
                ConcurrentAppendException,
                ConcurrentDeleteDeleteException,
                ConcurrentDeleteReadException,
                ConcurrentTransactionException,
                DeltaConcurrentModificationException,
                MetadataChangedException,
                ProtocolChangedException,
            ) as e:
                final_exception = e
                logger.info(
                    f"Delta transaction failed (attempt {i + 1}/5); retrying",
                    exc_info=True,  # Include information about the exception currently being handled
                )
            except Exception:
                logger.warning("Uncaught exception raised during Delta write", exc_info=True)
                raise
        raise Exception(f"Exceeded maximum Delta transaction retries ({max_retries})") from final_exception

    return wrapper


def _assert_safe_delta_write_configuration(spark: SparkSession):
    """Asserts that the Spark configuration is such that it is safe to write to Delta concurrently.

    With the Open Source Delta JAR installed (as it is on EMR), writing to a Delta table concurrently with another
    Spark cluster could corrupt the table unless the Delta Logstore class is overridden.

    On Databricks everything as fine as multi-cluster writes are enabled (the default).
    """
    configs = {
        DBRICKS_RUNTIME_VERSION: os.environ.get(DBRICKS_RUNTIME_VERSION, None),
        DBRICKS_MULTI_CLUSTER_WRITES_ENABLED: spark.conf.get(DBRICKS_MULTI_CLUSTER_WRITES_ENABLED, None),
        DELTA_LOGSTORE_CLASS: spark.conf.get(DELTA_LOGSTORE_CLASS, None),
    }
    if configs[DBRICKS_RUNTIME_VERSION] and configs[DBRICKS_MULTI_CLUSTER_WRITES_ENABLED] == "true":
        return True
    if configs[DELTA_LOGSTORE_CLASS] == DYNAMODB_LOGSTORE_CLASS:
        return True
    raise AssertionError(f"Configuration is not safe for concurrent writes: {configs}")


class DeltaWriter(OfflineStoreWriter):
    """DeltaLake implementation of OfflineStoreWriter"""

    def __init__(
        self, params: OfflineStoreParams, delta_config: args_proto.DeltaConfig, spark: SparkSession, version: int
    ):
        self._params = params
        self._delta_config = delta_config
        self._version = version
        self._spark = spark
        self._window = delta_config.time_partition_size.ToTimedelta()
        self._metadata_writer = DeltaMetadataWriter(spark)
        if not spark.conf.get("spark.databricks.delta.commitInfo.userMetadata"):
            raise AssertionError(f"Expected spark.databricks.delta.commitInfo.userMetadata to be set for delta writes")

    def append_dataframe(self, data_frame: DataFrame):
        data_frame = self._add_partition(data_frame)
        self._ensure_table_exists(self._spark, data_frame.schema)
        self._append_dataframe(data_frame)

    def upsert_dataframe(self, data_frame):
        # See https://github.com/delta-io/delta/issues/282 for why this isn't at the top of the file
        from delta.tables import DeltaTable

        _assert_safe_delta_write_configuration(self._spark)

        data_frame = self._add_partition(data_frame)
        self._ensure_table_exists(self._spark, data_frame.schema)

        table = DeltaTable.forPath(self._spark, self._params.s3_path)

        base = table.toDF().alias("base")
        updates = data_frame.alias("updates")

        # Build a condition which matches on all join keys, the timestamp, and the time partition column. The time
        # partition column is not needed for correctness, but it allows some files to be skipped by Delta.
        all_match_keys = [self._params.time_column, TIME_PARTITION, *self._params.join_key_columns]
        key_matches = [base[k] == updates[k] for k in all_match_keys]
        match_condition = functools.reduce(lambda l, r: l & r, key_matches)

        @_with_delta_retries
        def _execute():
            table.merge(updates, match_condition).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

        _execute()

    def delete_keys(self, data_frame) -> int:
        # See https://github.com/delta-io/delta/issues/282 for why this isn't at the top of the file
        from delta.tables import DeltaTable

        _assert_safe_delta_write_configuration(self._spark)

        deltaTable = DeltaTable.forPath(self._spark, self._params.s3_path)
        query = ""
        columns = data_frame.columns
        for column in columns:
            if query:
                query = query + " AND "
            query = query + "t." + column + " = k." + column

        @_with_delta_retries
        def _execute():
            deltaTable.alias("t").merge(data_frame.alias("k"), query).whenMatchedDelete().execute()

        @_with_delta_retries
        def _vacuum():
            deltaTable.vacuum()

        _execute()
        _vacuum()

        last_operation = deltaTable.history(1).collect()
        if not last_operation:
            return 0

        return int(last_operation[0].operationMetrics.get("numTargetRowsDeleted", 0))

    def delete_time_range(
        self,
        feature_start_time: datetime,
        feature_end_time: datetime,
        feature_store_format_version: int,
    ):
        from delta.tables import DeltaTable

        start_timestamp = pendulum.instance(feature_start_time).int_timestamp
        end_timestamp = pendulum.instance(feature_end_time).int_timestamp
        start_partition = _unix_timestamp_to_partition(start_timestamp, self._window)
        end_partition = _unix_timestamp_to_partition(end_timestamp, self._window)
        start_time = convert_timestamp_to_epoch(feature_start_time, feature_store_format_version)
        end_time = convert_timestamp_to_epoch(feature_end_time, feature_store_format_version)

        assert self._params.always_store_anchor_column

        table = DeltaTable.forPath(self._spark, self._params.s3_path)

        @_with_delta_retries
        def _execute():
            table.delete(
                f'{ANCHOR_TIME} >= {start_time} and {ANCHOR_TIME} < {end_time} and {TIME_PARTITION} >= to_timestamp("{start_partition}") and {TIME_PARTITION} <= to_timestamp("{end_partition}")'
            )

        _execute()

    def _add_partition(self, data_frame: DataFrame) -> DataFrame:
        """Adds the time_partition column and drops the _anchor_time column if needed."""
        partition_size = self._delta_config.time_partition_size.ToTimedelta()
        partition = _timestamp_to_partition_column(data_frame, self._params.time_column, partition_size, self._version)
        data_frame = data_frame.withColumn(TIME_PARTITION, partition)
        if not self._params.always_store_anchor_column:
            data_frame = data_frame.drop(ANCHOR_TIME)
        return data_frame

    def _ensure_table_exists(self, spark: SparkSession, schema: StructType):
        """Ensures that the table exists with the given schema.

        Some operations (including merge) fail when the table doesn't already exist. Others (append) can have conflicts
        where they wouldn't normally when they also create a new table. This function ensures neither will happen.
        """
        df = spark.createDataFrame([], schema)  # DF with 0 rows
        self._append_dataframe(df)
        # we set auto manifest so each job generates its own manifest (necessary for athena retrieval)
        self._metadata_writer.set_table_property(
            self._params.s3_path, "delta.compatibility.symlinkFormatManifest.enabled", "true"
        )

    @_with_delta_retries
    def _append_dataframe(self, df: DataFrame):
        _assert_safe_delta_write_configuration(self._spark)
        df.write.partitionBy(TIME_PARTITION).format("delta").mode("append").save(self._params.s3_path)


class DeltaMetadataWriter:
    def __init__(self, spark: SparkSession):
        self._spark = spark

    @_with_delta_retries
    def generate_symlink_manifest(self, path: str):
        _assert_safe_delta_write_configuration(self._spark)
        self._spark.sql(f"GENERATE symlink_format_manifest FOR TABLE delta.`{path}`")

    @_with_delta_retries
    def set_table_property(self, path, key, val):
        _assert_safe_delta_write_configuration(self._spark)
        # TODO(TEC-11200): fix the "Delta table not found" issue when setting the table properties below
        # and remove the catching of the `AnalysisException`.
        try:
            self._spark.sql(f"ALTER TABLE delta.`{path}` SET TBLPROPERTIES({key}={val})")
        except AnalysisException:
            logger.warning(
                (
                    f"Setting properties '{key}={val}' to the Delta table 'delta.{path}' failed. "
                    "This can result into reading the stale data when using Athena/Snowflake."
                ),
                exc_info=True,
            )


class DeltaReader(OfflineStoreReader):
    def __init__(self, spark: SparkSession, fd: FeatureDefinition):
        self._spark = spark
        assert fd.materialization_enabled and fd.writes_to_offline_store
        self._path = fd.materialized_data_path
        self._window = fd.offline_store_config.delta.time_partition_size.ToTimedelta()

    def read(self, time_limits: Optional[pendulum.Period]):
        spark_df = self._spark.read.format("delta").load(self._path)

        # Delta is always partitioned by TIME_PARTITION. We want to explicitly cast to a timestamp in case:
        #   `spark.sql.sources.partitionColumnTypeInference.enabled` = "false"
        spark_df = spark_df.withColumn(TIME_PARTITION, functions.col(TIME_PARTITION).cast("timestamp"))

        if time_limits is not None:
            start = _unix_timestamp_to_partition(time_limits.start.int_timestamp, self._window)
            end = _unix_timestamp_to_partition(time_limits.end.int_timestamp, self._window)
            partition_col = functions.col(TIME_PARTITION)
            spark_df = spark_df.where((start <= partition_col) & (partition_col <= end))
        return spark_df.drop(TIME_PARTITION)


@dataclass
class TimestampFormats:
    spark_format: str
    python_format: str


def _size_seconds(window: Union[timedelta, pendulum.Duration]):
    if isinstance(window, pendulum.Duration):
        window = window.as_timedelta()
    if window % timedelta(seconds=1) != timedelta(0):
        raise AssertionError(f"partition_size is not a round number of seconds: {window}")
    return int(window.total_seconds())


def _timestamp_formats(partition_size: timedelta):
    if partition_size % timedelta(days=1) == timedelta(0):
        return TimestampFormats(spark_format="yyyy-MM-dd", python_format="%Y-%m-%d")
    else:
        return TimestampFormats(spark_format="yyyy-MM-dd-HH:mm:ss", python_format="%Y-%m-%d-%H:%M:%S")


def _timestamp_to_partition_column(df: DataFrame, time_col: str, partition_size: timedelta, version: int) -> Column:
    # For some insane reason from_unixtime returns a timestamp in the session timezone, so it's pretty annoying to
    # convert a unix time to a formatted UTC timestamp unless the session is set to UTC. This only runs in
    # materialization so we can just assert that that's the case.
    tz = df.sql_ctx.sparkSession.conf.get("spark.sql.session.timeZone")
    if tz not in {"UTC", "Etc/UTC", "GMT"}:
        raise AssertionError(f"spark.sql.session.timeZone must be UTC, not {tz}")
    time_column_type = df.schema[time_col].dataType
    allowed_types = {IntegerType(), TimestampType(), LongType()}
    if time_column_type not in allowed_types:
        raise AssertionError(f"timestamp column must be one of {allowed_types}, not {time_column_type}")
    time_val = functions.col(time_col).cast(LongType())
    if time_col == TEMPORAL_ANCHOR_COLUMN_NAME:
        time_val = convert_epoch_to_datetime(functions.col(time_col), version).cast(LongType())
    aligned = functions.from_unixtime(_align_timestamp(time_val, _size_seconds(partition_size)))
    partition_format = _timestamp_formats(partition_size).spark_format
    return functions.date_format(aligned.cast(TimestampType()), partition_format)


def _unix_timestamp_to_partition(unix_timestamp: int, partition_size: timedelta) -> str:
    dt = pendulum.from_timestamp(_align_timestamp(unix_timestamp, _size_seconds(partition_size)))
    partition_format = _timestamp_formats(partition_size).python_format
    return dt.strftime(partition_format)


def _align_timestamp(int_timestamp_col, window_size):
    return int_timestamp_col - (int_timestamp_col % window_size)
