import datetime
import enum
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
from typing import Union

import attrs
import pendulum

from tecton_core import time_utils
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.query import sql_compat
from tecton_core.query_consts import ANCHOR_TIME
from tecton_proto.args.feature_view_pb2 import OfflineFeatureStoreConfig
from tecton_proto.data.feature_view_pb2 import DeltaOfflineStoreVersion
from tecton_proto.data.feature_view_pb2 import ParquetOfflineStoreVersion


TIME_PARTITION = "time_partition"
SECONDS_TO_NANOSECONDS = 1000 * 1000 * 1000
CONTINUOUS_PARTITION_SIZE_SECONDS = 86400


class PartitionType(str, enum.Enum):
    DATE_STR = "DateString"
    EPOCH = "Epoch"
    # RAW_TIMESTAMP is only used for Snowflake
    RAW_TIMESTAMP = "RawTimestamp"


class OfflineStoreType(str, enum.Enum):
    PARQUET = "parquet"
    DELTA = "delta"
    SNOWFLAKE = "snowflake"


@attrs.frozen
class TimestampFormats:
    spark_format: str
    python_format: str


@attrs.frozen
class OfflineStorePartitionParams:
    partition_by: str
    partition_type: PartitionType
    partition_interval: pendulum.duration


def partition_size_for_parquet(fd: FeatureDefinition) -> pendulum.Duration:
    if fd.offline_store_params is not None:
        return pendulum.Duration(
            seconds=fd.offline_store_params.parquet.time_partition_size.ToTimedelta().total_seconds()
        )
    elif fd.is_continuous:
        return pendulum.Duration(seconds=CONTINUOUS_PARTITION_SIZE_SECONDS)
    else:
        return fd.min_scheduling_interval


def partition_col_for_parquet(fd: FeatureDefinition) -> str:
    offline_store_version = (
        fd.offline_store_params.parquet.version
        if fd.offline_store_params is not None
        else ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_1
    )
    if offline_store_version == ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_1:
        return TIME_PARTITION if fd.is_continuous else ANCHOR_TIME
    elif offline_store_version == ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_2:
        return TIME_PARTITION
    else:
        msg = "unsupported offline store version"
        raise TectonInternalError(msg)


def partition_size_for_delta(fd: FeatureDefinition) -> pendulum.Duration:
    if fd.offline_store_params is not None:
        return pendulum.Duration(
            seconds=fd.offline_store_params.delta.time_partition_size.ToTimedelta().total_seconds()
        )
    else:
        return pendulum.Duration(
            seconds=fd.offline_store_config.delta.time_partition_size.ToTimedelta().total_seconds()
        )


DELTA_SUPPORTED_VERSIONS = [DeltaOfflineStoreVersion.DELTA_OFFLINE_STORE_VERSION_1]

PARQUET_SUPPORTED_VERSIONS = [
    ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_1,
    ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_2,
]


def _check_supported_offline_store_version(fd: FeatureDefinition) -> None:
    if fd.offline_store_params is None:
        return
    if (
        fd.offline_store_params.HasField("delta")
        and fd.offline_store_params.delta.version not in DELTA_SUPPORTED_VERSIONS
    ):
        msg = (
            f"Unsupported offline store version {fd.offline_store_params.delta.version}. Try upgrading your Tecton SDK."
        )
        raise TectonInternalError(msg)
    if (
        fd.offline_store_params.HasField("parquet")
        and fd.offline_store_params.parquet.version not in PARQUET_SUPPORTED_VERSIONS
    ):
        msg = f"Unsupported offline store version {fd.offline_store_params.parquet.version}. Try upgrading your Tecton SDK."
        raise TectonInternalError(msg)


def get_offline_store_type(offline_store_config: OfflineFeatureStoreConfig) -> OfflineStoreType:
    # TODO(TEC-15800): Update Snowflake FV protos to have snowflake as their store type
    if sql_compat.dialect() == sql_compat.Dialect.SNOWFLAKE:
        return OfflineStoreType.SNOWFLAKE

    store_type = offline_store_config.WhichOneof("store_type")
    if store_type == OfflineStoreType.PARQUET:
        return OfflineStoreType.PARQUET
    elif store_type == OfflineStoreType.DELTA:
        return OfflineStoreType.DELTA
    else:
        msg = f"Unknown offline store type {store_type}"
        raise TectonInternalError(msg)


