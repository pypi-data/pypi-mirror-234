"""Configs and dataclasses used to construct Tecton objects.

Classes in this file should be simple data classes (i.e. do not have much functionality) and should not depend directly
on Tecton objects (to avoid circular dependencies).
"""
import datetime
import functools
import inspect
import json
from enum import Enum
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attrs
from google.protobuf.struct_pb2 import Struct
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from typeguard import typechecked

from tecton._internals.repo import function_serialization
from tecton.aggregation_functions import AggregationFunction
from tecton.types import Field
from tecton_core import feature_view_utils
from tecton_core import time_utils
from tecton_core.filter_context import FilterContext
from tecton_proto.args import data_source_pb2
from tecton_proto.args import feature_service_pb2
from tecton_proto.args import feature_view_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_spark import data_source_helper
from tecton_spark import spark_schema_wrapper


AVAILABILITY_SPOT = "spot"
AVAILABILITY_ON_DEMAND = "on_demand"
AVAILABILITY_SPOT_FALLBACK = "spot_with_fallback"
DATABRICKS_SUPPORTED_AVAILABILITY = {AVAILABILITY_SPOT, AVAILABILITY_ON_DEMAND, AVAILABILITY_SPOT_FALLBACK}
EMR_SUPPORTED_AVAILABILITY = {AVAILABILITY_SPOT, AVAILABILITY_ON_DEMAND, AVAILABILITY_SPOT_FALLBACK}


class SparkVersions(str, Enum):
    Emr6_5 = "emr-6.5.0"
    Emr6_7 = "emr-6.7.0"
    Emr6_9 = "emr-6.9.0"
    Dbr11_3 = "11.3.x-scala2.12"
    Dbr10_4 = "10.4.x-scala2.12"
    Dbr9_1 = "9.1.x-scala2.12"


DEFAULT_SPARK_VERSIONS = {"databricks_spark_version": SparkVersions.Dbr10_4, "emr_spark_version": SparkVersions.Emr6_7}
EMR_SUPPORTED_SPARK = {SparkVersions.Emr6_5, SparkVersions.Emr6_7, SparkVersions.Emr6_9}
DATABRICKS_SUPPORTED_SPARK = {SparkVersions.Dbr10_4, SparkVersions.Dbr9_1, SparkVersions.Dbr11_3}


@attrs.define(auto_attribs=True)
class ExistingClusterConfig:
    """Use an existing Databricks cluster.

    :param existing_cluster_id: ID of the existing cluster.
    """

    existing_cluster_id: str

    def _to_proto(self) -> feature_view_pb2.ExistingClusterConfig:
        proto = feature_view_pb2.ExistingClusterConfig()
        proto.existing_cluster_id = self.existing_cluster_id

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(existing_cluster=self._to_proto())


def _to_json_cluster_proto(json_str) -> feature_view_pb2.JsonClusterConfig:
    json_struct = Struct()
    json_struct.update(json.loads(json_str))
    return feature_view_pb2.JsonClusterConfig(json=json_struct)


@attrs.define(auto_attribs=True)
class EMRJsonClusterConfig:
    """Configuration used to specify materialization clusters using json on EMR.

    This class describes the attributes of the new clusters which are created in EMR during
    materialization jobs. Please find more details in `User Guide`_.

    :param json: A JSON string used to directly configure the cluster used in materialization.

    .. _User Guide: https://docs.tecton.ai/docs/materializing-features/configuring-job-clusters-via-json#configuring-emr-job-clusters
    """

    json: Optional[str] = None

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        if self.json is None:
            raise ValueError("Missing input JSON string")
        return feature_view_pb2.ClusterConfig(json_emr=_to_json_cluster_proto(self.json))


@attrs.define(auto_attribs=True)
class EMRClusterConfig:
    """Configuration used to specify materialization cluster options on EMR.

    This class describes the attributes of the new clusters which are created in EMR during
    materialization jobs. You can configure options of these clusters, like cluster size and extra pip dependencies.

    :param instance_type: Instance type for the cluster. Must be a valid type as listed in https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-supported-instance-types.html.
        Additionally, Graviton instances such as the m6g family are not supported. If not specified, a value determined by the Tecton backend is used.
    :param instance_availability: Instance availability for the cluster : "spot", "on_demand", or "spot_with_fallback".
        If not specified, default is spot.
    :param number_of_workers: Number of instances for the materialization job. If not specified, a value determined by the Tecton backend is used
    :param first_on_demand: The first `first_on_demand` nodes of the cluster will use on_demand instances. The rest will use the type specified by instance_availability.
        If first_on_demand >= 1, the master node will use on_demand instance type. `first_on_demand` is recommended to be set >= 1 for cluster configs for critical streaming features.
    :param root_volume_size_in_gb: Size of the root volume in GB per instance for the materialization job.
        If not specified, a value determined by the Tecton backend is used.
    :param extra_pip_dependencies: Extra pip dependencies to be installed on the materialization cluster. Must be PyPI packages, or wheels/eggs in S3 or DBFS.
    :param spark_config: Map of Spark configuration options and their respective values that will be passed to the
        FeatureView materialization Spark cluster.
    :param emr_version: EMR version of the cluster. Supported versions include "emr-6.9.0", "emr-6.7.0" and "emr-6.5.0". (Default: emr-6.7.0)

    Note on ``extra_pip_dependencies``: This is a list of packages that will be installed during materialization.
    To use PyPI packages, specify the package name and optionally the version, e.g. ``"tensorflow"`` or ``"tensorflow==2.2.0"``.
    To use custom code, package it as a Python wheel or egg file in S3 or DBFS, then specify the path to the file,
    e.g. ``"s3://my-bucket/path/custom.whl"``, or ``"dbfs:/path/to/custom.whl"``.

    These libraries will only be available to use inside Spark UDFs. For example, if you set
    ``extra_pip_dependencies=["tensorflow"]``, you can use it in your transformation as shown below.

    An example of EMRClusterConfig.

    .. code-block:: python

        from tecton import batch_feature_view, Input, EMRClusterConfig

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            # Can be an argument instance to a batch feature view decorator
            batch_compute = EMRClusterConfig(
                instance_type = 'm5.2xlarge',
                number_of_workers=4,
                extra_pip_dependencies=["tensorflow==2.2.0"],
            ),
            # Other named arguments to batch feature view
            ...
        )

        # Use the tensorflow package in the UDF since tensorflow will be installed
        # on the EMR Spark cluster. The import has to be within the UDF body. Putting it at the
        # top of the file or inside transformation function won't work.

        @transformation(mode='pyspark')
        def test_transformation(transformation_input):
            from pyspark.sql import functions as F
            from pyspark.sql.types import IntegerType

            def my_tensorflow(x):
                import tensorflow as tf
                return int(tf.math.log1p(float(x)).numpy())

            my_tensorflow_udf = F.udf(my_tensorflow, IntegerType())

            return transformation_input.select(
                'entity_id',
                'timestamp',
                my_tensorflow_udf('clicks').alias('log1p_clicks')
            )
    """

    instance_type: Optional[str] = None
    instance_availability: Optional[str] = None
    number_of_workers: Optional[int] = None
    first_on_demand: Optional[int] = None
    root_volume_size_in_gb: Optional[int] = None
    extra_pip_dependencies: Optional[List[str]] = None
    spark_config: Optional[Dict[str, str]] = None
    emr_version: str = DEFAULT_SPARK_VERSIONS["emr_spark_version"]

    def _to_proto(self) -> feature_view_pb2.NewClusterConfig:
        proto = feature_view_pb2.NewClusterConfig()
        if self.instance_type:
            proto.instance_type = self.instance_type
        if self.instance_availability:
            if self.instance_availability not in EMR_SUPPORTED_AVAILABILITY:
                raise ValueError(
                    f"Instance availability {self.instance_availability} is not supported. Choose one of {EMR_SUPPORTED_AVAILABILITY}"
                )
            proto.instance_availability = self.instance_availability
        if self.emr_version not in EMR_SUPPORTED_SPARK:
            raise ValueError(
                f"EMR version {self.emr_version} is not supported. Supported versions: {EMR_SUPPORTED_SPARK}"
            )
        if self.number_of_workers:
            proto.number_of_workers = self.number_of_workers
        if self.first_on_demand:
            proto.first_on_demand = self.first_on_demand
        if self.root_volume_size_in_gb:
            proto.root_volume_size_in_gb = self.root_volume_size_in_gb
        if self.extra_pip_dependencies:
            proto.extra_pip_dependencies.extend(self.extra_pip_dependencies)
        if self.spark_config:
            spark_config = SparkConfigWrapper(self.spark_config)._to_proto()
            proto.spark_config.CopyFrom(spark_config)
        proto.pinned_spark_version = self.emr_version

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(new_emr=self._to_proto())


