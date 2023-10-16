import copy
import enum
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pendulum
from typeguard import typechecked

from tecton_core import aggregation_utils
from tecton_core import errors
from tecton_core import feature_view_utils
from tecton_core import id_helper
from tecton_core import pipeline_common
from tecton_core import schema
from tecton_core import time_utils
from tecton_core.data_types import TimestampType
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.data import feature_store_pb2
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2
from tecton_proto.validation import validator_pb2


__all__ = [
    "FeatureViewSpec",
    "MaterializedFeatureViewSpec",
    "OnDemandFeatureViewSpec",
    "FeatureTableSpec",
    "MaterializedFeatureViewType",
    "create_feature_view_spec_from_data_proto",
    "create_feature_view_spec_from_args_proto",
    "FeatureViewSpecArgsSupplement",
    "get_batch_schedule_from_feature_view_args",
    "get_batch_trigger_from_feature_view_args",
    "get_join_keys_from_feature_view_args",
    "get_online_serving_keys_from_feature_view_args",
    "get_aggregate_features_from_feature_view_args",
]


@utils.frozen_strict
class FeatureViewSpec(tecton_object_spec.TectonObjectSpec):
    """Base class for feature view specs."""

    join_keys: Tuple[str, ...]
    entity_ids: Tuple[str, ...]
    online_serving_keys: Tuple[str, ...]  # Aka the Online Serving Index.
    feature_store_format_version: feature_store_pb2.FeatureStoreFormatVersion.ValueType = attrs.field()
    view_schema: schema.Schema
    materialization_schema: schema.Schema

    # materialization_enabled is True if the feature view has online or online set to True, and the feature view is
    # applied to a live workspace.
    materialization_enabled: bool
    online: bool
    offline: bool

    url: Optional[str] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @feature_store_format_version.validator
    def check_valid_feature_store_format_version(self, _, value):
        if (
            value < feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT
            or value > feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_MAX
        ):
            msg = f"Unsupported feature_store_format_version: {value}"
            raise ValueError(msg)

    @property
    def features(self) -> List[str]:
        """
        Returns the output feature names of this feature view
        """
        raise NotImplementedError

    def join_key_schema(self) -> schema.Schema:
        """
        Return the join key schmea which is adjusted by online serving keys. Only ODFV needs to overwrite this.
        """
        spine_schema_dict = self.view_schema.to_dict()
        # If online_serving_keys are specified, spine only needs to contain these keys instead of all join keys.
        retrieval_keys = self.online_serving_keys if len(self.online_serving_keys) > 0 else self.join_keys
        spine_schema_dict = {key: spine_schema_dict[key] for key in retrieval_keys}
        return schema.Schema.from_dict(spine_schema_dict)


@attrs.define
class FeatureViewSpecArgsSupplement:
    """A data class used for supplementing args protos during FeatureViewSpec construction.

    This Python data class can be used to include data that is not included in args protos (e.g. schemas) into the
    FeatureViewSpec constructor.
    """

    view_schema: Optional[schema_pb2.Schema]
    materialization_schema: Optional[schema_pb2.Schema]


class MaterializedFeatureViewType(enum.Enum):
    TEMPORAL = 1
    TEMPORAL_AGGREGATE = 2


