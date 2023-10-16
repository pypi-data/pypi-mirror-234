import functools
import itertools
import logging
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

import pendulum
from py4j.protocol import Py4JJavaError
from pyspark.sql import Column
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import StructType
from pyspark.sql.types import TimestampType

from tecton_core import time_utils as core_time_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.offline_store import TIME_PARTITION
from tecton_core.offline_store import _check_supported_offline_store_version
from tecton_core.offline_store import _timestamp_formats
from tecton_core.offline_store import partition_col_for_parquet
from tecton_core.offline_store import partition_size_for_delta
from tecton_core.offline_store import partition_size_for_parquet
from tecton_core.offline_store import window_size_seconds
from tecton_core.query_consts import ANCHOR_TIME
from tecton_spark import time_utils as spark_time_utils


DBRICKS_MULTI_CLUSTER_WRITES_ENABLED = "spark.databricks.delta.multiClusterWrites.enabled"
DBRICKS_RUNTIME_VERSION = "DATABRICKS_RUNTIME_VERSION"

SPARK_GCS_DELTA_LOGSTORE_CLASS = "io.delta.storage.GCSLogStore"

SPARK31_DELTA_LOGSTORE_CLASS = "spark.delta.logStore.class"
SPARK31_DYNAMODB_LOGSTORE_CLASS = "io.delta.storage.DynamoDBLogStore"

SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS = "spark.delta.logStore.s3.impl"
SPARK32_OR_HIGHER_DYNAMODB_LOGSTORE_CLASS = "io.delta.storage.S3DynamoDBLogStore"

logger = logging.getLogger(__name__)


@dataclass
class OfflineStoreWriterParams:
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
    params: OfflineStoreWriterParams, fd: FeatureDefinition, version: int, spark: SparkSession
):
    """Creates a concrete implementation of OfflineStoreWriter based on fv_config."""
    fv_config = fd.offline_store_config
    case = fv_config.WhichOneof("store_type")
    if case == "delta":
        return DeltaWriter(fd, params, spark, version)
    elif case == "parquet":
        return ParquetWriter(fd, params, spark, version)
    # Remove default after database migration is complete.
    # raise KeyError(case)
    return ParquetWriter(fd, params, spark, version)


def get_offline_store_reader(
    spark: SparkSession, fd: FeatureDefinition, path: Optional[str] = None
) -> "OfflineStoreReader":
    case = fd.offline_store_config.WhichOneof("store_type")
    if case == "delta":
        return DeltaReader(spark, fd, path=path)
    elif case == "parquet":
        return ParquetReader(spark, fd, path=path)
    # Remove default after database migration is complete.
    # raise KeyError(case)
    return ParquetReader(spark, fd, path=path)


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
    def read(self, partition_time_limits: pendulum.Period) -> DataFrame:
        """Note that partition_time_limits only applies partition filtering, so you can have records outside it"""
        raise NotImplementedError


class ParquetWriter(OfflineStoreWriter):
    """Parquet implementation of OfflineStoreWriter"""

    def __init__(self, fd: FeatureDefinition, params: OfflineStoreWriterParams, spark: SparkSession, version: int):
        _check_supported_offline_store_version(fd)
        self._fd = fd
        self._params = params
        self._spark = spark
        self._version = version
        self._partition_size = partition_size_for_parquet(fd).as_timedelta()
        self._partition_col = partition_col_for_parquet(fd)

    def append_dataframe(self, data_frame):
        if self._partition_col == TIME_PARTITION:
            align_duration = core_time_utils.convert_timedelta_for_version(self._partition_size, self._version)
            aligned_time = _align_timestamp(functions.col(ANCHOR_TIME), functions.lit(align_duration))
            data_frame = data_frame.withColumn(TIME_PARTITION, aligned_time)

        data_frame.write.option("partitionOverwriteMode", "dynamic").partitionBy(self._partition_col).parquet(
            self._params.s3_path, mode="overwrite"
        )

    def upsert_dataframe(self, data_frame):
        raise NotImplementedError()

    def delete_keys(self, data_frame):
        raise NotImplementedError()


