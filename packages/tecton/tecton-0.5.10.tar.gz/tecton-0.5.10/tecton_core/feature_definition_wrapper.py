import enum
from typing import Dict
from typing import List
from typing import Optional

import pendulum

from tecton_core import time_utils
from tecton_core.fco_container import FcoContainer
from tecton_core.feature_view_utils import CONTINUOUS_MODE_BATCH_INTERVAL
from tecton_core.feature_view_utils import get_input_feature_columns
from tecton_core.feature_view_utils import validate_version
from tecton_core.id_helper import IdHelper
from tecton_core.logger import get_logger
from tecton_core.online_serving_index import OnlineServingIndex
from tecton_core.schema import Schema
from tecton_proto.args.feature_view_pb2 import OfflineFeatureStoreConfig
from tecton_proto.args.feature_view_pb2 import OnlineStoreConfig
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.common.framework_version_pb2 import FrameworkVersion as FrameworkVersionProto
from tecton_proto.data.feature_view_pb2 import FeatureView
from tecton_proto.data.feature_view_pb2 import MaterializationTimeRangePolicy
from tecton_proto.data.feature_view_pb2 import TrailingTimeWindowAggregation
from tecton_proto.data.new_transformation_pb2 import NewTransformation as Transformation
from tecton_proto.data.virtual_data_source_pb2 import VirtualDataSource

logger = get_logger("FeatureDefinitionWrapper")


# Create a parallel enum class since Python proto extensions do not use an enum class.
# Keep up-to-date with FrameworkVersion from tecton_proto/args/version_constraints.proto.
class FrameworkVersion(enum.Enum):
    UNSPECIFIED = FrameworkVersionProto.UNSPECIFIED
    FWV3 = FrameworkVersionProto.FWV3
    FWV4 = FrameworkVersionProto.FWV4
    FWV5 = FrameworkVersionProto.FWV5