@attrs.define(auto_attribs=True)
class DatabricksJsonClusterConfig:
    """Configuration used to specify materialization clusters using json on Databricks.

    This class describes the attributes of the new clusters which are created in Databricks during
    materialization jobs. Please find more details in `User Guide`_.

    :param json: A JSON string used to directly configure the cluster used in materialization.

    .. _User Guide: https://docs.tecton.ai/docs/materializing-features/configuring-job-clusters-via-json#configuring-databricks-job-clusters
    """

    json: Optional[str] = None

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        if self.json is None:
            raise ValueError("Missing input JSON string")
        return feature_view_pb2.ClusterConfig(json_databricks=_to_json_cluster_proto(self.json))


@attrs.define(auto_attribs=True)
class DatabricksClusterConfig:
    """Configuration used to specify materialization cluster options on Databricks.

    This class describes the attributes of the new clusters which are created in Databricks during
    materialization jobs. You can configure options of these clusters, like cluster size and extra pip dependencies.

    :param instance_type: Instance type for the cluster. Must be a valid type as listed in https://databricks.com/product/aws-pricing/instance-types.
        Additionally, Graviton instances such as the m6g family are not supported. If not specified, a value determined by the Tecton backend is used.
    :param instance_availability: Instance availability for the cluster : "spot", "on_demand", or "spot_with_fallback".
        If not specified, default is spot.
    :param first_on_demand: The first `first_on_demand` nodes of the cluster will use on_demand instances. The rest will use the type specified by instance_availability.
        If first_on_demand >= 1, the driver node use on_demand instance type.
    :param number_of_workers: Number of instances for the materialization job. If not specified, a value determined by the Tecton backend is used.
        If set to 0 then jobs will be run in single-node clusters.
    :param root_volume_size_in_gb: Size of the root volume in GB per instance for the materialization job.
        If not specified, a value determined by the Tecton backend is used.
    :param extra_pip_dependencies: Extra pip dependencies to be installed on the materialization cluster. Must be PyPI packages, or wheels/eggs in S3 or DBFS.
    :param spark_config: Map of Spark configuration options and their respective values that will be passed to the
        FeatureView materialization Spark cluster.
    :param dbr_version: DBR version of the cluster. Supported versions include 9.1.x-scala2.12, 10.4.x-scala2.12, and 11.3.x-scala2.12. (Default: 10.4.x-scala2.12)

    Note on ``extra_pip_dependencies``: This is a list of packages that will be installed during materialization.
    To use PyPI packages, specify the package name and optionally the version, e.g. ``"tensorflow"`` or ``"tensorflow==2.2.0"``.
    To use custom code, package it as a Python wheel or egg file in S3 or DBFS, then specify the path to the file,
    e.g. ``"s3://my-bucket/path/custom.whl"``, or ``"dbfs:/path/to/custom.whl"``.

    These libraries will only be available to use inside Spark UDFs. For example, if you set
    ``extra_pip_dependencies=["tensorflow"]``, you can use it in your transformation as shown below.

    An example of DatabricksClusterConfig.

    .. code-block:: python

        from tecton import batch_feature_view, Input, DatabricksClusterConfig

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            # Can be an argument instance to a batch feature view decorator
            batch_compute = DatabricksClusterConfig(
                instance_type = 'm5.2xlarge',
                spark_config = {"spark.executor.memory" : "12g"}
                extra_pip_dependencies=["tensorflow"],
            ),
            # Other named arguments to batch feature view
            ...
        )

        # Use the tensorflow package in the UDF since tensorflow will be installed
        # on the Databricks Spark cluster. The import has to be within the UDF body. Putting it at the
        # top of the file or inside transformation function won't work.

        @transformation(mode='pyspark')
        def test_transformation(transformation_input):
            from pyspark.sql import functions as F
            from pyspark.sql.types import IntegerType

            def my_tensorflow(x):
                import tensorflow as tf
                return int(tf.math.log1p(float(x)).numpy())

            my_tensorflow_udf = F.udf(my_tensorflow, IntegerType())

            return transformation_input.select(
                'entity_id',
                'timestamp',
                my_tensorflow_udf('clicks').alias('log1p_clicks')
            )

    """

    instance_type: Optional[str] = None
    instance_availability: Optional[str] = None
    number_of_workers: Optional[int] = None
    first_on_demand: Optional[int] = None
    root_volume_size_in_gb: Optional[int] = None
    extra_pip_dependencies: Optional[List[str]] = None
    spark_config: Optional[Dict[str, str]] = None
    dbr_version: str = DEFAULT_SPARK_VERSIONS["databricks_spark_version"]

    def _to_proto(self) -> feature_view_pb2.NewClusterConfig:
        proto = feature_view_pb2.NewClusterConfig()
        if self.instance_type:
            proto.instance_type = self.instance_type
        if self.instance_availability:
            if self.instance_availability not in DATABRICKS_SUPPORTED_AVAILABILITY:
                raise ValueError(
                    f"Instance availability {self.instance_availability} is not supported. Choose {AVAILABILITY_SPOT}, {AVAILABILITY_ON_DEMAND} or {AVAILABILITY_SPOT_FALLBACK}"
                )
            proto.instance_availability = self.instance_availability
        if self.dbr_version not in DATABRICKS_SUPPORTED_SPARK:
            raise ValueError(
                f"Databricks version {self.dbr_version} is not supported. Supported versions: {DATABRICKS_SUPPORTED_SPARK}"
            )

        if self.number_of_workers is not None:
            proto.number_of_workers = self.number_of_workers
        if self.root_volume_size_in_gb:
            proto.root_volume_size_in_gb = self.root_volume_size_in_gb
        if self.first_on_demand:
            proto.first_on_demand = self.first_on_demand
        if self.extra_pip_dependencies:
            # Pretty easy to do e.g. extra_pip_dependencies="tensorflow" by mistake and end up with
            # [t, e, n, s, o, r, f, l, o, w] as a list of dependencies passed to the Spark job.
            #
            # Since this is annoying to debug, we check for that here.
            if isinstance(self.extra_pip_dependencies, str):
                raise ValueError("extra_pip_dependencies must be a list")
            proto.extra_pip_dependencies.extend(self.extra_pip_dependencies)
        if self.spark_config:
            spark_config = SparkConfigWrapper(self.spark_config)._to_proto()
            proto.spark_config.CopyFrom(spark_config)
        proto.pinned_spark_version = self.dbr_version

        return proto

    def _to_cluster_proto(self) -> feature_view_pb2.ClusterConfig:
        return feature_view_pb2.ClusterConfig(new_databricks=self._to_proto())