class ParquetReader(OfflineStoreReader):
    def __init__(self, spark: SparkSession, fd: FeatureDefinition, path: Optional[str]):
        _check_supported_offline_store_version(fd)
        self._spark = spark
        assert fd.materialization_enabled and fd.writes_to_offline_store
        self._path = path or fd.materialized_data_path
        self._partition_col = partition_col_for_parquet(fd)
        self._partition_size = partition_size_for_parquet(fd).as_timedelta()
        self.version = fd.get_feature_store_format_version

    def read(self, partition_time_limits: Optional[pendulum.Period]):
        spark_df = self._spark.read.parquet(self._path)

        # Parquet is partitioned by TIME_PARTITION when is_continuous and ANCHOR_TIME when not.
        # We want to explicitly cast the partition type in case:
        #   `spark.sql.sources.partitionColumnTypeInference.enabled` = "false"

        spark_df = spark_df.withColumn(self._partition_col, functions.col(self._partition_col).cast("long"))

        if partition_time_limits and self._partition_size:
            aligned_start_time = core_time_utils.align_time_downwards(partition_time_limits.start, self._partition_size)
            aligned_end_time = core_time_utils.align_time_downwards(partition_time_limits.end, self._partition_size)
            start_time_epoch = core_time_utils.convert_timestamp_for_version(aligned_start_time, self.version)
            end_time_epoch = core_time_utils.convert_timestamp_for_version(aligned_end_time, self.version)
            partition_col = functions.col(self._partition_col)
            spark_df = spark_df.where((start_time_epoch <= partition_col) & (partition_col <= end_time_epoch))

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
        from delta.exceptions import ConcurrentAppendException
        from delta.exceptions import ConcurrentDeleteDeleteException
        from delta.exceptions import ConcurrentDeleteReadException
        from delta.exceptions import ConcurrentTransactionException
        from delta.exceptions import DeltaConcurrentModificationException
        from delta.exceptions import MetadataChangedException
        from delta.exceptions import ProtocolChangedException

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
        msg = f"Exceeded maximum Delta transaction retries ({max_retries})"
        raise Exception(msg) from final_exception

    return wrapper


def _assert_safe_delta_write_configuration(spark: SparkSession):
    """Asserts that the Spark configuration is such that it is safe to write to Delta concurrently.

    With the Open Source Delta JAR installed (as it is on EMR), writing to a Delta table concurrently with another
    Spark cluster could corrupt the table unless the Delta Logstore class is overridden.

    On Databricks everything is fine as multi-cluster writes are enabled (the default).
    """

    configs = {
        DBRICKS_RUNTIME_VERSION: os.environ.get(DBRICKS_RUNTIME_VERSION, None),
        DBRICKS_MULTI_CLUSTER_WRITES_ENABLED: spark.conf.get(DBRICKS_MULTI_CLUSTER_WRITES_ENABLED, None),
        SPARK31_DELTA_LOGSTORE_CLASS: spark.conf.get(SPARK31_DELTA_LOGSTORE_CLASS, None),
        SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS: spark.conf.get(SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS, None),
    }
    if configs[DBRICKS_RUNTIME_VERSION] and configs[DBRICKS_MULTI_CLUSTER_WRITES_ENABLED] == "true":
        return True

    # either the spark 3.1 or spark 3.2+ DELTA_LOGSTORE_CLASS name can be set
    if configs[SPARK31_DELTA_LOGSTORE_CLASS] in [SPARK31_DYNAMODB_LOGSTORE_CLASS, SPARK_GCS_DELTA_LOGSTORE_CLASS]:
        return True
    if configs[SPARK32_OR_HIGHER_DELTA_LOGSTORE_CLASS] in [
        SPARK32_OR_HIGHER_DYNAMODB_LOGSTORE_CLASS,
        SPARK_GCS_DELTA_LOGSTORE_CLASS,
    ]:
        return True
    msg = f"Configuration is not safe for concurrent writes: {configs}"
    raise AssertionError(msg)