@utils.frozen_strict
class MaterializedFeatureViewSpec(FeatureViewSpec):
    """Spec for Batch and Stream feature views."""

    is_continuous: bool
    type: MaterializedFeatureViewType
    data_source_type: data_source_type_pb2.DataSourceType.ValueType
    incremental_backfills: bool
    timestamp_field: str

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    pipeline: Optional[pipeline_pb2.Pipeline]

    batch_schedule: Optional[pendulum.Duration]
    slide_interval: Optional[pendulum.Duration]
    ttl: Optional[pendulum.Duration]
    feature_start_time: Optional[pendulum.DateTime]
    materialization_start_time: Optional[pendulum.DateTime] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )
    max_source_data_delay: pendulum.Duration
    materialized_data_path: Optional[str]
    time_range_policy: Optional[feature_view__data_pb2.MaterializationTimeRangePolicy.ValueType]
    materialization_state_transitions: Tuple[feature_view__data_pb2.MaterializationStateTransition, ...] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    offline_store: Optional[feature_view__args_pb2.OfflineFeatureStoreConfig]
    offline_store_params: Optional[feature_view__data_pb2.OfflineStoreParams] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    # Generally, data protos should not be exposed in the "spec". However, we make an exception in this case because
    # (a) there is no equivalent args proto, (b) it's a good data model for this usage, and (c) this proto is used
    # extensively in the query gen code (not worth refactoring).
    aggregate_features: Tuple[feature_view__data_pb2.AggregateFeature, ...]
    slide_interval_string: Optional[str]

    # Only relevant for offline-materialized fvs on snowflake compute
    snowflake_view_name: Optional[str]

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required. (batch_cluster_config should be.)
    batch_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]
    stream_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    # See failure: https://tectonworkspace.slack.com/archives/C04L8M14XGX/p1675279851469019
    batch_trigger: Optional[feature_view__args_pb2.BatchTriggerType.ValueType]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "MaterializedFeatureViewSpec":
        if proto.HasField("temporal_aggregate"):
            fv_type = MaterializedFeatureViewType.TEMPORAL_AGGREGATE
            is_continuous = proto.temporal_aggregate.is_continuous
            data_source_type = utils.get_field_or_none(proto.temporal_aggregate, "data_source_type")
            incremental_backfills = False
            slide_interval = time_utils.proto_to_duration(proto.temporal_aggregate.slide_interval)
            ttl = None
            aggregate_features = utils.get_tuple_from_repeated_field(proto.temporal_aggregate.features)
            slide_interval_string = utils.get_field_or_none(proto.temporal_aggregate, "slide_interval_string")
        elif proto.HasField("temporal"):
            fv_type = MaterializedFeatureViewType.TEMPORAL
            is_continuous = proto.temporal.is_continuous
            data_source_type = utils.get_field_or_none(proto.temporal, "data_source_type")
            incremental_backfills = proto.temporal.incremental_backfills
            slide_interval = None
            ttl = utils.get_non_default_duration_field_or_none(proto.temporal, "serving_ttl")
            aggregate_features = tuple()
            slide_interval_string = None
        else:
            msg = f"Unexpected feature view type: {proto}"
            raise TypeError(msg)

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            offline_store_params=utils.get_field_or_none(proto.materialization_params, "offline_store_params"),
            is_continuous=is_continuous,
            data_source_type=data_source_type,
            incremental_backfills=incremental_backfills,
            timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
            type=fv_type,
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=proto.materialization_enabled,
            online=proto.materialization_params.writes_to_online_store,
            offline=proto.materialization_params.writes_to_offline_store,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            batch_schedule=utils.get_non_default_duration_field_or_none(
                proto.materialization_params, "schedule_interval"
            ),
            slide_interval=slide_interval,
            ttl=ttl,
            feature_start_time=utils.get_timestamp_field_or_none(
                proto.materialization_params, "feature_start_timestamp"
            ),
            materialization_start_time=utils.get_timestamp_field_or_none(
                proto.materialization_params, "materialization_start_timestamp"
            ),
            max_source_data_delay=time_utils.proto_to_duration(proto.materialization_params.max_source_data_delay),
            aggregate_features=aggregate_features,
            slide_interval_string=slide_interval_string,
            materialized_data_path=utils.get_field_or_none(
                proto.enrichments.fp_materialization.materialized_data_location, "path"
            ),
            materialization_state_transitions=utils.get_tuple_from_repeated_field(
                proto.materialization_state_transitions
            ),
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            snowflake_view_name=utils.get_field_or_none(proto.snowflake_data, "snowflake_view_name"),
            validation_args=validator_pb2.FcoValidationArgs(feature_view=proto.validation_args),
            batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
            stream_cluster_config=utils.get_field_or_none(proto.materialization_params, "stream_materialization"),
            batch_trigger=utils.get_field_or_none(proto, "batch_trigger"),
            url=utils.get_field_or_none(proto, "web_url"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_view__args_pb2.FeatureViewArgs, supplement: FeatureViewSpecArgsSupplement
    ) -> "MaterializedFeatureViewSpec":
        feature_start_time = utils.get_timestamp_field_or_none(
            proto.materialized_feature_view_args, "feature_start_time"
        )

        is_continuous = (
            proto.materialized_feature_view_args.stream_processing_mode
            == feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
        )

        is_aggregate = len(proto.materialized_feature_view_args.aggregations) > 0
        if is_aggregate:
            fv_type = MaterializedFeatureViewType.TEMPORAL_AGGREGATE
            slide_interval_string = feature_view_utils.construct_aggregation_interval_name(
                proto.materialized_feature_view_args.aggregation_interval, is_continuous
            )

            # Logic must be kept in sync with getMaterializationStartTime() in FeatureViewManager.
            max_window = max(
                [
                    utils.get_duration_field_or_none(agg, "time_window")
                    for agg in proto.materialized_feature_view_args.aggregations
                ]
            )
            if feature_start_time is not None:
                materialization_start_time = feature_start_time - max_window
            else:
                materialization_start_time = None

            slide_interval = utils.get_duration_field_or_none(
                proto.materialized_feature_view_args, "aggregation_interval"
            )
        else:
            fv_type = MaterializedFeatureViewType.TEMPORAL
            slide_interval_string = None
            materialization_start_time = feature_start_time
            slide_interval = None

        if proto.materialized_feature_view_args.HasField("timestamp_field"):
            timestamp_field = proto.materialized_feature_view_args.timestamp_field
        else:
            timestamp_field = _get_timestamp_column(supplement.view_schema)

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(proto.feature_view_id, proto.info),
            entity_ids=tuple(id_helper.IdHelper.to_string(entity.entity_id) for entity in proto.entities),
            join_keys=get_join_keys_from_feature_view_args(proto),
            online_serving_keys=get_online_serving_keys_from_feature_view_args(proto),
            view_schema=schema.Schema(supplement.view_schema),
            materialization_schema=schema.Schema(supplement.materialization_schema),
            offline_store=utils.get_field_or_none(proto.materialized_feature_view_args, "offline_store"),
            offline_store_params=None,
            is_continuous=is_continuous,
            data_source_type=utils.get_field_or_none(proto.materialized_feature_view_args, "data_source_type"),
            incremental_backfills=proto.materialized_feature_view_args.incremental_backfills,
            timestamp_field=timestamp_field,
            type=fv_type,
            feature_store_format_version=feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
            materialization_enabled=False,
            online=proto.online_enabled,
            offline=proto.offline_enabled,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            batch_schedule=get_batch_schedule_from_feature_view_args(proto),
            slide_interval=slide_interval,
            ttl=utils.get_duration_field_or_none(proto.materialized_feature_view_args, "serving_ttl"),
            feature_start_time=feature_start_time,
            materialization_start_time=materialization_start_time,
            max_source_data_delay=_get_max_schedule_offset(proto.pipeline),
            aggregate_features=get_aggregate_features_from_feature_view_args(proto),
            slide_interval_string=slide_interval_string,
            materialized_data_path=None,
            time_range_policy=feature_view__data_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE,
            materialization_state_transitions=tuple(),
            snowflake_view_name=None,
            validation_args=None,
            batch_cluster_config=utils.get_field_or_none(proto.materialized_feature_view_args, "batch_compute"),
            stream_cluster_config=utils.get_field_or_none(proto.materialized_feature_view_args, "stream_compute"),
            batch_trigger=get_batch_trigger_from_feature_view_args(proto),
            url=None,
        )

    @property
    def features(self) -> List[str]:
        if len(self.aggregate_features) > 0:
            # Temporal aggregate feature view.
            return [aggregate_feature.output_feature_name for aggregate_feature in self.aggregate_features]
        else:
            # Temporal feature view.
            return [
                col
                for col in self.view_schema.column_names()
                if col != self.timestamp_field and col not in self.join_keys
            ]