@attrs.define(auto_attribs=True)
class SparkConfigWrapper:
    spark_config_map: Dict[str, str]

    HARDCODED_OPTS = {
        "spark.driver.memory": "spark_driver_memory",
        "spark.executor.memory": "spark_executor_memory",
        "spark.driver.memoryOverhead": "spark_driver_memory_overhead",
        "spark.executor.memoryOverhead": "spark_executor_memory_overhead",
    }

    def _to_proto(self):
        proto = feature_view_pb2.SparkConfig()
        for opt, val in self.spark_config_map.items():
            if opt in self.HARDCODED_OPTS:
                setattr(proto, self.HARDCODED_OPTS[opt], val)
            else:
                proto.spark_conf[opt] = val

        return proto


@attrs.define(auto_attribs=True)
class ParquetConfig:
    """(Config Class) ParquetConfig Class.

    This class describes the attributes of Parquet-based offline feature store storage for the feature definition.

    :param subdirectory_override: This is for the location of the feature data in the offline store. By default, all feature views will be under the subdirectory <workspace_name> if this param is not specified.
    """

    subdirectory_override: Optional[str] = None

    def _to_proto(self):
        store_config = feature_view_pb2.OfflineFeatureStoreConfig()
        store_config.parquet.SetInParent()
        if self.subdirectory_override:
            store_config.subdirectory_override = self.subdirectory_override
        return store_config


@attrs.define(auto_attribs=True)
class DeltaConfig:
    """(Config Class) DeltaConfig Class.

    This class describes the attributes of DeltaLake-based offline feature store storage for the feature definition.

    :param time_partition_size: The size of a time partition in the DeltaLake table, specified as a datetime.timedelta. Defaults to 24 hours.
    :param subdirectory_override: This is for the location of the feature data in the offline store. By default, all feature views will be under the subdirectory <workspace_name> if this param is not specified.
    """

    time_partition_size: Optional[datetime.timedelta] = datetime.timedelta(hours=24)
    subdirectory_override: Optional[str] = None

    def _to_proto(self):
        store_config = feature_view_pb2.OfflineFeatureStoreConfig()
        store_config.delta.time_partition_size.FromTimedelta(self.time_partition_size)
        if self.subdirectory_override:
            store_config.subdirectory_override = self.subdirectory_override
        return store_config


@attrs.define(auto_attribs=True)
class DynamoConfig:
    """(Config Class) DynamoConfig Class.

    This class describes the attributes of DynamoDB based online feature store for the feature definition.
    Currently there are no attributes for this class.
    Users can specify online_store = DynamoConfig()
    """

    def _to_proto(self):
        store_config = feature_view_pb2.OnlineStoreConfig()
        store_config.dynamo.enabled = True
        store_config.dynamo.SetInParent()
        return store_config


@attrs.define(auto_attribs=True)
class RedisConfig:
    """(Config Class) RedisConfig Class.

    This class describes the attributes of Redis-based online feature store for the feature definition.
    Note : Your Tecton deployment needs to be connected to Redis before you can use this configuration option. See https://docs.tecton.ai/docs/setting-up-tecton/setting-up-other-components/connecting-redis-as-an-online-store for details and please contact Tecton Support if you need assistance.

    :param primary_endpoint: Primary endpoint for the Redis Cluster. This is optional and if absent, Tecton will use the default Redis Cluster configured for your deployment.
    :param authentication_token: Authentication token for the Redis Cluster, must be provided if primary_endpoint is present.
    """

    primary_endpoint: Optional[str] = None
    authentication_token: Optional[str] = None

    def _to_proto(self):
        # TODO(TEC-13889): Remove the tls_enabled field from proto and backend as this should always be set to true
        tls_enabled = True if self.authentication_token else False
        return feature_view_pb2.OnlineStoreConfig(
            redis=feature_view_pb2.RedisOnlineStore(
                enabled=True,
                primary_endpoint=self.primary_endpoint,
                authentication_token=self.authentication_token,
                tls_enabled=tls_enabled,
            )
        )


@attrs.define(auto_attribs=True)
class MonitoringConfig:
    """Configuration used to specify monitoring options.

    This class describes the FeatureView materialization freshness and alerting configurations. Requires
    materialization to be enabled. Freshness monitoring requires online materialization to be enabled.
    See `Monitoring Materialization`_ for more details.

    :param monitor_freshness: Defines the enabled/disabled state of monitoring when feature data is materialized to the online feature store.
    :type monitor_freshness: bool
    :param expected_freshness: Threshold used to determine if recently materialized feature data is stale.
        Data is stale if ``now - anchor_time(most_recent_feature_value) > expected_freshness``.
        Value must be at least 2 times the feature tile length.
        If not specified, a value determined by the Tecton backend is used
    :type expected_freshness: timedelta, optional
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :type alert_email: str, optional

    An example declaration of a MonitorConfig

        .. code-block:: python

            from datetime import timedelta
            from tecton import batch_feature_view, Input, MonitoringConfig
            # For all named arguments to the batch feature view, see docs for details and types.
            @batch_feature_view(
                sources=[FilteredSource(credit_scores_batch)],
                # Can be an argument instance to a batch feature view decorator
                monitoring = MonitoringConfig(
                    monitor_freshness=True,
                    expected_freshness=timedelta(weeks=1),
                    alert_email="brian@tecton.ai"
                ),
                # Other named arguments
                ...
            )

            # Your batch feature view function
            def credit_batch_feature_view(credit_scores):
              ...

    .. _Monitoring Materialization: https://docs.tecton.ai/v2/overviews/monitoring_materialization.html
    """

    monitor_freshness: bool
    expected_freshness: Optional[datetime.timedelta] = None
    alert_email: Optional[str] = None

    def _to_proto(self) -> feature_view_pb2.MonitoringConfig:
        proto = feature_view_pb2.MonitoringConfig()

        if self.expected_freshness:
            proto.expected_freshness.FromTimedelta(self.expected_freshness)

        proto.alert_email = self.alert_email or ""
        proto.monitor_freshness = self.monitor_freshness
        return proto


@attrs.define(auto_attribs=True)
class LoggingConfig(object):
    """
    Configuration used to describe feature and request logging for Feature Services.

    :param sample_rate: The rate of logging features. Must be between (0, 1]. Defaults to 1.
    :param log_effective_times: Whether to log the timestamps of the last update of the logged feature values. Defaults to False.

    An example of LoggingConfig declaration as part of FeatureService

    .. code-block:: Python

        from tecton import FeatureService, LoggingConfig

        # LoggingConfig is normaly used as a named argument parameter to a FeatureService instance definition.
        my_feature_service = FeatureService(
            name="An example of Feature Service"
            # Other named arguments
            ...
            # A LoggingConfig instance
            logging=LoggingConfig(
                    sample_rate=0.5,
                    log_effective_times=False,
            )
            ...
        )
    """

    sample_rate: float = attrs.field(default=1.0, validator=attrs.validators.instance_of((float, int)))
    log_effective_times: bool = attrs.field(default=False, validator=attrs.validators.instance_of(bool))

    def _to_proto(self) -> feature_service_pb2.LoggingConfigArgs:
        return feature_service_pb2.LoggingConfigArgs(
            sample_rate=self.sample_rate, log_effective_times=self.log_effective_times
        )

    @classmethod
    def _from_proto(cls, logging_config_proto: feature_service_pb2.LoggingConfigArgs) -> "LoggingConfig":
        return LoggingConfig(logging_config_proto.sample_rate, logging_config_proto.log_effective_times)


class OutputStream:
    """Base class for output stream configs."""

    def _to_proto() -> feature_view_pb2.OutputStream:
        raise NotImplementedError


