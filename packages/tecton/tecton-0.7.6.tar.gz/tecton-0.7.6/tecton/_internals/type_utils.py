from typing import List
from typing import Union

from pyspark.sql import types as spark_types

from tecton import types as sdk_types
from tecton_core import data_types as tecton_types
from tecton_proto.common import schema_pb2
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


def to_column(field: sdk_types.Field) -> schema_pb2.Column:
    data_type = field.tecton_type().proto.data_type
    return schema_pb2.Column(name=field.name, offline_data_type=data_type)


def to_tecton_schema(fields: List[sdk_types.Field]) -> schema_pb2.Schema:
    columns = [to_column(field) for field in fields]
    return schema_pb2.Schema(columns=columns)


def to_spark_schema_wrapper(field_list: List[sdk_types.Field]) -> SparkSchemaWrapper:
    s = spark_types.StructType([field.spark_type() for field in field_list])
    return SparkSchemaWrapper(s)


def sdk_type_from_tecton_type(
    data_type: Union[tecton_types.DataType, tecton_types.StructType, tecton_types.ArrayType, tecton_types.MapType]
) -> Union[sdk_types.DataType, sdk_types.Array, sdk_types.Struct]:
    if isinstance(data_type, tecton_types.Int64Type):
        return sdk_types.Int64
    elif isinstance(data_type, tecton_types.Float32Type):
        return sdk_types.Float32
    elif isinstance(data_type, tecton_types.Float64Type):
        return sdk_types.Float64
    elif isinstance(data_type, tecton_types.StringType):
        return sdk_types.String
    elif isinstance(data_type, tecton_types.BoolType):
        return sdk_types.Bool
    elif isinstance(data_type, tecton_types.TimestampType):
        return sdk_types.Timestamp
    elif isinstance(data_type, tecton_types.ArrayType):
        return sdk_types.Array(sdk_type_from_tecton_type(data_type.element_type))
    elif isinstance(data_type, tecton_types.StructType):
        fields = [sdk_types.Field(field.name, sdk_type_from_tecton_type(field.data_type)) for field in data_type.fields]
        return sdk_types.Struct(fields)
    elif isinstance(data_type, tecton_types.MapType):
        return sdk_types.Map(
            sdk_type_from_tecton_type(data_type.key_type), sdk_type_from_tecton_type(data_type.value_type)
        )
    else:
        msg = f"{data_type} is not a recognized data types."
        raise NotImplementedError(msg)