@utils.frozen_strict
class OnDemandFeatureViewSpec(FeatureViewSpec):
    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    pipeline: Optional[pipeline_pb2.Pipeline]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "OnDemandFeatureViewSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=False,
            online=False,
            offline=False,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            validation_args=validator_pb2.FcoValidationArgs(feature_view=proto.validation_args),
            url=utils.get_field_or_none(proto, "web_url"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_view__args_pb2.FeatureViewArgs, supplement: FeatureViewSpecArgsSupplement
    ) -> "OnDemandFeatureViewSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(proto.feature_view_id, proto.info),
            entity_ids=tuple(),
            join_keys=tuple(),
            online_serving_keys=tuple(),
            view_schema=schema.Schema(supplement.view_schema),
            materialization_schema=schema.Schema(supplement.materialization_schema),
            feature_store_format_version=feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
            materialization_enabled=False,
            online=False,
            offline=False,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            validation_args=None,
            url=None,
        )

    @property
    def features(self) -> List[str]:
        return list(self.view_schema.column_names())

    def join_key_schema(
        self, dependent_fv_specs_and_jk_overrides: List[Tuple[FeatureViewSpec, List[utils.JoinKeyMappingSpec]]]
    ) -> schema.Schema:
        """Returns the combined join key schema from all input FVs which are adjusted by join key overridings."""
        input_fv_schema = schema.Schema(schema_pb2.Schema())
        for fv_spec, jk_overrides in dependent_fv_specs_and_jk_overrides:
            fv_schema_dict = fv_spec.join_key_schema().to_dict()
            for jk_override_spec in jk_overrides:
                fv_schema_dict[jk_override_spec.spine_column_name] = fv_schema_dict[
                    jk_override_spec.feature_view_column_name
                ]
                # Delete the original feature_view_column_name entry as the data type is assigned to the overriding key.
                del fv_schema_dict[jk_override_spec.feature_view_column_name]
            input_fv_schema += schema.Schema.from_dict(fv_schema_dict)
        return input_fv_schema