class FeatureDefinitionWrapper:
    def __init__(self, feature_view_proto: FeatureView, fco_container: FcoContainer):
        self.fv = feature_view_proto
        self.fco_container = fco_container

    @property
    def id(self) -> str:
        return IdHelper.to_string(self.fv.feature_view_id)

    @property
    def name(self) -> str:
        return self.fv.fco_metadata.name

    @property
    def is_temporal_aggregate(self) -> bool:
        return self.fv.HasField("temporal_aggregate")

    @property
    def is_continuous_temporal_aggregate(self) -> bool:
        return self.fv.temporal_aggregate.is_continuous

    @property
    def is_temporal(self) -> bool:
        return self.fv.HasField("temporal")

    @property
    def is_feature_table(self) -> bool:
        return self.fv.HasField("feature_table")

    @property
    def is_stream(self) -> bool:
        if self.fv.HasField("temporal"):
            data_source_type = self.fv.temporal.data_source_type
        elif self.fv.HasField("temporal_aggregate"):
            data_source_type = self.fv.temporal_aggregate.data_source_type
        else:
            return False

        return data_source_type == DataSourceType.STREAM_WITH_BATCH

    @property
    def is_on_demand(self) -> bool:
        return self.fv.HasField("on_demand_feature_view")

    @property
    def is_incremental_backfill(self) -> bool:
        return self.fv.HasField("temporal") and self.fv.temporal.incremental_backfills

    @property
    def get_feature_store_format_version(self) -> int:
        version = self.fv.feature_store_format_version
        validate_version(version)
        return version

    @property
    def namespace_separator(self) -> FrameworkVersion:
        if self.framework_version == FrameworkVersion.FWV5:
            return "__"
        else:
            return "."

    @property
    def framework_version(self) -> FrameworkVersion:
        return FrameworkVersion(self.fv.fco_metadata.framework_version)

    @property
    def time_key(self) -> str:
        return self.fv.timestamp_key

    @property
    def join_keys(self) -> List[str]:
        return list(self.fv.join_keys)

    @property
    def online_serving_index(self) -> OnlineServingIndex:
        return OnlineServingIndex.from_proto(self.fv.online_serving_index)

    @property
    def wildcard_join_key(self) -> Optional[str]:
        """
        Returns a wildcard join key column name for the feature view if it exists;
        Otherwise returns None.
        """
        online_serving_index = self.online_serving_index
        wildcard_keys = [join_key for join_key in self.join_keys if join_key not in online_serving_index.join_keys]
        return wildcard_keys[0] if wildcard_keys else None

    @property
    def offline_store_config(self) -> OfflineFeatureStoreConfig:
        return self.fv.materialization_params.offline_store_config

    @property
    def online_store_params(self) -> OnlineStoreConfig:
        return self.fv.materialization_params.online_store_params

    @property
    def online_store_data_delay_seconds(self) -> int:
        return 0 if self.is_stream else self.allowed_upstream_lateness.in_seconds()

    @property
    def timestamp_key(self) -> Optional[str]:
        return self.fv.timestamp_key

    @property
    def materialization_enabled(self) -> bool:
        return self.fv.materialization_enabled

    @property
    def writes_to_offline_store(self) -> bool:
        if self.is_temporal_aggregate or self.is_temporal:
            return self.fv.materialization_params.writes_to_offline_store
        elif self.is_feature_table:
            return self.fv.feature_table.offline_enabled
        else:
            raise ValueError(f"Invalid invocation on unsupported FeatureView type")

    @property
    def writes_to_online_store(self) -> bool:
        if self.is_temporal_aggregate or self.is_temporal:
            return self.fv.materialization_params.writes_to_online_store
        elif self.is_feature_table:
            return self.fv.feature_table.online_enabled
        else:
            raise ValueError(f"Invalid invocation on unsupported FeatureView type")

    @property
    def view_schema(self) -> Schema:
        return Schema(self.fv.schemas.view_schema)

    @property
    def min_scheduling_interval(self) -> Optional[pendulum.Duration]:
        if self.is_feature_table:
            return None

        duration = None
        if self.is_temporal_aggregate:
            duration = self.fv.temporal_aggregate.slide_interval
        elif self.is_temporal:
            duration = self.fv.materialization_params.schedule_interval

        return time_utils.proto_to_duration(duration)

    @property
    def batch_materialization_schedule(self) -> pendulum.Duration:
        if self.is_temporal_aggregate and not self.fv.materialization_params.HasField("schedule_interval"):
            if self.is_continuous_temporal_aggregate:
                return time_utils.proto_to_duration(CONTINUOUS_MODE_BATCH_INTERVAL)
            else:
                return time_utils.proto_to_duration(self.fv.temporal_aggregate.slide_interval)
        else:
            return time_utils.proto_to_duration(self.fv.materialization_params.schedule_interval)

    @property
    def allowed_upstream_lateness(self) -> pendulum.Duration:
        return time_utils.proto_to_duration(self.fv.materialization_params.allowed_upstream_lateness)

    @property
    def materialization_start_timestamp(self) -> pendulum.datetime:
        return pendulum.instance(self.fv.materialization_params.materialization_start_timestamp.ToDatetime())

    @property
    def feature_start_timestamp(self) -> Optional[pendulum.datetime]:
        if self.fv.materialization_params.HasField("feature_start_timestamp"):
            return pendulum.instance(self.fv.materialization_params.feature_start_timestamp.ToDatetime())
        else:
            return None

    @property
    def time_range_policy(self) -> MaterializationTimeRangePolicy:
        return self.fv.materialization_params.time_range_policy

    @property
    def data_partitions_coalesce_override(self) -> int:
        return 10  # Value of DEFAULT_COALESCE_FOR_S3 as defined in materialization.py

    @property
    def data_source_ids(self) -> List[str]:
        nodes = pipeline_to_ds_inputs(self.fv.pipeline).values()
        return [IdHelper.to_string(node.virtual_data_source_id) for node in nodes]

    @property
    def data_sources(self) -> List[VirtualDataSource]:
        ds_ids = self.data_source_ids
        return self.fco_container.get_by_ids(ds_ids)

    @property
    def get_tile_interval(self) -> pendulum.Duration:
        if self.is_temporal_aggregate:
            return time_utils.proto_to_duration(self.fv.temporal_aggregate.slide_interval)
        elif self.is_temporal:
            return time_utils.proto_to_duration(self.fv.materialization_params.schedule_interval)

        raise ValueError(f"Invalid invocation on unsupported FeatureView type")

    @property
    def get_batch_schedule_for_version(self) -> int:
        return time_utils.convert_proto_duration_for_version(
            self.fv.materialization_params.schedule_interval, self.get_feature_store_format_version
        )

    @property
    def get_tile_interval_for_version(self) -> int:
        if self.is_temporal_aggregate:
            return time_utils.convert_proto_duration_for_version(
                self.fv.temporal_aggregate.slide_interval, self.get_feature_store_format_version
            )
        elif self.is_temporal:
            return time_utils.convert_proto_duration_for_version(
                self.fv.materialization_params.schedule_interval, self.get_feature_store_format_version
            )

        raise ValueError(f"Invalid invocation on unsupported FeatureView type")

    @property
    def get_aggregate_slide_interval_string(self) -> str:
        if self.is_temporal_aggregate:
            return self.fv.temporal_aggregate.slide_interval_string
        raise ValueError(f"Invalid invocation on unsupported FeatureView type")

    @property
    def materialized_data_path(self) -> str:
        return self.fv.enrichments.fp_materialization.materialized_data_location.path

    @property
    def max_aggregation_window(self) -> Optional[int]:
        if self.is_temporal_aggregate:
            return max(
                [feature.window for feature in self.fv.temporal_aggregate.features],
                key=lambda window: window.ToSeconds(),
            )
        return None

    @property
    def transformations(self) -> List[Transformation]:
        transformation_ids = pipeline_to_transformation_ids(self.pipeline)
        return self.fco_container.get_by_ids(transformation_ids)

    @property
    def trailing_time_window_aggregation(self) -> Optional[TrailingTimeWindowAggregation]:
        if not self.is_temporal_aggregate:
            return None

        aggregation = TrailingTimeWindowAggregation()
        aggregation.time_key = self.timestamp_key
        slide_period_seconds = self.fv.temporal_aggregate.slide_interval.ToSeconds()
        aggregation.is_continuous = slide_period_seconds == 0
        aggregation.aggregation_slide_period.FromSeconds(slide_period_seconds)

        aggregation.features.extend(self.fv.temporal_aggregate.features)
        return aggregation

    @property
    def serving_ttl(self) -> Optional[pendulum.Duration]:
        if self.is_temporal:
            return time_utils.proto_to_duration(self.fv.temporal.serving_ttl)
        elif self.is_feature_table:
            return time_utils.proto_to_duration(self.fv.feature_table.serving_ttl)
        return None

    @property
    def features(self) -> List[str]:
        if self.is_temporal_aggregate and self.trailing_time_window_aggregation:
            return [
                f.output_feature_name
                for f in self.trailing_time_window_aggregation.features
                if f.output_feature_name != self.timestamp_key
            ]
        elif self.is_on_demand:
            return Schema(self.fv.schemas.view_schema).column_names()
        view_schema = Schema(self.fv.schemas.view_schema)
        return get_input_feature_columns(view_schema.to_proto(), self.join_keys, self.timestamp_key)

    @property
    def workspace(self) -> str:
        return self.fv.fco_metadata.workspace

    @property
    def pipeline(self) -> Pipeline:
        return self.fv.pipeline

    @property
    def feature_view_proto(self) -> FeatureView:
        return self.fv


