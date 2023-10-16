import logging
import uuid

from tecton_core.offline_store import DeltaReader
from tecton_core.offline_store import OfflineStoreReaderParams
from tecton_core.query import nodes
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.pandas import nodes as pandas_nodes
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_rewriter import QueryTreeRewriter


logger = logging.getLogger(__name__)


class PandasTreeRewriter(QueryTreeRewriter):
    def rewrite(self, tree: NodeRef, prev_query_tree_step: QueryTreeStep, query_tree_compute: QueryTreeCompute) -> None:
        if prev_query_tree_step == QueryTreeStep.INIT:
            self._rewrite_init(tree, query_tree_compute)
            return

    def _rewrite_init(self, tree: NodeRef, query_tree_compute: QueryTreeCompute) -> None:
        """Finds all FeatureViewPipelineNodes, executes their subtrees, and replaces them with StagedTableScanNodes."""
        tree_node = tree.node

        if isinstance(tree_node, nodes.FeatureViewPipelineNode):
            pipeline_node = pandas_nodes.PandasFeatureViewPipelineNode.from_node_inputs(
                query_node=tree_node,
                input_node=None,
            )
            pipeline_result_df = pipeline_node.to_dataframe()
            staging_table_name = f"{pipeline_node.feature_definition_wrapper.name}_{uuid.uuid4().hex[:16]}_pandas"
            tree.node = nodes.StagedTableScanNode(
                staged_columns=pipeline_node.columns,
                staging_table_name=staging_table_name,
            )
            query_tree_compute.register_temp_table_from_pandas(staging_table_name, pipeline_result_df)
        else:
            for i in tree.inputs:
                self._rewrite_init(tree=i, query_tree_compute=query_tree_compute)


class OfflineScanTreeRewriter(QueryTreeRewriter):
    def rewrite(self, tree: NodeRef, prev_query_tree_step: QueryTreeStep, query_tree_compute: QueryTreeCompute) -> None:
        for i in tree.inputs:
            self.rewrite(tree=i, prev_query_tree_step=prev_query_tree_step, query_tree_compute=query_tree_compute)

        tree_node = tree.node
        if isinstance(tree_node, nodes.OfflineStoreScanNode):
            fdw = tree_node.feature_definition_wrapper
            reader_params = OfflineStoreReaderParams(path=fdw.materialized_data_path)
            reader = DeltaReader(params=reader_params, fd=fdw)
            table = reader.read(tree_node.partition_time_filter)

            staged_table_name = f"{fdw.name}_offline_store_scan_{uuid.uuid4().hex[:16]}"
            query_tree_compute.register_temp_table(staged_table_name, table)
            tree.node = nodes.StagedTableScanNode(
                staged_columns=tree_node.columns,
                staging_table_name=staged_table_name,
            )