@utils.frozen_strict
class FeatureTableSpec(FeatureViewSpec):
    timestamp_field: str
    ttl: Optional[pendulum.Duration]

    offline_store: Optional[feature_view__args_pb2.OfflineFeatureStoreConfig]
    offline_store_params: Optional[feature_view__data_pb2.OfflineStoreParams] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )
    materialized_data_path: Optional[str]
    time_range_policy: Optional[feature_view__data_pb2.MaterializationTimeRangePolicy.ValueType]
    materialization_state_transitions: Tuple[feature_view__data_pb2.MaterializationStateTransition, ...] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required. (batch_cluster_config should be.)
    batch_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "FeatureTableSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            offline_store_params=utils.get_field_or_none(proto.materialization_params, "offline_store_params"),
            timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=proto.materialization_enabled,
            online=proto.feature_table.online_enabled,
            offline=proto.feature_table.offline_enabled,
            ttl=utils.get_non_default_duration_field_or_none(proto.feature_table, "serving_ttl"),
            materialized_data_path=utils.get_field_or_none(
                proto.enrichments.fp_materialization.materialized_data_location, "path"
            ),
            materialization_state_transitions=utils.get_tuple_from_repeated_field(
                proto.materialization_state_transitions
            ),
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            validation_args=validator_pb2.FcoValidationArgs(feature_view=proto.validation_args),
            batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
            url=utils.get_field_or_none(proto, "web_url"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_view__args_pb2.FeatureViewArgs, supplement: FeatureViewSpecArgsSupplement
    ) -> "FeatureTableSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(proto.feature_view_id, proto.info),
            entity_ids=tuple(id_helper.IdHelper.to_string(entity.entity_id) for entity in proto.entities),
            join_keys=get_join_keys_from_feature_view_args(proto),
            online_serving_keys=get_online_serving_keys_from_feature_view_args(proto),
            view_schema=schema.Schema(supplement.view_schema),
            materialization_schema=schema.Schema(supplement.materialization_schema),
            offline_store=utils.get_field_or_none(proto.feature_table_args, "offline_store"),
            offline_store_params=None,
            timestamp_field=_get_timestamp_column(supplement.view_schema),
            feature_store_format_version=feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
            materialization_enabled=False,
            online=proto.online_enabled,
            offline=proto.offline_enabled,
            ttl=utils.get_duration_field_or_none(proto.feature_table_args, "serving_ttl"),
            materialized_data_path=None,
            materialization_state_transitions=tuple(),
            time_range_policy=None,
            validation_args=None,
            batch_cluster_config=utils.get_field_or_none(proto.feature_table_args, "batch_compute"),
            url=None,
        )

    @property
    def features(self) -> List[str]:
        return [
            col for col in self.view_schema.column_names() if col != self.timestamp_field and col not in self.join_keys
        ]