def pipeline_to_ds_inputs(pipeline: Pipeline) -> Dict[str, DataSourceNode]:
    ds_nodes: Dict[str, DataSourceNode] = {}

    def _recurse_pipeline_to_ds_nodes(pipeline_node: PipelineNode, ds_nodes_: Dict[str, DataSourceNode]):
        if pipeline_node.HasField("data_source_node"):
            ds_nodes_[pipeline_node.data_source_node.input_name] = pipeline_node.data_source_node
        elif pipeline_node.HasField("transformation_node"):
            inputs = pipeline_node.transformation_node.inputs
            for input_ in inputs:
                _recurse_pipeline_to_ds_nodes(input_.node, ds_nodes_)

    _recurse_pipeline_to_ds_nodes(pipeline.root, ds_nodes)

    return ds_nodes


def pipeline_to_transformation_ids(pipeline: Pipeline) -> List[str]:
    id_list: List[str] = []

    def _recurse_pipeline_to_transformation_ids(node: PipelineNode, id_list: List[str]):
        if node.HasField("transformation_node"):
            id_list.append(IdHelper.to_string(node.transformation_node.transformation_id))
            for input in node.transformation_node.inputs:
                _recurse_pipeline_to_transformation_ids(input.node, id_list)
        return id_list

    _recurse_pipeline_to_transformation_ids(pipeline.root, id_list)
    return id_list