@attrs.define(auto_attribs=True)
class KinesisOutputStream(OutputStream):
    """Configuration used for a Kinesis output stream.

    :param stream_name: Name of the Kinesis stream.
    :param region: AWS region of the stream, e.g: "us-west-2".
    :param options: A map of additional Spark readStream options. Only `roleArn` is supported.
    :param include_features: Return feature values in addition to entity keys. Not supported for window aggregate Feature Views.
    """

    stream_name: str
    region: str
    options: Optional[Dict[str, str]] = None
    include_features: bool = False

    def _to_proto(self) -> feature_view_pb2.OutputStream:
        args = data_source_pb2.KinesisDataSourceArgs(
            stream_name=self.stream_name,
            region=self.region,
        )
        options = self.options or {}
        for key in sorted(options.keys()):
            option = data_source_pb2.Option(
                key=key,
                value=options[key],
            )
            args.options.append(option)

        return feature_view_pb2.OutputStream(
            include_features=self.include_features,
            kinesis=args,
        )


@attrs.define(auto_attribs=True)
class KafkaOutputStream(OutputStream):
    """Configuration used for a Kafka output stream.

    :param kafka_bootstrap_servers: The list of bootstrap servers for your Kafka brokers, e.g: "abc.xyz.com:xxxx,abc2.xyz.com:xxxx".
    :param topics: A comma-separated list of Kafka topics the record will be appended to. Currently only supports one topic.
    :param options: A map of additional Spark readStream options. Only `roleArn` is supported at the moment.
    :param include_features: Return feature values in addition to entity keys. Not supported for window aggregate Feature Views.
    """

    kafka_bootstrap_servers: str
    topics: str
    options: Optional[Dict[str, str]] = None
    include_features: bool = False

    def _to_proto(self) -> feature_view_pb2.OutputStream:
        args = data_source_pb2.KafkaDataSourceArgs(
            kafka_bootstrap_servers=self.kafka_bootstrap_servers,
            topics=self.topics,
        )
        options = self.options or {}
        for key in sorted(options.keys()):
            option = data_source_pb2.Option(
                key=key,
                value=options[key],
            )
            args.options.append(option)

        return feature_view_pb2.OutputStream(
            include_features=self.include_features,
            kafka=args,
        )


# NOTE: When adding a new format, change data_source_helper.py:_partition_value_for_time if needed
@attrs.define(auto_attribs=True)
class DatetimePartitionColumn:
    """Helper class to tell Tecton how underlying flat files are date/time partitioned for Hive/Glue data sources. This can translate into a significant performance increase.

    You will generally include an object of this class in the ``datetime_partition_columns`` option in a :class:`HiveConfig` object.

    :param column_name: The name of the column in the Glue/Hive schema that corresponds to the underlying date/time partition folder. Note that if you do not explicitly specify a name in your partition folders, Glue will name the column of the form ``partition_0``.
    :param datepart: The part of the date that this column specifies. Can be one of "year", "month", "day", "hour", or the full "date". If used with ``format_string``, this should be the size of partition being represented, e.g. ``datepart="month"`` for ``format_string="%Y-%m"``.
    :param zero_padded: Whether the ``datepart`` has a leading zero if less than two digits. This must be set to True if ``datepart="date"``. (Should not be set if ``format_string`` is set.)
    :param format_string:
        A ``datetime.strftime`` format string override for "non-default" partition columns formats. E.g. ``"%Y%m%d"`` for ``datepart="date"`` instead of the Tecton default ``"%Y-%m-%d"``, or ``"%Y-%m"`` for ``datepart="month"`` instead of the Tecton default ``"%m"``.

        IMPORTANT: This format string must convert python datetimes (via ``datetime.strftime(format)``) to strings that are sortable in time order. For example, ``"%m-%Y"`` would be an invalid format string because ``"09-2019" > "05-2020"``.

        See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes for format codes.

    Example definitions:

        Assume you have an S3 bucket with parquet files stored in the following structure: ``s3://mybucket/2022/05/04/<multiple parquet files>`` , where ``2022`` is the year, ``05`` is the month, and ``04`` is the day of the month. In this scenario, you could use the following definition:

        .. code-block:: python

            datetime_partition_columns = [
                DatetimePartitionColumn(column_name="partition_0", datepart="year", zero_padded=True),
                DatetimePartitionColumn(column_name="partition_1", datepart="month", zero_padded=True),
                DatetimePartitionColumn(column_name="partition_2", datepart="day", zero_padded=True),
            ]
            batch_config = HiveConfig(
                database='my_db',
                table='my_table',
                timestamp_field='timestamp',
                datetime_partition_columns=datetime_partition_columns,
            )

        Example using the ``format_string`` parameter. Assume your data is partitioned by ``"YYYY-MM"``, e.g. ``s3://mybucket/2022-05/<multiple parquet files>``. Tecton's default month format is ``"%m"``, which would fail to format datetime strings that are comparable to your table's partition column, so the definition needs to specify an override.

        .. code-block:: python

            datetime_partition_columns = [
                DatetimePartitionColumn(column_name="partition_1", datepart="month", format_string="%Y-%m"),
            ]
    """

    #: The name of the column in the Glue/Hive schema that corresponds to the underlying date/time partition folder.
    column_name: str

    #: The part of the date that this column specifies. Can be one of "year", "month", "day", "hour", or the full "date".
    datepart: str

    #: Whether the ``datepart`` has a leading zero if less than two digits.
    zero_padded: bool = False

    #: A ``datetime.strftime`` format string override for "non-default" partition columns formats.
    format_string: Optional[str] = None


@attrs.define(frozen=True)
class RequestSource:
    """Declare a ``RequestSource``, for using request-time data in an ``OnDemandFeatureView``.

    Example of a RequestSource declaration:

    .. code-block:: python

        from tecton import RequestSource
        from tecton.types import Field, Float64

        schema = [Field('amount', Float64)]
        transaction_request = RequestSource(schema=schema)


    Attributes:
        schema: The schema of this Request Source.
    """

    schema: List[Field]


class BaseStreamConfig:
    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        raise NotImplementedError


class BaseBatchConfig:
    @property
    def data_delay(self) -> datetime.timedelta:
        raise NotImplementedError

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        raise NotImplementedError


class FileConfig(BaseBatchConfig):
    """
    Configuration used to reference a file or directory (S3, etc.)

    The FileConfig class is used to create a reference to a file or directory of files in S3,
    HDFS, or DBFS.

    The schema of the data source is inferred from the underlying file(s). It can also be modified using the
    ``post_processor`` parameter.

    This class is used as an input to a :class:`BatchSource`'s parameter ``batch_config``. Declaring this configuration class alone
    will not register a Data Source. Instead, declare as a part of ``BatchSource`` that takes this configuration class
    instance as a parameter.
    """

    def __init__(
        self,
        uri: str,
        file_format: str,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        schema_uri: Optional[str] = None,
        schema_override: Optional[StructType] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
    ):
        """
        Instantiates a new FileConfig.

        :param uri: S3 or HDFS path to file(s).
        :param file_format: File format. "json", "parquet", or "csv"
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                to filter data from this source, before any feature view transformations are applied.
                                Only required if this source is used with `FilteredSource`.
        :param timestamp_format: Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param post_processor: Python user defined function ``f(DataFrame) -> DataFrame`` that takes in raw
                                     Pyspark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param schema_uri: A file or subpath of "uri" that can be used for fast schema inference.
                           This is useful for speeding up plan computation for highly partitioned data sources containing many files.
        :param schema_override: A pyspark.sql.types.StructType object that will be used as the schema when
                                reading from the file. If omitted, the schema will be inferred automatically.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                batch schedule period. This parameter configures how long they wait after the end
                                of the period before starting, typically to ensure that all data has landed.
                                For example, if a feature view has a `batch_schedule` of 1 day and one of
                                the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                incremental materialization jobs will run at `01:00` UTC.
        :return: A FileConfig class instance.

        Example of a FileConfig declaration:

        .. code-block:: python

            from tecton import FileConfig, BatchSource

            def convert_temperature(df):
                from pyspark.sql.functions import udf,col
                from pyspark.sql.types import DoubleType

                # Convert the incoming PySpark DataFrame temperature Celsius to Fahrenheit
                udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
                converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
                return converted_df

            # declare a FileConfig, which can be used as a parameter to a `BatchSource`
            ad_impressions_file_ds = FileConfig(uri="s3://tecton.ai.public/data/ad_impressions_sample.parquet",
                                                file_format="parquet",
                                                timestamp_field="timestamp",
                                                post_processor=convert_temperature)

            # This FileConfig can then be included as an parameter a BatchSource declaration.
            # For example,
            ad_impressions_batch = BatchSource(name="ad_impressions_batch",
                                               batch_config=ad_impressions_file_ds)

        """
        self._args = data_source_pb2.FileDataSourceArgs()
        self._args.uri = uri
        self._args.file_format = file_format
        if schema_uri is not None:
            self._args.schema_uri = schema_uri
        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            self._args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            self._args.common_args.timestamp_field = timestamp_field
        if timestamp_format:
            self._args.timestamp_format = timestamp_format
        if schema_override:
            self._args.schema_override.CopyFrom(spark_schema_wrapper.SparkSchemaWrapper(schema_override).to_proto())

        self._args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self) -> datetime.timedelta:
        """Returns the duration that materialization jobs wait after the batch_schedule before starting, typically to ensure that all data has landed."""
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.file_ds_config.CopyFrom(self._args)