def _get_view_schema(schemas: feature_view__data_pb2.FeatureViewSchemas) -> Optional[schema.Schema]:
    # Copy the schema so the `ClearField` doesn't change the proto passed into this fuction such as the schema in the MaterializationTaskParam.
    schemas_copy = copy.deepcopy(schemas)
    if schemas_copy.HasField("view_schema"):
        """
        feature_server_type raw_spark_type and raw_snowflake_type are deprecated fields that are still served in data
        proto for backwards compatibility with old SDKs. Clear the field here so that:
            1) Developers don't depend on this field being set.
            2) Local specs are equivalent to the remote specs.
        """
        for column in schemas_copy.view_schema.columns:
            column.ClearField("feature_server_type")
            column.ClearField("raw_spark_type")
            column.ClearField("raw_snowflake_type")
        return schema.Schema(schemas_copy.view_schema)
    else:
        return None


def _get_materialization_schema(schemas: feature_view__data_pb2.FeatureViewSchemas) -> Optional[schema.Schema]:
    # Copy the schema so the `ClearField` doesn't change the proto passed into this fuction such as the schema in the MaterializationTaskParam.
    schemas_copy = copy.deepcopy(schemas)
    if schemas_copy.HasField("materialization_schema"):
        """
        feature_server_type raw_spark_type and raw_snowflake_type are deprecated fields that are still served in data
        proto for backwards compatibility with old SDKs. Clear the field here so that:
            1) Developers don't depend on this field being set.
            2) Local specs are equivalent to the remote specs.
        """
        for column in schemas_copy.materialization_schema.columns:
            column.ClearField("feature_server_type")
            column.ClearField("raw_spark_type")
            column.ClearField("raw_snowflake_type")
        return schema.Schema(schemas_copy.materialization_schema)
    else:
        return None


@typechecked
def create_feature_view_spec_from_data_proto(
    proto: feature_view__data_pb2.FeatureView,
) -> Optional[Union[MaterializedFeatureViewSpec, OnDemandFeatureViewSpec, FeatureTableSpec]]:
    if proto.HasField("temporal_aggregate") or proto.HasField("temporal"):
        return MaterializedFeatureViewSpec.from_data_proto(proto)
    elif proto.HasField("on_demand_feature_view"):
        return OnDemandFeatureViewSpec.from_data_proto(proto)
    elif proto.HasField("feature_table"):
        return FeatureTableSpec.from_data_proto(proto)
    else:
        msg = f"Unexpect feature view type: {proto}"
        raise ValueError(msg)


