from tecton_core import data_types as tecton_types
from tecton_core import errors
from tecton_proto.common import data_type_pb2


# Keep in sync with DataTypeUtils.kt
def snowflake_type_to_tecton_type(snowflake_type: str, column_name: str) -> tecton_types.DataType:
    if snowflake_type == "VARCHAR":
        return tecton_types.StringType()
    elif snowflake_type == "NUMBER":
        return tecton_types.Int64Type()
    elif snowflake_type == "FLOAT":
        return tecton_types.Float64Type()
    elif snowflake_type == "BOOLEAN":
        return tecton_types.BoolType()
    elif snowflake_type == "TIMESTAMP_NTZ":
        return tecton_types.TimestampType()
    elif snowflake_type == "TIMESTAMP_TZ" or snowflake_type == "TIMESTAMP_LTZ":
        raise errors.TectonValidationError(
            f"Timestamp type {snowflake_type} for column {column_name} is not supported because it contains a timezone.Please use TIMESTAMP_NTZ instead."
        )
    else:
        raise errors.TectonValidationError(f"Unsupported Snowflake type {snowflake_type} for column {column_name}.")


def tecton_type_to_snowflake_type(tecton_type_proto: data_type_pb2.DataType, column_name: str) -> str:
    tecton_type = tecton_types.data_type_from_proto(tecton_type_proto)
    if isinstance(tecton_type, tecton_types.StringType):
        return "VARCHAR"
    elif isinstance(tecton_type, tecton_types.Int64Type):
        return "NUMBER"
    elif isinstance(tecton_type, tecton_types.Float64Type):
        return "FLOAT"
    elif isinstance(tecton_type, tecton_types.BoolType):
        return "BOOLEAN"
    elif isinstance(tecton_type, tecton_types.TimestampType):
        return "TIMESTAMP_NTZ"
    elif isinstance(tecton_type, tecton_types.ArrayType) and isinstance(
        tecton_type.element_type, tecton_types.StringType
    ):
        return "ARRAY"
    else:
        raise errors.TectonValidationError(
            f"Unsupported tecton type {tecton_type} for column {column_name} on Snowflake."
        )