class KafkaConfig(BaseStreamConfig):
    """
    Configuration used to reference a Kafka stream.

    The KafkaConfig class is used to create a reference to a Kafka stream.

    This class is used as an input to a :class:`StreamSource`'s parameter ``stream_config``. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of ``StreamSource`` that takes this configuration
    class instance as a parameter.

    """

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        topics: str,
        post_processor,
        timestamp_field: str,
        watermark_delay_threshold: datetime.timedelta = datetime.timedelta(hours=24),
        options: Optional[Dict[str, str]] = None,
        ssl_keystore_location: Optional[str] = None,
        ssl_keystore_password_secret_id: Optional[str] = None,
        ssl_truststore_location: Optional[str] = None,
        ssl_truststore_password_secret_id: Optional[str] = None,
        security_protocol: Optional[str] = None,
        deduplication_columns: Optional[List[str]] = None,
    ):
        """
        Instantiates a new KafkaConfig.

        :param kafka_bootstrap_servers: A comma-separated list of the Kafka bootstrap server addresses. Passed directly
                                        to the Spark ``kafka.bootstrap.servers`` option.
        :param topics: A comma-separated list of Kafka topics to subscribe to. Passed directly to the Spark ``subscribe``
                       option.
        :param post_processor: Python user defined function ``f(DataFrame) -> DataFrame`` that takes in raw
                                      Pyspark data source DataFrame and translates it to the DataFrame to be
                                      consumed by the Feature View. See an example of
                                      post_processor in the `User Guide`_.
        :param timestamp_field: Name of the column containing timestamp for watermarking.
        :param watermark_delay_threshold: (Default: 24h) Watermark time interval, e.g: timedelta(hours=36), used by Spark Structured Streaming to account for late-arriving data. See: `Productionizing a Stream`_.
        :param options: A map of additional Spark readStream options
        :param ssl_keystore_location: An DBFS (Databricks only) or S3 URI that points to the keystore file that should be used for SSL brokers. Note for S3 URIs, this must be configured by your Tecton representative.
            Example: ``s3://tecton-<deployment name>/kafka-credentials/kafka_client_keystore.jks``
            Example: ``dbfs:/kafka-credentials/kafka_client_keystore.jks``
        :param ssl_keystore_password_secret_id: The config key for the password for the Keystore.
            Should start with ``SECRET_``, example: ``SECRET_KAFKA_PRODUCTION``.
        :param ssl_truststore_location: An DBFS (Databricks only) or S3 URI that points to the truststore file that should be used for SSL brokers. Note for S3 URIs, this must be configured by your Tecton representative. If not provided, the default truststore for your compute provider will be used. Note that this is required for AWS-signed keystores on Databricks.
            Example: ``s3://tecton-<deployment name>/kafka-credentials/kafka_client_truststore.jks``
            Example: ``dbfs:/kafka-credentials/kafka_client_truststore.jks``
        :param ssl_truststore_password_secret_id (Optional): The config key for the password for the Truststore.
            Should start with ``SECRET_``, example: ``SECRET_KAFKA_PRODUCTION``.
        :param security_protocol: Security protocol passed to kafka.security.protocol. See Kafka documentation for valid values.
        :param deduplication_columns: Columns in the stream data that uniquely identify data records.
                                        Used for de-duplicating. Spark will drop rows if there are duplicates in the deduplication_columns, but only within the watermark delay window.

        :return: A KafkaConfig class instance.

        .. _User Guide: https://docs.tecton.ai/0.5/examples/create-a-streaming-data-source.html#write-the-stream-message-post-processor-function
        .. _Productionizing a Stream: https://docs.tecton.ai/0.5/overviews/framework/feature_views/stream/index.html#productionizing-a-stream

        Example of a KafkaConfig declaration:

        .. code-block:: python

            import datetime
            import pyspark
            from tecton import KafkaConfig


            def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import from_json, col
                from pyspark.sql.types import StringType, TimestampType

                PAYLOAD_SCHEMA = (
                  StructType()
                        .add("accountId", StringType(), False)
                        .add("transaction_id", StringType(), False)
                )

                EVENT_ENVELOPE_SCHEMA = (
                  StructType()
                        .add("timestamp", TimestampType(), False)
                        .add("payload", PAYLOAD_SCHEMA, False)
                )

                value = col("value").cast("string")
                df = df.withColumn("event", from_json(value, EVENT_ENVELOPE_SCHEMA))
                df = df.withColumn("accountId", col("event.payload.accountId"))
                df = df.withColumn("transaction_id", col("event.payload.transaction_id"))
                df = df.withColumn("timestamp", col("event.timestamp"))

                return df

            # Declare Kafka Config instance object that can be used as an argument in StreamSource
            click_stream_kafka_ds = KafkaConfig(
                                        kafka_bootstrap_servers="127.0.0.1:12345",
                                        topics="click-events-json",
                                        timestamp_field="click_event_timestamp",
                                        post_processor=raw_data_deserialization)
        """
        self._args = args = data_source_pb2.KafkaDataSourceArgs()
        args.kafka_bootstrap_servers = kafka_bootstrap_servers
        args.topics = topics
        if function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        args.common_args.timestamp_field = timestamp_field
        if watermark_delay_threshold:
            args.common_args.watermark_delay_threshold.FromTimedelta(watermark_delay_threshold)
        for key in sorted((options or {}).keys()):
            option = data_source_pb2.Option()
            option.key = key
            option.value = options[key]
            args.options.append(option)
        if ssl_keystore_location:
            args.ssl_keystore_location = ssl_keystore_location
        if ssl_keystore_password_secret_id:
            args.ssl_keystore_password_secret_id = ssl_keystore_password_secret_id
        if ssl_truststore_location:
            args.ssl_truststore_location = ssl_truststore_location
        if ssl_truststore_password_secret_id:
            args.ssl_truststore_password_secret_id = ssl_truststore_password_secret_id
        if security_protocol:
            args.security_protocol = security_protocol
        if deduplication_columns:
            for column_name in deduplication_columns:
                args.common_args.deduplication_columns.append(column_name)

        self.post_processor = post_processor

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.kafka_ds_config.CopyFrom(self._args)