@typechecked
def create_feature_view_spec_from_args_proto(
    proto: feature_view__args_pb2.FeatureViewArgs,
    supplement: FeatureViewSpecArgsSupplement,
) -> Optional[Union[MaterializedFeatureViewSpec, OnDemandFeatureViewSpec, FeatureTableSpec]]:
    if proto.HasField("materialized_feature_view_args"):
        return MaterializedFeatureViewSpec.from_args_proto(proto, supplement)
    elif proto.HasField("on_demand_args"):
        return OnDemandFeatureViewSpec.from_args_proto(proto, supplement)
    elif proto.HasField("feature_table_args"):
        return FeatureTableSpec.from_args_proto(proto, supplement)
    else:
        msg = f"Unexpect feature view type: {proto}"
        raise ValueError(msg)


def _get_timestamp_column(schema_proto: schema_pb2.Schema) -> str:
    schema_ = schema.Schema(schema_proto)
    timestamp_columns = [column[0] for column in schema_.column_name_and_data_types() if column[1] == TimestampType()]
    if len(timestamp_columns) != 1:
        msg = f"Attempted to infer timestamp. Expected exactly one timestamp column in schema {schema_}"
        raise errors.TectonValidationError(msg)
    return timestamp_columns[0]


def _get_max_schedule_offset(pipeline: pipeline_pb2.Pipeline) -> pendulum.Duration:
    ds_nodes = pipeline_common.get_all_data_source_nodes(pipeline)
    assert len(ds_nodes) > 0
    return max([time_utils.proto_to_duration(ds_node.data_source_node.schedule_offset) for ds_node in ds_nodes])


@typechecked
def get_batch_schedule_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
) -> Optional[pendulum.Duration]:
    is_aggregate = len(proto.materialized_feature_view_args.aggregations) > 0
    if is_aggregate:
        slide_interval = utils.get_duration_field_or_none(proto.materialized_feature_view_args, "aggregation_interval")
        is_continuous = (
            proto.materialized_feature_view_args.stream_processing_mode
            == feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
        )

        if is_continuous:
            # Default is set in Kotlin to one day per CONTINUOUS_MODE_TILE_DURATION.
            return pendulum.Duration(days=1)
        else:
            return (
                utils.get_duration_field_or_none(proto.materialized_feature_view_args, "batch_schedule")
                or slide_interval
            )
    else:
        return utils.get_duration_field_or_none(proto.materialized_feature_view_args, "batch_schedule")


@typechecked
def get_aggregate_features_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
) -> Tuple[feature_view__data_pb2.AggregateFeature, ...]:
    is_continuous = (
        proto.materialized_feature_view_args.stream_processing_mode
        == feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
    )
    aggregate_features = []
    for agg_args_proto in proto.materialized_feature_view_args.aggregations:
        agg_data_proto = aggregation_utils.create_aggregate_features(
            agg_args_proto, proto.materialized_feature_view_args.aggregation_interval, is_continuous
        )
        aggregate_features.append(agg_data_proto)
    return tuple(aggregate_features)


@typechecked
def get_batch_trigger_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
) -> Optional[feature_view__args_pb2.BatchTriggerType.ValueType]:
    if proto.materialized_feature_view_args.HasField("batch_trigger"):
        return proto.materialized_feature_view_args.batch_trigger
    else:
        return feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_SCHEDULED


@typechecked
def get_join_keys_from_feature_view_args(proto: feature_view__args_pb2.FeatureViewArgs) -> Tuple[str, ...]:
    join_keys = []
    for entity in proto.entities:
        join_keys.extend(entity.join_keys)
    return tuple(join_keys)


@typechecked
def get_online_serving_keys_from_feature_view_args(proto: feature_view__args_pb2.FeatureViewArgs) -> Tuple[str, ...]:
    return (
        tuple(proto.online_serving_index) if proto.online_serving_index else get_join_keys_from_feature_view_args(proto)
    )
