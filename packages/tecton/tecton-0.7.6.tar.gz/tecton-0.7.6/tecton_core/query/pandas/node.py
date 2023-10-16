from __future__ import annotations

from abc import abstractmethod
from typing import List

import attrs
import pandas

from tecton_core.query import node_interface
from tecton_core.query.pandas.sql import SqlExecutor


# SqlExecNodes are responsible for executing the sql string produced by the query node and using its SqlExecutor to
# output a pandas dataframe
@attrs.frozen
class SqlExecNode:
    columns: List[str]
    sql_string: str
    sql_executor: SqlExecutor

    @classmethod
    def from_sql_inputs(cls, query_node: node_interface.QueryNode, sql_executor: SqlExecutor):
        return cls(columns=query_node.columns, sql_string=query_node.to_sql(), sql_executor=sql_executor)  # type: ignore

    def to_dataframe(self) -> pandas.DataFrame:
        df = self._to_dataframe()
        if set([c.lower() for c in df.columns]) != set([c.lower() for c in self.columns]):
            pass
            # Because we do not refresh schemas on data sources, we can sometimes get different columns than what we have
            # cached. This is problematic but will require separate solution; don't fail for now
            # raise RuntimeError(f"Returned mismatch of columns: received: {df.columns}, expected: {self.columns}")
        return df

    def _to_dataframe(self) -> pandas.DataFrame:
        if self.sql_executor is None:
            msg = "SQL Executor must not be None"
            raise ValueError(msg)
        pandas_df = self.sql_executor.read_sql(self.sql_string)
        return pandas_df


# PandasExecNodes are responsible for taking in a pandas dataframe, performing some pandas operation and outputting a
# pandas dataframe
@attrs.frozen
class PandasExecNode:
    columns: List[str]
    input_node: PandasExecNode

    @classmethod
    def from_node_inputs(cls, query_node: node_interface.QueryNode, input_node: PandasExecNode):
        kwargs = attrs.asdict(query_node, recurse=False)
        kwargs["input_node"] = input_node
        kwargs["columns"] = query_node.columns
        return cls(**kwargs)

    def to_dataframe(self) -> pandas.DataFrame:
        df = self._to_dataframe()
        if set([c.lower() for c in df.columns]) != set([c.lower() for c in self.columns]):
            pass
            # Because we do not refresh schemas on data sources, we can sometimes get different columns than what we have
            # cached. This is problematic but will require separate solution; don't fail for now
            # raise RuntimeError(f"Returned mismatch of columns: received: {df.columns}, expected: {self.columns}")
        return df

    @abstractmethod
    def _to_dataframe(self) -> pandas.DataFrame:
        raise NotImplementedError