class KinesisConfig(BaseStreamConfig):
    """
    Configuration used to reference a Kinesis stream.

    The KinesisConfig class is used to create a reference to an AWS Kinesis stream.

    This class is used as an input to a :class:`StreamSource`'s parameter ``stream_config``. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of ``StreamSource`` that takes this configuration
    class instance as a parameter.
    """

    def __init__(
        self,
        stream_name: str,
        region: str,
        post_processor,
        timestamp_field: str,
        initial_stream_position: str,
        watermark_delay_threshold: datetime.timedelta = datetime.timedelta(hours=24),
        deduplication_columns: Optional[List[str]] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """
        Instantiates a new KinesisConfig.

        :param stream_name: Name of the Kinesis stream.
        :param region: AWS region of the stream, e.g: "us-west-2".
        :param post_processor: Python user defined function ``f(DataFrame) -> DataFrame`` that takes in raw
                                      Pyspark data source DataFrame and translates it to the DataFrame to be
                                      consumed by the Feature View. See an example of
                                      post_processor in the `User Guide`_.
        :param timestamp_field: Name of the column containing timestamp for watermarking.
        :param initial_stream_position: Initial position in stream, e.g: "latest" or "trim_horizon".
                                                More information available in `Spark Kinesis Documentation`_.
        :param watermark_delay_threshold: (Default: 24h) Watermark time interval, e.g: timedelta(hours=36), used by Spark Structured Streaming to account for late-arriving data. See: `Productionizing a Stream`_.
        :param deduplication_columns: Columns in the stream data that uniquely identify data records.
                                        Used for de-duplicating.
        :param options: A map of additional Spark readStream options

        :return: A KinesisConfig class instance.

        .. _User Guide: https://docs.tecton.ai/0.5/examples/create-a-streaming-data-source.html#write-the-stream-message-post-processor-function
        .. _Productionizing a Stream: https://docs.tecton.ai/0.5/overviews/framework/feature_views/stream/index.html#productionizing-a-stream
        .. _Spark Kinesis Documentation: https://spark.apache.org/docs/latest/streaming-kinesis-integration.html

        Example of a KinesisConfig declaration:

        .. code-block:: python

            import pyspark
            from tecton import KinesisConfig


            # Define our deserialization raw stream translator
            def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import col, from_json, from_utc_timestamp
                from pyspark.sql.types import StructType, StringType

                payload_schema = (
                  StructType()
                        .add('amount', StringType(), False)
                        .add('isFraud', StringType(), False)
                        .add('timestamp', StringType(), False)
                )

                return (
                    df.selectExpr('cast (data as STRING) jsonData')
                    .select(from_json('jsonData', payload_schema).alias('payload'))
                    .select(
                        col('payload.amount').cast('long').alias('amount'),
                        col('payload.isFraud').cast('long').alias('isFraud'),
                        from_utc_timestamp('payload.timestamp', 'UTC').alias('timestamp')
                    )
                )
            # Declare KinesisConfig instance object that can be used as argument in `StreamSource`
            stream_config = KinesisConfig(
                                    stream_name='transaction_events',
                                    region='us-west-2',
                                    initial_stream_position='latest',
                                    timestamp_field='timestamp',
                                    post_processor=raw_data_deserialization,
                                    options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
            )
        """

        args = data_source_pb2.KinesisDataSourceArgs()
        args.stream_name = stream_name
        args.region = region
        if function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        args.common_args.timestamp_field = timestamp_field
        if initial_stream_position:
            args.initial_stream_position = data_source_helper.INITIAL_STREAM_POSITION_STR_TO_ENUM[
                initial_stream_position
            ]
        if watermark_delay_threshold:
            args.common_args.watermark_delay_threshold.FromTimedelta(watermark_delay_threshold)
        if deduplication_columns:
            for column_name in deduplication_columns:
                args.common_args.deduplication_columns.append(column_name)
        options_ = options or {}
        for key in sorted(options_.keys()):
            option = data_source_pb2.Option()
            option.key = key
            option.value = options_[key]
            args.options.append(option)

        self._args = args
        self.post_processor = post_processor

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.kinesis_ds_config.CopyFrom(self._args)


class HiveConfig(BaseBatchConfig):
    """
    Configuration used to reference a Hive table.

    The HiveConfig class is used to create a reference to a Hive Table.

    This class is used as an input to a :class:`BatchSource`'s parameter ``batch_config``. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of ``BatchSource`` that takes this configuration
    class instance as a parameter.
    """

    def __init__(
        self,
        table: str,
        database: str,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        datetime_partition_columns: Optional[List[DatetimePartitionColumn]] = None,
        post_processor: Optional[Callable] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
    ):
        """
        Instantiates a new HiveConfig.

        :param table: A table registered in Hive MetaStore.
        :param database: A database registered in Hive MetaStore.
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                    to filter data from this source, before any feature view transformations are applied.
                                    Only required if this source is used with `FilteredSource`.
        :param timestamp_format: Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param datetime_partition_columns: List of DatetimePartitionColumn the raw data is partitioned by, otherwise None.
        :param post_processor: Python user defined function ``f(DataFrame) -> DataFrame`` that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A HiveConfig class instance.


        Example of a HiveConfig declaration:

        .. code-block:: python

            from tecton import HiveConfig
            import pyspark

            def convert_temperature(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import udf,col
                from pyspark.sql.types import DoubleType

                # Convert the incoming PySpark DataFrame temperature Celsius to Fahrenheit
                udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
                converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
                return converted_df

            # declare a HiveConfig instance, which can be used as a parameter to a BatchSource
            batch_config=HiveConfig(database='global_temperatures',
                                        table='us_cities',
                                        timestamp_field='timestamp',
                                        post_processor=convert_temperature)

        """
        self._args = data_source_pb2.HiveDataSourceArgs()
        self._args.table = table
        self._args.database = database
        if timestamp_field:
            self._args.common_args.timestamp_field = timestamp_field
        if timestamp_format:
            self._args.timestamp_format = timestamp_format

        if datetime_partition_columns:
            for column in datetime_partition_columns:
                column_args = data_source_pb2.DatetimePartitionColumnArgs()
                column_args.column_name = column.column_name
                column_args.datepart = column.datepart
                column_args.zero_padded = column.zero_padded
                if column.format_string:
                    column_args.format_string = column.format_string
                self._args.datetime_partition_columns.append(column_args)
        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            self._args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))

        self._args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.hive_ds_config.CopyFrom(self._args)


class SnowflakeConfig(BaseBatchConfig):
    """
    Configuration used to reference a Snowflake table or query.

    The SnowflakeConfig class is used to create a reference to a Snowflake table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class is used as an input to a :class:`BatchSource`'s parameter ``batch_config``. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of ``BatchSource`` that takes this configuration
    class instance as a parameter.
    """

    def __init__(
        self,
        *,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        warehouse: Optional[str] = None,
        url: Optional[str] = None,
        role: Optional[str] = None,
        table: Optional[str] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
    ):
        """
        Instantiates a new SnowflakeConfig. One of table and query should be specified when creating this file.

        :param database: The Snowflake database for this Data source.
        :param schema: The Snowflake schema for this Data source.
        :param warehouse: The Snowflake warehouse for this Data source. This parameter is not supported in Tecton on Snowflake.
        :param url: The connection URL to Snowflake, which contains account information
                         (e.g. https://xy12345.eu-west-1.snowflakecomputing.com). This parameter is not supported in Tecton on Snowflake.
        :param role: The Snowflake role that should be used for this Data source. This parameter is not supported in Tecton on Snowflake.

        :param table: The table for this Data source. Only one of `table` and `query` must be specified.
        :param query: The query for this Data source. Only one of `table` and `query` must be specified.
                        This parameter is not supported in Tecton on Snowflake.
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                    to filter data from this source, before any feature view transformations are applied.
                                    Only required if this source is used with `FilteredSource`.
        :param post_processor: Python user defined function ``f(DataFrame) -> DataFrame`` that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View. This parameter is not supported in Tecton on Snowflake.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A SnowflakeConfig class instance.


        Example of a SnowflakeConfig declaration:

        .. code-block:: python

            from tecton import SnowflakeConfig, BatchSource

            # Declare SnowflakeConfig instance object that can be used as an argument in BatchSource
            snowflake_ds_config = SnowflakeConfig(
                                              url="https://<your-cluster>.eu-west-1.snowflakecomputing.com/",
                                              database="CLICK_STREAM_DB",
                                              schema="CLICK_STREAM_SCHEMA",
                                              warehouse="COMPUTE_WH",
                                              table="CLICK_STREAM_FEATURES",
                                              query="SELECT timestamp as ts, created, user_id, clicks, click_rate"
                                                     "FROM CLICK_STREAM_DB.CLICK_STREAM_FEATURES")

            # Use in the BatchSource
            snowflake_ds = BatchSource(name="click_stream_snowflake_ds",
                                           batch_config=snowflake_ds_config)
        """
        self._args = args = data_source_pb2.SnowflakeDataSourceArgs(
            database=database,
            schema=schema,
            warehouse=warehouse,
            url=url,
            role=role,
            table=table,
            query=query,
        )

        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

        args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.snowflake_ds_config.CopyFrom(self._args)