def get_offline_store_partition_params(feature_definition: FeatureDefinition) -> OfflineStorePartitionParams:
    # Examples of how our offline store is partitioned
    ### BWAFV on Delta
    # Partition Column: time_partition
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]

    ### Continuous SWAFV on Parquet
    # Partition Column: time_partition
    # Materialized Columns: timestamp, _anchor_time, [join_keys], [feature_columns]
    # Note: Very weird that we have a timestamp parquet column here - redundant with _anchor_time

    ### BWAFV on Parquet
    # Partition Column: _anchor_time
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]
    # !! In this case we need to drop the partition column from the top level columns

    ### BFV on Parquet
    # Partition Column: _anchor_time
    # Materialized Columns: ts, [join_keys], [feature_columns]

    ### Any FV on Snowflake
    # Partition Column: none
    # Materialized Columns: ts, [join_keys], [feature_columns]

    _check_supported_offline_store_version(feature_definition)
    offline_store_config = feature_definition.offline_store_config
    store_type = get_offline_store_type(offline_store_config)

    if store_type == OfflineStoreType.SNOWFLAKE:
        partition_by = feature_definition.time_key
        partition_type = PartitionType.RAW_TIMESTAMP
        partition_interval = pendulum.Duration(seconds=0)
    elif store_type == OfflineStoreType.DELTA:
        partition_by = TIME_PARTITION
        partition_type = PartitionType.DATE_STR
        partition_interval = partition_size_for_delta(feature_definition)
    elif store_type == OfflineStoreType.PARQUET:
        partition_by = partition_col_for_parquet(feature_definition)
        partition_type = PartitionType.EPOCH
        partition_interval = partition_size_for_parquet(feature_definition)
    else:
        msg = "Unexpected offline store config"
        raise Exception(msg)
    return OfflineStorePartitionParams(partition_by, partition_type, partition_interval)


def timestamp_to_partition_date_str(timestamp: pendulum.DateTime, partition_params: OfflineStorePartitionParams) -> str:
    partition_interval_timedelta = partition_params.partition_interval.as_timedelta()
    aligned_time = time_utils.align_time_downwards(timestamp, partition_interval_timedelta)
    partition_format = timestamp_formats(partition_interval_timedelta).python_format
    return aligned_time.strftime(partition_format)


def timestamp_to_partition_epoch(
    timestamp: pendulum.DateTime,
    partition_params: OfflineStorePartitionParams,
    feature_store_format_version: int,
) -> int:
    aligned_time = time_utils.align_time_downwards(timestamp, partition_params.partition_interval.as_timedelta())
    # align_time_downwards returns the time without tzinfo. convert_timestamp_for_version calls timestamp() which
    # treats naive datetime instances as local time. This can cause an issue if local time is not in UTC.
    aligned_time = aligned_time.replace(tzinfo=datetime.timezone.utc)
    return time_utils.convert_timestamp_for_version(aligned_time, feature_store_format_version)


def window_size_seconds(window: Union[timedelta, pendulum.Duration]) -> int:
    if isinstance(window, pendulum.Duration):
        window = window.as_timedelta()
    if window % timedelta(seconds=1) != timedelta(0):
        msg = f"partition_size is not a round number of seconds: {window}"
        raise AssertionError(msg)
    return int(window.total_seconds())


def timestamp_formats(partition_size: timedelta) -> TimestampFormats:
    if partition_size % timedelta(days=1) == timedelta(0):
        return TimestampFormats(spark_format="yyyy-MM-dd", python_format="%Y-%m-%d")
    else:
        return TimestampFormats(spark_format="yyyy-MM-dd-HH:mm:ss", python_format="%Y-%m-%d-%H:%M:%S")


def datetime_to_partition_str(dt: datetime, partition_size: timedelta) -> str:
    partition_format = timestamp_formats(partition_size).python_format
    return dt.strftime(partition_format)


@dataclass
class OfflineStoreReaderParams:
    path: str


class OfflineStoreReader(ABC):
    @abstractmethod
    def read(self, partition_time_limits: Optional[pendulum.Period] = None) -> "pyarrow.Table":  # noqa: F821
        raise NotImplementedError


class DeltaReader(OfflineStoreReader):
    def __init__(self, params: OfflineStoreReaderParams, fd: FeatureDefinition) -> None:
        self._params = params
        self._partition_size = partition_size_for_delta(fd).as_timedelta()

    def read(self, partition_time_limits: Optional[pendulum.Period] = None) -> "pyarrow.Table":  # noqa: F821
        # TODO(TEC-16757): Move import to top of file.
        from deltalake import DeltaTable

        filters = None
        if partition_time_limits is not None and self._partition_size:
            filters = []
            aligned_start_time = time_utils.align_time_downwards(partition_time_limits.start, self._partition_size)
            start_partition = datetime_to_partition_str(aligned_start_time, self._partition_size)
            filters.append((TIME_PARTITION, ">=", start_partition))

            aligned_end_time = time_utils.align_time_downwards(partition_time_limits.end, self._partition_size)
            end_partition = datetime_to_partition_str(aligned_end_time, self._partition_size)
            filters.append((TIME_PARTITION, "<=", end_partition))

        return DeltaTable(self._params.path).to_pyarrow_table(filters=filters)
