from abc import ABC
from abc import abstractmethod
from typing import Type

from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode


class Rewrite(ABC):
    @abstractmethod
    def rewrite(self, node: NodeRef) -> NodeRef:
        raise NotImplementedError


def tree_contains(tree: NodeRef, node_type: Type[QueryNode]) -> bool:
    """Returns True if the tree contains a NodeRef of the given type, False otherwise."""
    if isinstance(tree.node, node_type):
        return True

    return any(tree_contains(subtree, node_type) for subtree in tree.inputs)
