from typing import Dict
from typing import List
from typing import Tuple

import attrs

from tecton_core import schema_derivation_utils
from tecton_core.data_types import DataType
from tecton_core.data_types import data_type_from_proto
from tecton_core.errors import TectonValidationError
from tecton_proto.common import schema_pb2


@attrs.frozen
class Schema:
    proto: schema_pb2.Schema

    # TODO(jake): Remove this method. Just access proto attr directly.
    def to_proto(self):
        return self.proto

    def column_names(self):
        return [c.name for c in self.proto.columns]

    def column_name_and_data_types(self) -> List[Tuple[str, DataType]]:
        return [(c.name, data_type_from_proto(c.offline_data_type)) for c in self.proto.columns]

    def to_dict(self) -> Dict[str, DataType]:
        return dict(self.column_name_and_data_types())

    @classmethod
    def from_dict(cls, schema_dict):
        schema_proto = schema_pb2.Schema()
        for col_name, col_type in schema_dict.items():
            col = schema_proto.columns.add()
            col.CopyFrom(schema_derivation_utils.column_from_tecton_data_type(col_type))
            col.name = col_name
        return cls(proto=schema_proto)

    def __add__(self, other: "Schema") -> "Schema":
        if other is None:
            return self
        self_dict = self.to_dict()
        other_dict = other.to_dict()

        # Check if two schema share any column name with different types. This should never happen theoretically.
        shared_col_name = set(self_dict.keys()).intersection(set(other_dict.keys()))
        for col_name in shared_col_name:
            if self_dict[col_name] != other_dict[col_name]:
                msg = f"Column name '{col_name} has different data types: {str(self_dict[col_name])} VS {str(other_dict[col_name])}"
                raise TectonValidationError(msg)

        self_dict.update(other_dict)
        return self.from_dict(self_dict)
