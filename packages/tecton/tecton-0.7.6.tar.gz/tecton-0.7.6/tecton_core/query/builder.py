from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import pendulum

from tecton_core import errors
from tecton_core import specs
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_definition_wrapper import pipeline_to_ds_inputs
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.feature_set_config import find_dependent_feature_set_items
from tecton_core.pipeline_common import get_time_window_from_data_source_node
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AddEffectiveTimestampNode
from tecton_core.query.nodes import AddRetrievalAnchorTimeNode
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinInputContainer
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import AsofWildcardExplodeNode
from tecton_core.query.nodes import ConvertEpochToTimestampNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFeatureStartTimeNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import SelectDistinctNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_core.query.nodes import WildcardJoinNode
from tecton_core.query.sql_compat import default_case
from tecton_core.query_consts import ANCHOR_TIME
from tecton_core.query_consts import EFFECTIVE_TIMESTAMP
from tecton_core.query_consts import EXPIRATION_TIMESTAMP
from tecton_core.query_consts import UDF_INTERNAL
from tecton_proto.args.pipeline_pb2 import DataSourceNode as ProtoDataSourceNode


WINDOW_END_COLUMN_NAME = "tile_end_time"


def build_datasource_scan_node(
    ds: specs.DataSourceSpec,
    for_stream: bool,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> NodeRef:
    return DataSourceScanNode(
        ds,
        ds_node=None,
        is_stream=for_stream,
        start_time=start_time,
        end_time=end_time,
    ).as_ref()


def _get_ds_time_limits(
    feature_data_time_limits: Optional[pendulum.Period],
    schedule_interval: Optional[pendulum.Duration],
    data_source_node: ProtoDataSourceNode,
) -> Tuple[Optional[datetime], Optional[datetime]]:
    ds_time_limits = get_time_window_from_data_source_node(
        feature_data_time_limits, schedule_interval, data_source_node
    )
    if ds_time_limits:
        return ds_time_limits.start, ds_time_limits.end
    return None, None


def build_datasource_input_querynodes(
    fdw: FeatureDefinitionWrapper, for_stream: bool, feature_data_time_limits: Optional[pendulum.Period] = None
) -> Dict[str, NodeRef]:
    """
    Starting in FWV5, data sources of FVs with incremental backfills may contain transformations that are only
    correct if the data has been filtered to a specific range.
    """
    schedule_interval = fdw.get_tile_interval if fdw.is_temporal else None
    ds_inputs = pipeline_to_ds_inputs(fdw.pipeline)

    input_querynodes = {}
    for input_name, node in ds_inputs.items():
        start_time, end_time = _get_ds_time_limits(feature_data_time_limits, schedule_interval, node)
        input_querynodes[input_name] = DataSourceScanNode(
            ds=fdw.fco_container.get_by_id_proto(node.virtual_data_source_id),
            ds_node=node,
            is_stream=for_stream,
            start_time=start_time,
            end_time=end_time,
        ).as_ref()
    return input_querynodes


def get_stream_watermark(fdw: FeatureDefinitionWrapper) -> Optional[str]:
    ds_inputs = pipeline_to_ds_inputs(fdw.pipeline)
    for input_name, node in ds_inputs.items():
        ds_spec = fdw.fco_container.get_by_id_proto(node.virtual_data_source_id)
        if ds_spec.stream_source is not None:
            watermark_delay_threshold_seconds = ds_spec.stream_source.watermark_delay_threshold.total_seconds()
            # NOTE: we do not want to set an explicit '0 seconds' watermark as
            # that can lead to data loss (data source functions supports
            # user-specified watermark configuration in function).
            if watermark_delay_threshold_seconds:
                return f"{watermark_delay_threshold_seconds} seconds"
    return None


# build QueryTree that executes all transformations
def build_pipeline_querytree(
    fdw: FeatureDefinitionWrapper, for_stream: bool, feature_data_time_limits: Optional[pendulum.Period] = None
) -> NodeRef:
    inputs_map = build_datasource_input_querynodes(fdw, for_stream, feature_data_time_limits)
    base = FeatureViewPipelineNode(
        inputs_map=inputs_map,
        feature_definition_wrapper=fdw,
        feature_time_limits=feature_data_time_limits,
    ).as_ref()
    if feature_data_time_limits:
        return FeatureTimeFilterNode(
            base,
            feature_data_time_limits=feature_data_time_limits,
            policy=fdw.time_range_policy,
            timestamp_field=fdw.timestamp_key,
        ).as_ref()
    return base


def build_materialization_querytree(
    fdw: FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    include_window_end_time: bool = False,
    aggregation_anchor_time: Optional[datetime] = None,
    enable_feature_metrics: bool = False,
) -> NodeRef:
    """Builds a querytree to construct a dataframe for materialization.

    For example, WAFVs are partially aggregated, and BFVs are augmented with an anchor time column. The resulting
    dataframe can also be easily modified to be used for `fv.run`.

    Args:
        fdw: The feature view to be materialized.
        for_stream: If True, the underlying data source is a streaming source.
        feature_data_time_limits: If set, the resulting features will be filtered with respect to these time limits.
        include_window_end_time: If True, a tile end time column with name "tile_end_time" will be included for WAFVs.
            Should only be set for WAFVs.
        aggregation_anchor_time: If set, it will be used as the offset for aggregations. Should only be set for WAFVs.
        enable_feature_metrics: If True, metrics will be collected on the querytree.
    """
    assert not for_stream or feature_data_time_limits is None, "Cannot run with time limits on a stream source"
    tree = build_pipeline_querytree(fdw, for_stream, feature_data_time_limits)
    if for_stream:
        watermark = get_stream_watermark(fdw)
        if watermark:
            tree = StreamWatermarkNode(tree, fdw.time_key, watermark).as_ref()
    if enable_feature_metrics:
        tree = MetricsCollectorNode(tree).as_ref()
    anchor_time_field = default_case(ANCHOR_TIME)
    if fdw.is_temporal:
        # BFVs require an anchor time column, but SFVs do not.
        if not for_stream:
            assert not include_window_end_time, "Not supported window end time for temporal"
            tree = AddAnchorTimeNode(
                tree,
                feature_store_format_version=fdw.get_feature_store_format_version,
                batch_schedule=fdw.get_batch_schedule_for_version,
                timestamp_field=fdw.timestamp_key,
            ).as_ref()
    elif fdw.is_temporal_aggregate:
        window_end_column_name = default_case(WINDOW_END_COLUMN_NAME) if include_window_end_time else None
        tree = PartialAggNode(
            tree,
            fdw=fdw,
            window_start_column_name=anchor_time_field,
            window_end_column_name=window_end_column_name,
            aggregation_anchor_time=aggregation_anchor_time,
        ).as_ref()
    else:
        msg = "unexpected FV type"
        raise Exception(msg)
    return tree


def build_get_features(
    fdw: FeatureDefinitionWrapper,
    from_source: Optional[bool],
    feature_data_time_limits: Optional[pendulum.Period] = None,
    aggregation_anchor_time: Optional[datetime] = None,
):
    # NOTE: this is ideally the *only* place where we validate
    # from_source arguments. However, until Snowflake and Athena are migrated
    # to QueryTree, we also need validations to live in the interactive/unified
    # SDK.
    #
    # Behavior:
    #   from_source is True: force compute from source
    #   from_source is False: force compute from materialized data
    #   from_source is None: compute from materialized data if feature
    #       definition offline=True, otherwise compute from source
    if from_source is None:
        from_source = not fdw.materialization_enabled or not fdw.writes_to_offline_store

    if from_source is False:
        assert not aggregation_anchor_time, "aggregation anchor time is not allowed when fetching features from source"
        if not fdw.materialization_enabled or not fdw.writes_to_offline_store:
            raise errors.FV_NEEDS_TO_BE_MATERIALIZED(fdw.name)
        return OfflineStoreScanNode(
            feature_definition_wrapper=fdw, partition_time_filter=feature_data_time_limits
        ).as_ref()
    else:
        # TODO(sanika) uncomment when athena has been migrated to querytree
        # if conf.get_or_none("SQL_DIALECT") == "athena":
        #     raise errors.TectonAthenaValidationError(
        #         "Features can only be read from the offline store when Athena compute is enabled. Please set from_source = False"
        #     )
        # TODO(TEC-13005)
        # TODO(pooja): raise an appropriate error here for push source
        if fdw.is_incremental_backfill:
            raise errors.FV_BFC_SINGLE_FROM_SOURCE
        return build_materialization_querytree(
            fdw,
            for_stream=False,
            feature_data_time_limits=feature_data_time_limits,
            aggregation_anchor_time=aggregation_anchor_time,
        )


def build_get_full_agg_features(
    fdw: FeatureDefinitionWrapper,
    from_source: Optional[bool],
    feature_data_time_limits: Optional[pendulum.Period] = None,
    respect_feature_start_time: bool = True,
    aggregation_anchor_time: Optional[datetime] = None,
    show_effective_time: bool = False,
):
    partial_aggs = build_get_features(
        fdw,
        from_source,
        feature_data_time_limits=feature_data_time_limits,
        aggregation_anchor_time=aggregation_anchor_time,
    )
    cols_to_drop = list(set(partial_aggs.columns) - set(list(fdw.join_keys) + [ANCHOR_TIME]))
    spine = RenameColsNode(partial_aggs, drop=cols_to_drop).as_ref()
    join = AsofJoinFullAggNode(
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
    ).as_ref()
    if respect_feature_start_time and fdw.feature_start_timestamp:
        join = RespectFeatureStartTimeNode.for_anchor_time_column(join, ANCHOR_TIME, fdw).as_ref()

    # The `AsofJoinFullAggNode` returned by `build_get_full_agg_features` converts timestamps to epochs. We convert back
    # from epochs to timestamps so that we can add an effective timestamp column.
    qt = ConvertEpochToTimestampNode(join, {ANCHOR_TIME: fdw.get_feature_store_format_version}).as_ref()

    # We want the time to be on the end of the window not the start.
    qt = AddDurationNode(
        qt,
        timestamp_field=ANCHOR_TIME,
        duration=fdw.get_tile_interval,
        new_column_name=fdw.trailing_time_window_aggregation.time_key,
    ).as_ref()
    qt = RenameColsNode(qt, drop=[ANCHOR_TIME]).as_ref()

    if show_effective_time:
        batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
        qt = AddEffectiveTimestampNode(
            qt,
            timestamp_field=fdw.trailing_time_window_aggregation.time_key,
            effective_timestamp_name=EFFECTIVE_TIMESTAMP,
            batch_schedule_seconds=batch_schedule_seconds,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
            is_stream=fdw.is_stream,
            is_temporal_aggregate=True,
        ).as_ref()

    return qt


def build_spine_join_querytree(
    dac: FeatureDefinitionAndJoinConfig, spine_node: NodeRef, spine_time_field: str, from_source: Optional[bool]
) -> NodeRef:
    fdw = dac.feature_definition
    if fdw.timestamp_key is not None and spine_time_field != fdw.timestamp_key:
        spine_node = RenameColsNode(spine_node, mapping={spine_time_field: fdw.timestamp_key}).as_ref()
    if any([jk[0] != jk[1] for jk in dac.join_keys]):
        spine_node = RenameColsNode(
            spine_node, mapping={jk[0]: jk[1] for jk in dac.join_keys if jk[0] != jk[1]}
        ).as_ref()

    if fdw.is_temporal or fdw.is_feature_table:
        ret = _build_spine_query_tree_temporal_or_feature_table(
            spine_node=spine_node,
            dac=dac,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
            from_source=from_source,
        )
    elif fdw.is_temporal_aggregate:
        augmented_spine = AddRetrievalAnchorTimeNode(
            spine_node,
            name=fdw.name,
            feature_store_format_version=fdw.get_feature_store_format_version,
            batch_schedule=fdw.get_batch_schedule_for_version,
            tile_interval=fdw.get_tile_interval_for_version,
            timestamp_field=fdw.timestamp_key,
            is_stream=fdw.is_stream,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
        ).as_ref()
        base = build_get_features(
            fdw,
            from_source=from_source,
            # NOTE: feature_data_time_limits is set to None since time pushdown
            # should happen as part of a optimization rewrite.
            feature_data_time_limits=None,
            aggregation_anchor_time=None,
        )

        anchor_time_field = default_case(ANCHOR_TIME)
        if fdw.wildcard_join_key is not None and fdw.wildcard_join_key not in spine_node.columns:
            augmented_spine = AsofWildcardExplodeNode(
                augmented_spine, anchor_time_field, base, anchor_time_field, fdw
            ).as_ref()

        join = AsofJoinFullAggNode(
            spine=augmented_spine,
            partial_agg_node=base,
            fdw=fdw,
        ).as_ref()

        if fdw.feature_start_timestamp:
            join = RespectFeatureStartTimeNode.for_anchor_time_column(join, anchor_time_field, fdw).as_ref()

        rename_map: Dict[str, Optional[str]] = {}
        cols_to_drop = [anchor_time_field]
        for f in fdw.features:
            if f not in dac.features:
                cols_to_drop.append(f)
            else:
                # TODO: make a helper
                rename_map[f] = f"{dac.namespace}{fdw.namespace_separator}{f}"
        ret = RenameColsNode(join, mapping=rename_map, drop=cols_to_drop).as_ref()
    elif fdw.is_on_demand:
        inputs = find_dependent_feature_set_items(
            fdw.fco_container,
            fdw.pipeline.root,
            visited_inputs={},
            fv_id=fdw.id,
        )
        dac = FeatureDefinitionAndJoinConfig.from_feature_definition(fdw)
        fsc = FeatureSetConfig(inputs + [dac])
        ret = build_feature_set_config_querytree(fsc, spine_node, spine_time_field, from_source)
    else:
        raise NotImplementedError
    if fdw.timestamp_key is not None and spine_time_field != fdw.timestamp_key:
        ret = RenameColsNode(ret, {fdw.timestamp_key: spine_time_field}).as_ref()
    if any([jk[0] != jk[1] for jk in dac.join_keys]):
        ret = RenameColsNode(ret, {jk[1]: jk[0] for jk in dac.join_keys if jk[0] != jk[1]}).as_ref()
    return ret


def _update_internal_cols(fdw: FeatureDefinitionWrapper, dac: FeatureDefinitionAndJoinConfig, internal_cols: Set[str]):
    if dac.namespace.startswith(UDF_INTERNAL):
        for feature in fdw.features:
            internal_cols.add(dac.namespace + fdw.namespace_separator + feature)
    for feature in dac.features:
        if UDF_INTERNAL in feature:
            internal_cols.add(feature)


# Construct each wildcard materialized fvtree by joining against distinct set of join keys.
# Then, outer join these using WildcardJoinNode which performs an outer join while handling null-valued features properly.
def _build_wild_fv_subtree(spine_node, fv_dacs, spine_time_field, from_source) -> NodeRef:
    newtree = None
    for dac in fv_dacs:
        fdw = dac.feature_definition

        subspine_join_keys = [jk[0] for jk in dac.join_keys if jk[0] != fdw.wildcard_join_key]
        # SelectDistinctNode is needed for correctness in order to filter out rows with duplicate join keys before
        # retrieving feature values. This avoids exploding wildcard rows when there are duplicates in both the spine and the
        # feature view tree.
        subspine = SelectDistinctNode(spine_node, subspine_join_keys + [spine_time_field]).as_ref()
        fvtree = build_spine_join_querytree(dac, subspine, spine_time_field, from_source)
        if len(dac.features) < len(fdw.features):
            fvtree = RenameColsNode(
                fvtree,
                drop=[f"{fdw.name}{fdw.namespace_separator}{f}" for f in fdw.features if f not in dac.features],
            ).as_ref()
        if newtree is None:
            newtree = fvtree
        else:
            join_cols = subspine_join_keys + [spine_time_field, fdw.wildcard_join_key]
            newtree = WildcardJoinNode(newtree, fvtree, join_cols=join_cols).as_ref()
    return newtree


# Construct each non-wildcard materialized fvtree by joining against distinct set of join keys.
# Then, outer join these fvtrees together.
def _build_standard_fv_subtree(spine_node, fv_dacs, spine_time_field, from_source):
    newtree = spine_node
    internal_cols = set()
    for dac in fv_dacs:
        fdw = dac.feature_definition
        _update_internal_cols(fdw, dac, internal_cols)

        subspine_join_keys = [jk[0] for jk in dac.join_keys]
        # SelectDistinctNode is needed for correctness in the case that there are duplicate rows in the spine. The
        # alternative considered was to add a row_id as a hash of the row or a monotonically increasing id, however the
        # row_id as a hash is not unique for duplicate rows and a monotonically increasing id is non-deterministic.
        subspine = SelectDistinctNode(spine_node, subspine_join_keys + [spine_time_field]).as_ref()
        fvtree = build_spine_join_querytree(dac, subspine, spine_time_field, from_source)
        if len(dac.features) < len(fdw.features):
            fvtree = RenameColsNode(
                fvtree,
                drop=[f"{fdw.name}{fdw.namespace_separator}{f}" for f in fdw.features if f not in dac.features],
            ).as_ref()
        newtree = JoinNode(newtree, fvtree, how="inner", join_cols=subspine_join_keys + [spine_time_field]).as_ref()
    return newtree, internal_cols


# Compute odfvs via udf on the parent (not using joins)
def _build_odfv_subtree(parent_tree: NodeRef, odfv_dacs: List[FeatureDefinitionAndJoinConfig]):
    newtree = parent_tree
    feature_definitions_namespaces = [(dac.feature_definition, dac.namespace) for dac in odfv_dacs]
    newtree = MultiOdfvPipelineNode(newtree, feature_definitions_namespaces).as_ref()

    # Compute the union of the features to be computed
    dac_features = set()
    fdw_features = set()
    for dac in odfv_dacs:
        feature_prefix = f"{dac.namespace}{dac.feature_definition.namespace_separator}"
        dac_features.update({f"{feature_prefix}{f}" for f in dac.features})
        fdw_features.update({f"{feature_prefix}{f}" for f in dac.feature_definition.features})

    # Drop features if user queried a subset via feature services
    if len(dac_features) < len(fdw_features):
        newtree = RenameColsNode(
            newtree,
            drop=[namespaced_feat for namespaced_feat in fdw_features if namespaced_feat not in dac_features],
        ).as_ref()
    return newtree


# Construct each materialized fvtree by joining against distinct set of join keys.
# Then, join the full spine against each of those.
# Finally, compute odfvs via udf on top of the result (not using joins)
def build_feature_set_config_querytree(
    fsc: FeatureSetConfig, spine_node: NodeRef, spine_time_field: str, from_source: Optional[bool]
) -> NodeRef:
    odfv_dacs: List[FeatureDefinitionAndJoinConfig] = []
    wildcard_dacs: List[FeatureDefinitionAndJoinConfig] = []
    normal_fv_dacs: List[FeatureDefinitionAndJoinConfig] = []

    for dac in fsc.definitions_and_configs:
        if dac.feature_definition.is_on_demand:
            odfv_dacs.append(dac)
        elif dac.feature_definition.wildcard_join_key is not None:
            if dac.feature_definition.wildcard_join_key in spine_node.columns:
                # Despite this being a wildcard FV, since we have the wildcard
                # key in the spine we will treat it like a normal FV.
                normal_fv_dacs.append(dac)
            else:
                wildcard_dacs.append(dac)
        else:
            normal_fv_dacs.append(dac)

    if wildcard_dacs:
        newtree = _build_wild_fv_subtree(spine_node, wildcard_dacs, spine_time_field, from_source)
    else:
        newtree = spine_node

    internal_cols = set()
    if normal_fv_dacs:
        newtree, internal_cols = _build_standard_fv_subtree(newtree, normal_fv_dacs, spine_time_field, from_source)

    if odfv_dacs:
        newtree = _build_odfv_subtree(newtree, odfv_dacs)

    # drop all internal cols
    if len(internal_cols) > 0:
        newtree = RenameColsNode(newtree, drop=list(internal_cols)).as_ref()

    return newtree


def _build_spine_query_tree_temporal_or_feature_table(
    spine_node: NodeRef, dac: FeatureDefinitionAndJoinConfig, data_delay_seconds: int, from_source: Optional[bool]
):
    fdw = dac.feature_definition
    TIMESTAMP_PLUS_TTL = default_case("_timestamp_plus_ttl")
    base = build_get_features(fdw, from_source=from_source)
    batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
    base = AddEffectiveTimestampNode(
        base,
        timestamp_field=fdw.timestamp_key,
        effective_timestamp_name=default_case(EFFECTIVE_TIMESTAMP),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=data_delay_seconds,
        is_stream=fdw.is_stream,
        is_temporal_aggregate=False,
    ).as_ref()
    if fdw.serving_ttl is not None:
        base = AddDurationNode(
            base, timestamp_field=fdw.timestamp_key, duration=fdw.serving_ttl, new_column_name=TIMESTAMP_PLUS_TTL
        ).as_ref()
        # Calculate effective expiration time = window(feature_time + ttl, batch_schedule).end + data_delay
        batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
        base = AddEffectiveTimestampNode(
            base,
            timestamp_field=TIMESTAMP_PLUS_TTL,
            effective_timestamp_name=default_case(EXPIRATION_TIMESTAMP),
            batch_schedule_seconds=batch_schedule_seconds,
            data_delay_seconds=data_delay_seconds,
            is_stream=fdw.is_stream,
            is_temporal_aggregate=False,
        ).as_ref()
    rightside_join_prefix = default_case("_tecton_right")
    join_prefixed_feature_names = [f"{rightside_join_prefix}_{f}" for f in fdw.features]
    # we can't just ask for the correct right_prefix to begin with because the asofJoin always sticks an extra underscore in between
    rename_map: Dict[str, Optional[str]] = {
        f"{rightside_join_prefix}_{f}": f"{dac.namespace}{fdw.namespace_separator}{f}"
        for f in fdw.features
        if f in dac.features
    }
    cols_to_drop = []
    for f in fdw.features:
        if f not in dac.features:
            cols_to_drop.append(f"{rightside_join_prefix}_{f}")
        else:
            rename_map[f"{rightside_join_prefix}_{f}"] = f"{dac.namespace}{fdw.namespace_separator}{f}"

    expiration_timestamp_col = f"{rightside_join_prefix}_{default_case(EXPIRATION_TIMESTAMP)}"

    cols_to_drop.append(f"{rightside_join_prefix}_{fdw.timestamp_key}")
    cols_to_drop.append(f"{rightside_join_prefix}_{default_case(ANCHOR_TIME)}")
    cols_to_drop.append(f"{rightside_join_prefix}_{default_case(EFFECTIVE_TIMESTAMP)}")
    if fdw.serving_ttl is not None:
        cols_to_drop.append(f"{rightside_join_prefix}_{default_case(TIMESTAMP_PLUS_TTL)}")
        cols_to_drop.append(expiration_timestamp_col)

    if fdw.feature_start_timestamp is not None:
        base = RespectFeatureStartTimeNode(
            base, fdw.timestamp_key, fdw.feature_start_timestamp, fdw.features, fdw.get_feature_store_format_version
        ).as_ref()

    if fdw.wildcard_join_key is not None and fdw.wildcard_join_key not in spine_node.columns:
        # Need to shallow copy base so that the left and right side are separate
        base_copy = NodeRef.shallow_copy(base)
        spine_node = AsofWildcardExplodeNode(
            spine_node, fdw.timestamp_key, base_copy, EFFECTIVE_TIMESTAMP, fdw
        ).as_ref()

    base = AsofJoinNode(
        left_container=AsofJoinInputContainer(spine_node, fdw.timestamp_key),
        right_container=AsofJoinInputContainer(
            base,
            timestamp_field=fdw.timestamp_key,
            effective_timestamp_field=default_case(EFFECTIVE_TIMESTAMP),
            prefix=rightside_join_prefix,
            schema=fdw.view_schema,
        ),
        join_cols=fdw.join_keys,
    ).as_ref()

    if fdw.serving_ttl is not None:
        base = RespectTTLNode(base, fdw.timestamp_key, expiration_timestamp_col, join_prefixed_feature_names).as_ref()
    # remove anchor cols/dupe timestamp cols
    return RenameColsNode(base, mapping=rename_map, drop=cols_to_drop).as_ref()