class RedshiftConfig(BaseBatchConfig):
    """
    Configuration used to reference a Redshift table or query.

    The RedshiftConfig class is used to create a reference to a Redshift table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        endpoint: str,
        table: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
    ):
        """
        Instantiates a new RedshiftConfig. One of table and query should be specified when creating this file.

        :param endpoint: The connection endpoint to Redshift
                         (e.g. redshift-cluster-1.cigcwzsdltjs.us-west-2.redshift.amazonaws.com:5439/dev).
        :param table: The Redshift table for this Data source. Only one of table and query should be specified.
        :param post_processor: Python user defined function ``f(DataFrame) -> DataFrame`` that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param query: A Redshift query for this Data source. Only one of table and query should be specified.
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                    to filter data from this source, before any feature view transformations are applied.
                                    Only required if this source is used with `FilteredSource`.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A RedshiftConfig class instance.

        Example of a RedshiftConfig declaration:

        .. code-block:: python

            from tecton import RedshiftConfig

            # Declare RedshiftConfig instance object that can be used as an argument in BatchSource
            redshift_ds_config = RedshiftConfig(endpoint="cluster-1.us-west-2.redshift.amazonaws.com:5439/dev",
                                                  query="SELECT timestamp as ts, created, user_id, ad_id, duration"
                                                        "FROM ad_serving_features")
        """
        self._args = args = data_source_pb2.RedshiftDataSourceArgs()
        args.endpoint = endpoint

        if table and query:
            raise AssertionError(f"Should only specify one of table and query sources for redshift")
        if not table and not query:
            raise AssertionError(f"Missing both table and query sources for redshift, exactly one must be present")

        if table:
            args.table = table
        else:
            args.query = query

        if post_processor is not None and function_serialization.should_serialize_function(post_processor):
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

        args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.redshift_ds_config.CopyFrom(self._args)


class SparkBatchConfig(BaseBatchConfig):
    """
    Configuration used to define a batch source using a Data Source Function.

    The ``SparkBatchConfig`` class is used to configure a batch source using a user defined Data Source Function.

    This class is used as an input to a :class:`BatchSource`'s parameter ``batch_config``. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of ``BatchSource`` that takes this configuration
    class instance as a parameter.

    **Do not instantiate this class directly.** Use :py:func:`tecton.spark_batch_config` instead.
    """

    def __init__(
        self,
        data_source_function: Union[
            Callable[[SparkSession], DataFrame], Callable[[SparkSession, FilterContext], DataFrame]
        ],
        data_delay: datetime.timedelta = datetime.timedelta(seconds=0),
        supports_time_filtering: bool = False,
    ):
        """
        Instantiates a new SparkBatchConfig.

        :param data_source_function: User defined Data Source Function that takes in a ``SparkSession`` and an optional
                                    :class:`tecton.FilterContext`, if ``supports_time_filtering=True``. Returns a ``DataFrame``.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a ``batch_schedule`` of 1 day and one of
                                    the data source inputs has a ``data_delay`` of 1 hour, then
                                    incremental materialization jobs will run at ``01:00`` UTC.
        :param supports_time_filtering: When set to ``True``, the Data Source Function must take the ``filter_context``
                                    parameter and implement time filtering logic.
                                    ``supports_time_filtering`` must be set to `True` if ``<data source>.get_dataframe()`` is called with ``start_time``
                                    or ``end_time``. ``supports_time_filtering`` must also be set to ``True`` if using :class:`tecton.declarative.FilteredSource`
                                    with a Data Source when defining a ``FeatureView``. The ``FeatureView`` will call
                                    the Data Source Function with the :class:`tecton.FilterContext`, which has the ``start_time`` and
                                    ``end_time`` set.

        :return: A SparkBatchConfig class instance.
        """
        params = list(inspect.signature(data_source_function).parameters)
        function_name = data_source_function.__name__
        if supports_time_filtering and params != ["spark", "filter_context"]:
            raise AssertionError(
                f"Data Source Function {function_name}'s required signature is `{function_name}(spark, filter_context)` when supports_time_filtering is True"
            )
        elif not supports_time_filtering and params != ["spark"]:
            raise AssertionError(
                f"Data Source Function {function_name}'s required signature is `{function_name}(spark)`"
            )

        self._args = data_source_pb2.SparkBatchConfigArgs()
        if function_serialization.should_serialize_function(data_source_function):
            self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self._args.data_delay.FromTimedelta(data_delay)
        self._args.supports_time_filtering = supports_time_filtering
        self._data_delay = data_delay
        self.data_source_function = data_source_function

    @property
    def data_delay(self) -> datetime.timedelta:
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.spark_batch_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)


@typechecked
def spark_batch_config(
    *,
    data_delay: Optional[datetime.timedelta] = datetime.timedelta(seconds=0),
    supports_time_filtering: Optional[bool] = False,
):
    """
    Declare a :class:`tecton.SparkBatchConfig` for configuring a Batch Source with a Data Source Function.
    The function takes in a ``SparkSession`` and an optional :class:`tecton.FilterContext`, if ``supports_time_filtering=True``. Returns a ``DataFrame``.

    :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                batch schedule period. This parameter configures how long they wait after the end
                                of the period before starting, typically to ensure that all data has landed.
                                For example, if a feature view has a ``batch_schedule`` of 1 day and one of
                                the data source inputs has ``data_delay=timedelta(hours=1)`` set, then
                                incremental materialization jobs will run at ``01:00`` UTC.
    :param supports_time_filtering: When set to ``True``, the Data Source Function must take the ``filter_context``
                                    parameter and implement time filtering logic.
                                    ``supports_time_filtering`` must be set to `True` if ``<data source>.get_dataframe()`` is called with ``start_time``
                                    or ``end_time``. ``supports_time_filtering`` must also be set to ``True`` if using :class:`tecton.declarative.FilteredSource`
                                    with a Data Source when defining a ``FeatureView``. The ``FeatureView`` will call
                                    the Data Source Function with the :class:`tecton.FilterContext`, which has the ``start_time`` and
                                    ``end_time`` set.

    Example defining a Data Source Function using ``spark_batch_config``:

    .. code-block:: python

        from tecton import spark_batch_config

        @spark_batch_config(supports_time_filtering=True)
        def redshift_data_source_function(spark, filter_context):
            spark_format = "com.databricks.spark.redshift"
            params = {
                "user": "<user name>",
                "password": os.environ["redshift_password"]
            }
            endpoint = "<redshift endpoint>"
            full_connection_string = f"jdbc:redshift://{endpoint};user={params['user']};password={params['password']}"
            df_reader = (
                spark.read.format(spark_format)
                .option("url", full_connection_string)
                .option("forward_spark_s3_credentials", "true")
            )
            df_reader = df_reader.option("dbtable", "your_table_name")
            df = df_reader_load()
            ts_column = "timestamp"
            df = df.withColumn(ts_column, col(ts_column).cast("timestamp"))
            # Handle time filtering
            if filter_context:
                if filter_context.start_time:
                    df = df.where(col(ts_column) >= filter_context.start_time)
                if filter_context.end_time:
                    df = df.where(col(ts_column) < filter_context.end_time)
            return df
    """

    def decorator(data_source_function):
        batch_config = SparkBatchConfig(
            data_source_function=data_source_function,
            data_delay=data_delay,
            supports_time_filtering=supports_time_filtering,
        )
        functools.update_wrapper(wrapper=batch_config, wrapped=data_source_function)
        return batch_config

    return decorator


class SparkStreamConfig(BaseStreamConfig):
    """
    Configuration used to define a stream source using a Data Source Function.

    The ``SparkStreamConfig`` class is used to configure a stream source using a user defined Data Source Function.

    This class is used as an input to a :class:`StreamSource`'s parameter ``stream_config``. Declaring this configuration
    class alone will not register a Data Source. Instead, declare as a part of ``StreamSource`` that takes this configuration
    class instance as a parameter.

    **Do not instantiate this class directly.** Use :py:func:`tecton.spark_stream_config` instead.
    """

    def __init__(self, data_source_function: Callable[[SparkSession], DataFrame]):
        """
        Instantiates a new SparkBatchConfig.

        :param data_source_function: User-defined Data Source Function that takes in a ``SparkSession`` and returns
                    a streaming ``DataFrame``.

        :return: A SparkStreamConfig class instance.
        """
        params = list(inspect.signature(data_source_function).parameters)
        function_name = data_source_function.__name__
        if params != ["spark"]:
            raise AssertionError(
                f"Data Source Function {function_name}'s required signature is `{function_name}(spark)`"
            )

        self._args = data_source_pb2.SparkStreamConfigArgs()
        if function_serialization.should_serialize_function(data_source_function):
            self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self.data_source_function = data_source_function

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.spark_stream_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)


def spark_stream_config():
    """
    Declare a :class:`tecton.SparkStreamConfig` for configuring a Stream Source with a Data Source Function. The function takes in a ``SparkSession`` returns a streaming ``DataFrame``.

    Example defining a Data Source Function using ``spark_stream_config``:

    .. code-block:: python

        from tecton import spark_stream_config

        def raw_data_deserialization(df):
            from pyspark.sql.functions import col, from_json, from_utc_timestamp, when
            from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, BooleanType, IntegerType
            payload_schema = StructType([
                StructField("user_id", StringType(), False),
                StructField("transaction_id", StringType(), False),
                StructField("category", StringType(), False),
                StructField("amt", StringType(), False),
                StructField("timestamp", StringType(), False),
            ])
            return (
                df.selectExpr("cast (data as STRING) jsonData")
                .select(from_json("jsonData", payload_schema).alias("payload"))
                .select(
                    col("payload.user_id").alias("user_id"),
                    col("payload.transaction_id").alias("transaction_id"),
                    col("payload.category").alias("category"),
                    col("payload.amt").cast("double").alias("amt"),
                    from_utc_timestamp("payload.timestamp", "UTC").alias("timestamp")
                )
            )

        @spark_stream_config()
        def kinesis_data_source_function(spark):
            options = {
                "streamName": "<stream name>",
                "roleArn": "<role ARN>",
                "region": "<region>",
                "shardFetchInterval": "30s",
                "initialPosition": "latest"
            }
            reader = spark.readStream.format("kinesis").options(**options)
            df = reader.load()
            df = raw_data_deserialization(df)
            watermark = "{} seconds".format(timedelta(hours=24).seconds)
            df = df.withWatermark("timestamp", watermark)
            return df
    """

    def decorator(data_source_function):
        stream_config = SparkStreamConfig(
            data_source_function=data_source_function,
        )
        functools.update_wrapper(wrapper=stream_config, wrapped=data_source_function)
        return stream_config

    return decorator


@attrs.define(auto_attribs=True)
class Aggregation(object):
    """
    This class describes a single aggregation that is applied in a batch or stream feature view.

    :param column: Column name of the feature we are aggregating.
    :type column: str
    :param function: One of the built-in aggregation functions.
    :type function: Union[str, AggregationFunction]
    :param time_window: Duration to aggregate over. Example: ``datetime.timedelta(days=30)``.
    :type time_window: datetime.timedelta
    :param name: The name of this feature. Defaults to an autogenerated name, e.g. transaction_count_7d_1d.
    :type name: str

    `function` can be one of predefined numeric aggregation functions, namely ``"count"``, ``"sum"``, ``"mean"``, ``"min"``, ``"max"``, ``"var_samp"``, ``"var_pop"``, ``"variance"`` - alias for ``"var_samp"``, ``"stddev_samp"``, ``"stddev_pop"``, ``"stddev"`` - alias for ``"stddev_samp"``. For
    these numeric aggregations, you can pass the name of it as a string. Nulls are handled like Spark SQL `Function(column)`, e.g. SUM/MEAN/MIN/MAX/VAR_SAMP/VAR_POP/VAR/STDDEV_SAMP/STDDEV_POP/STDDEV of all nulls is null and COUNT of all nulls is 0.

    In addition to numeric aggregations, :class:`Aggregation` supports the last non-distinct and distinct N aggregation that will compute the last N non-distinct and distinct values for the column by timestamp. Right now only string column is supported as input to this aggregation, i.e., the resulting feature value will be a list of strings. The order of the value in the list is ascending based on the timestamp. Nulls are not included in the aggregated list.

    You can use it via the ```last()``` and  ``last_distinct()`` helper function like this:

    .. code-block:: python

        from tecton.aggregation_functions import last_distinct, last

        @batch_feature_view(
        ...
        aggregations=[
            Aggregation(
                column='my_column',
                function=last_distinct(15),
                time_window=datetime.timedelta(days=7)),
            Aggregation(
                column='my_column',
                function=last(15),
                time_window=datetime.timedelta(days=7)),
            ],
        ...
        )
        def my_fv(data_source):
            pass

    """

    column: str
    """Column name of the feature we are aggregating."""
    function: Union[str, AggregationFunction]
    """One of the built-in aggregation functions (`'count'`, `'sum'`, `'mean'`, `'min'`, `'max'`, `'var_samp'`, `'var_pop'`, `'variance'`, `'stddev_samp'`, `'stddev_pop'`, `'stddev'`)."""
    time_window: datetime.timedelta
    """Example: ``datetime.timedelta(days=30)``"""
    name: Optional[str] = None
    """Example: ``datetime.timedelta(days=30)``"""

    def _to_proto(self, aggregation_interval: datetime.timedelta, is_continuous: bool):
        proto = feature_view_pb2.FeatureAggregation()
        proto.column = self.column

        if isinstance(self.function, str):
            proto.function = self.function
        elif isinstance(self.function, AggregationFunction):
            proto.function = self.function.name
            for k, v in self.function.params.items():
                assert isinstance(v, int)
                proto.function_params[k].CopyFrom(feature_view_pb2.ParamValue(int64_value=v))
        else:
            raise TypeError(f"Invalid function type: {type(self.function)}")

        proto.time_window.FromTimedelta(self.time_window)

        if self.name:
            proto.name = self.name
        else:
            proto.name = feature_view_utils.construct_aggregation_output_feature_name(
                proto.column,
                feature_view_utils.resolve_function_name(proto.function, proto.function_params),
                proto.time_window,
                time_utils.timedelta_to_proto(aggregation_interval),
                is_continuous,
            )
        return proto