class DeltaWriter(OfflineStoreWriter):
    """DeltaLake implementation of OfflineStoreWriter"""

    def __init__(self, fd: FeatureDefinition, params: OfflineStoreWriterParams, spark: SparkSession, version: int):
        _check_supported_offline_store_version(fd)
        self._params = params
        self._version = version
        self._spark = spark
        self._partition_size = partition_size_for_delta(fd).as_timedelta()
        self._metadata_writer = DeltaMetadataWriter(spark)
        if not spark.conf.get("spark.databricks.delta.commitInfo.userMetadata"):
            msg = "Expected spark.databricks.delta.commitInfo.userMetadata to be set for delta writes"
            raise AssertionError(msg)

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

        aligned_start_time = core_time_utils.align_time_downwards(feature_start_time, self._partition_size)
        aligned_end_time = core_time_utils.align_time_downwards(feature_end_time, self._partition_size)
        start_partition = _datetime_to_partition_str(aligned_start_time, self._partition_size)
        end_partition = _datetime_to_partition_str(aligned_end_time, self._partition_size)
        start_time = core_time_utils.convert_timestamp_for_version(feature_start_time, feature_store_format_version)
        end_time = core_time_utils.convert_timestamp_for_version(feature_end_time, feature_store_format_version)

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
        partition = _timestamp_to_partition_column(
            data_frame, self._params.time_column, self._partition_size, self._version
        )
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

        # Manifest files are not supported on GCS
        if not self._params.s3_path.startswith("gs://"):
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
        # we need spark_catalog in cases where the data source switches catalogs
        self._spark.sql(f"GENERATE symlink_format_manifest FOR TABLE spark_catalog.delta.`{path}`")

    @_with_delta_retries
    def set_table_property(self, path, key, val):
        _assert_safe_delta_write_configuration(self._spark)
        # we need spark_catalog in cases where the data source switches catalogs
        existing_tbl_properties = self._spark.sql(f"show tblproperties spark_catalog.delta.`{path}`").collect()
        # tblproperties are case sensitive
        has_tbl_property = any(key == r.key and val == r.value for r in existing_tbl_properties)
        # we only set it if not already set to avoid delta conflicts
        if not has_tbl_property:
            self._spark.sql(f"ALTER TABLE spark_catalog.delta.`{path}` SET TBLPROPERTIES({key}={val})")


class DeltaReader(OfflineStoreReader):
    def __init__(self, spark: SparkSession, fd: FeatureDefinition, path: Optional[str]):
        _check_supported_offline_store_version(fd)
        self._spark = spark
        assert fd.materialization_enabled and fd.writes_to_offline_store
        self._path = path or fd.materialized_data_path
        self._partition_size = partition_size_for_delta(fd).as_timedelta()

    def read(self, partition_time_limits: Optional[pendulum.Period]):
        spark_df = self._spark.read.format("delta").load(self._path)

        # Whenever the partition filtering logic is changed, also make sure the changes are applied to the sql based
        # version in query/nodes.py

        # Delta is always partitioned by TIME_PARTITION. We want to explicitly cast to a timestamp in case:
        #   `spark.sql.sources.partitionColumnTypeInference.enabled` = "false"
        spark_df = spark_df.withColumn(TIME_PARTITION, functions.col(TIME_PARTITION).cast("timestamp"))

        if partition_time_limits is not None and self._partition_size:
            aligned_start_time = core_time_utils.align_time_downwards(partition_time_limits.start, self._partition_size)
            aligned_end_time = core_time_utils.align_time_downwards(partition_time_limits.end, self._partition_size)
            start_partition = _datetime_to_partition_str(aligned_start_time, self._partition_size)
            end_partition = _datetime_to_partition_str(aligned_end_time, self._partition_size)
            partition_col = functions.col(TIME_PARTITION)
            spark_df = spark_df.where((start_partition <= partition_col) & (partition_col <= end_partition))

        return spark_df.drop(TIME_PARTITION)


def _timestamp_to_partition_column(df: DataFrame, time_col: str, partition_size: timedelta, version: int) -> Column:
    # For some insane reason from_unixtime returns a timestamp in the session timezone, so it's pretty annoying to
    # convert a unix time to a formatted UTC timestamp unless the session is set to UTC. This only runs in
    # materialization so we can just assert that that's the case.
    tz = df.sql_ctx.sparkSession.conf.get("spark.sql.session.timeZone")
    if tz not in {"UTC", "Etc/UTC", "GMT"}:
        msg = f"spark.sql.session.timeZone must be UTC, not {tz}"
        raise AssertionError(msg)
    time_column_type = df.schema[time_col].dataType
    allowed_types = {IntegerType(), TimestampType(), LongType()}
    if time_column_type not in allowed_types:
        msg = f"timestamp column must be one of {allowed_types}, not {time_column_type}"
        raise AssertionError(msg)
    time_val = functions.col(time_col).cast(LongType())
    if time_col == ANCHOR_TIME:
        time_val = spark_time_utils.convert_epoch_to_datetime(functions.col(time_col), version).cast(LongType())
    aligned = functions.from_unixtime(_align_timestamp(time_val, window_size_seconds(partition_size)))
    partition_format = _timestamp_formats(partition_size).spark_format
    return functions.date_format(aligned.cast(TimestampType()), partition_format)


def _datetime_to_partition_str(dt: datetime, partition_size: timedelta) -> str:
    partition_format = _timestamp_formats(partition_size).python_format
    return dt.strftime(partition_format)


def _align_timestamp(int_timestamp_col, window_size):
    return int_timestamp_col - (int_timestamp_col % window_size)
