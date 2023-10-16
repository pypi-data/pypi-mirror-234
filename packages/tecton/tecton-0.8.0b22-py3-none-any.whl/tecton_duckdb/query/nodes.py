from typing import Dict
from typing import List
from typing import Tuple

import attrs
from pypika.functions import Cast
from pypika.terms import Term

from tecton_core.data_types import ArrayType
from tecton_core.data_types import DataType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.query import nodes
from tecton_core.query.node_interface import QueryNode


@attrs.frozen
class PartialAggDuckDbNode(nodes.PartialAggNode):
    data_type_to_sql_type: Dict[DataType, str] = {Int32Type(): "Int32", Float32Type(): "Float", Float64Type(): "Double"}

    @classmethod
    def from_query_node(cls, query_node: nodes.PartialAggNode) -> QueryNode:
        return cls(
            input_node=query_node.input_node,
            fdw=query_node.fdw,
            window_start_column_name=query_node.window_start_column_name,
            window_end_column_name=query_node.window_end_column_name,
            aggregation_anchor_time=query_node.aggregation_anchor_time,
        )

    def _get_partial_agg_columns_and_names(self) -> List[Tuple[Term, str]]:
        """
        Primarily overwritten to do additional type casts to make DuckDB's post-aggregation types consistent with Spark

        The two main cases:
        - Integer SUMs: DuckDB will automatically convert all integer SUMs to cast to DuckDB INT128's, regardless
        of its original type. Note that when copying this out into parquet, DuckDB will convert these to doubles.
        - Averages: DuckDB will always widen the precision to doubles

        Spark, in contrast, maintains the same type for both of these cases
        """
        normal_agg_cols_with_names = super()._get_partial_agg_columns_and_names()
        schema = self.fdw.materialization_schema.to_dict()

        final_agg_cols = []
        for col, alias in normal_agg_cols_with_names:
            data_type = schema[alias]
            if isinstance(data_type, ArrayType):
                data_type = data_type.element_type
                is_array = True
            else:
                is_array = False

            sql_type = self.data_type_to_sql_type.get(data_type, str(data_type))
            sql_type += "[]" if is_array else ""

            final_agg_cols.append((Cast(col, sql_type), alias))

        return final_agg_cols
