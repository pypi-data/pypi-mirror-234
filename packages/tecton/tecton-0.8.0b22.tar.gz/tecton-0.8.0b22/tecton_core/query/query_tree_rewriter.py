from abc import ABC
from abc import abstractmethod

from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.query_tree_compute import QueryTreeCompute


class QueryTreeRewriter(ABC):
    @abstractmethod
    def rewrite(self, tree: NodeRef, query_tree_step: QueryTreeStep, query_tree_compute: QueryTreeCompute) -> None:
        raise NotImplementedError
