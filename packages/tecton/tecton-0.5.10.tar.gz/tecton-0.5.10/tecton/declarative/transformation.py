import functools
from dataclasses import dataclass
from dataclasses import field
from inspect import signature
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from google.protobuf.empty_pb2 import Empty
from pyspark.sql import DataFrame
from typeguard import typechecked

from tecton._internals import errors
from tecton._internals.fco import Fco
from tecton._internals.repo import function_serialization as func_ser
from tecton.cli.common import get_fco_source_info
from tecton.declarative.basic_info import prepare_basic_info
from tecton_core import function_deserialization as func_deser
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.id_helper import IdHelper
from tecton_proto.args.new_transformation_pb2 import NewTransformationArgs as TransformationArgs
from tecton_proto.args.new_transformation_pb2 import TransformationMode
from tecton_proto.args.pipeline_pb2 import Input
from tecton_proto.args.pipeline_pb2 import MaterializationContextNode
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.repo_metadata_pb2 import SourceInfo
from tecton_proto.common.id_pb2 import Id
from tecton_spark.materialization_context import materialization_context
from tecton_spark.materialization_context import UnboundMaterializationContext

SPARK_SQL_MODE = "spark_sql"
PYSPARK_MODE = "pyspark"
SNOWFLAKE_SQL_MODE = "snowflake_sql"
SNOWPARK_MODE = "snowpark"
ATHENA_MODE = "athena"
PANDAS_MODE = "pandas"
PYTHON_MODE = "python"

# TODO(jake): This global list can be removed after the 0.3 "compat" objects are cleaned up.
_GLOBAL_TRANSFORMATIONS_LIST = []


class Constant:
    ALLOWED_TYPES = [str, int, float, bool, type(None)]

    def __init__(self, value: Optional[Union[str, int, float, bool]]):
        self.value = value
        self.value_type = type(value)

        if self.value_type not in self.ALLOWED_TYPES:
            raise errors.InvalidConstantType(value, self.ALLOWED_TYPES)

    def __repr__(self):
        return f"Constant(value={self.value}, type={self.value_type})"


def const(value: Optional[Union[str, int, float, bool]]) -> Constant:
    """
    Wraps a const and returns a ``Constant`` object that can be used inside pipeline functions.

    :param value: The constant value that needs to be wrapped and used in the pipeline function.
    :return: A Constant object.
    """
    return Constant(value)


@dataclass
class Transformation(Fco):
    """
    (Tecton Object) Transformation class.
    """

    name: str
    mode: str
    user_function: Callable[..., Union[str, DataFrame]]
    description: str
    owner: str
    family: Optional[str]  # TODO: delete attribute with compat
    tags: Dict[str, str]
    _source_info: SourceInfo = field(init=False, repr=False)
    _args: TransformationArgs = field(init=False, repr=False)
    _ARGUMENT_TYPE = Union[PipelineNode, Constant, UnboundMaterializationContext]

    def _docstring(self):
        return None

    @property
    def transformer(self):
        return func_deser.from_proto(self._args.user_function)

    def _is_builtin(self):
        return False

    def __post_init__(self):
        self._source_info = get_fco_source_info()

        self._args = TransformationArgs()
        self._args.transformation_id.CopyFrom(IdHelper.from_string(IdHelper.generate_string_id()))
        self._args.version = FrameworkVersion.FWV5.value
        self._args.info.CopyFrom(
            prepare_basic_info(
                name=self.name, description=self.description, owner=self.owner, family=self.family, tags=self.tags
            )
        )
        if self.mode == SPARK_SQL_MODE:
            transform_mode = TransformationMode.TRANSFORMATION_MODE_SPARK_SQL
        elif self.mode == PYSPARK_MODE:
            transform_mode = TransformationMode.TRANSFORMATION_MODE_PYSPARK
        elif self.mode == SNOWFLAKE_SQL_MODE:
            transform_mode = TransformationMode.TRANSFORMATION_MODE_SNOWFLAKE_SQL
        elif self.mode == SNOWPARK_MODE:
            transform_mode = TransformationMode.TRANSFORMATION_MODE_SNOWPARK
        elif self.mode == ATHENA_MODE:
            transform_mode = TransformationMode.TRANSFORMATION_MODE_ATHENA
        elif self.mode == PANDAS_MODE:
            transform_mode = TransformationMode.TRANSFORMATION_MODE_PANDAS
        elif self.mode == PYTHON_MODE:
            transform_mode = TransformationMode.TRANSFORMATION_MODE_PYTHON
        else:
            raise errors.InvalidTransformationMode(
                self.name,
                self.mode,
                [
                    SPARK_SQL_MODE,
                    PYSPARK_MODE,
                    SNOWFLAKE_SQL_MODE,
                    SNOWPARK_MODE,
                    ATHENA_MODE,
                    PANDAS_MODE,
                    PYTHON_MODE,
                ],
            )
        if self._docstring() is not None:
            self._args.docstring = self._docstring()
        self._args.transformation_mode = transform_mode
        self._args.user_function.CopyFrom(func_ser.to_proto(self.user_function))
        self._args.is_builtin = self._is_builtin()
        if not self._is_builtin():
            Fco._register(self)
        _GLOBAL_TRANSFORMATIONS_LIST.append(self)

    def _args_proto(self) -> TransformationArgs:
        return self._args

    def __call__(self, *args, **kwargs) -> PipelineNode:
        wrapper = PipelineNode()
        node = wrapper.transformation_node
        node.transformation_id.CopyFrom(self._args.transformation_id)

        try:
            bound_user_function = signature(self.user_function).bind(*args, **kwargs)
        except TypeError as e:
            raise TypeError(f"while binding inputs to function {self.name}, TypeError: {e}")

        materialization_context_count = 0

        for i, arg in enumerate(args):
            input_ = Input()
            input_.arg_index = i
            input_.node.CopyFrom(self._value_to_node(arg))
            node.inputs.append(input_)
            if isinstance(arg, UnboundMaterializationContext):
                materialization_context_count += 1
        for name, arg in kwargs.items():
            input_ = Input()
            input_.arg_name = name
            input_.node.CopyFrom(self._value_to_node(arg))
            node.inputs.append(input_)
            if isinstance(arg, UnboundMaterializationContext):
                materialization_context_count += 1

        for param in signature(self.user_function).parameters.values():
            if isinstance(param.default, UnboundMaterializationContext):
                if param.name in bound_user_function.arguments:
                    # the user passed in context explicitly, so no need to double register
                    continue
                input_ = Input()
                input_.arg_name = param.name
                input_.node.CopyFrom(self._value_to_node(param.default))
                node.inputs.append(input_)
                if isinstance(param.default, UnboundMaterializationContext):
                    materialization_context_count += 1
            elif param.default is materialization_context:
                raise Exception(
                    "It seems you passed in tecton.materialization_context. Did you mean tecton.materialization_context()?"
                )

        if materialization_context_count > 1:
            raise Exception(f"Only 1 materialization_context can be passed into transformation {self.name}")

        return wrapper

    def _value_to_node(self, arg: _ARGUMENT_TYPE) -> PipelineNode:
        if isinstance(arg, PipelineNode):
            return arg
        elif isinstance(arg, Constant):
            wrapper = PipelineNode()
            node = wrapper.constant_node
            if arg.value is None:
                node.null_const.CopyFrom(Empty())
            elif arg.value_type == str:
                node.string_const = arg.value
            elif arg.value_type == int:
                node.int_const = repr(arg.value)
            elif arg.value_type == float:
                node.float_const = repr(arg.value)
            elif arg.value_type == bool:
                node.bool_const = arg.value
            return wrapper
        elif isinstance(arg, UnboundMaterializationContext):
            wrapper = PipelineNode()
            wrapper.materialization_context_node.CopyFrom(MaterializationContextNode())
            assert wrapper.HasField("materialization_context_node")
            return wrapper
        else:
            raise errors.InvalidTransformInvocation(self.name, arg)

    @property
    def _id(self) -> Id:
        return self._args.transformation_id

    def __hash__(self):
        return hash(self.name)


@typechecked
def transformation(
    mode: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
):
    """
    Declares a Transformation that wraps a user function. Transformations are assembled in a pipeline function of a Feature View.

    :param mode: The mode for this transformation must be one of "spark_sql", "pyspark", "snowflake_sql", "snowpark", "athena", "pandas" or "python".
    :param name: Unique, human friendly name that identifies the Transformation. Defaults to the function name.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :return: A wrapped transformation

    Examples of Spark SQL, PySpark, Pandas, and Python transformation declarations:

        .. code-block:: python

            from tecton import transformation
            from pyspark.sql import DataFrame
            import pandas as pd

            # Create a Spark SQL transformation.
            @transformation(mode="spark_sql",
                            description="Create new column by splitting the string in an existing column")
            def str_split(input_data, column_to_split, new_column_name, delimiter):
                return f'''
                    SELECT
                        *,
                        split({column_to_split}, {delimiter}) AS {new_column_name}
                    FROM {input_data}
                '''

             # Create an Athena transformation.
             @transformation(mode="athena",
                             description="Create new column by splitting the string in an existing column")
             def str_split(input_data, column_to_split, new_column_name, delimiter):
                 return f'''
                     SELECT
                         *,
                         split({column_to_split}, '{delimiter}') AS {new_column_name}
                     FROM {input_data}
                 '''

            # Create a PySpark transformation.
            @transformation(mode="pyspark",
                            description="Add a new column 'user_has_good_credit' if score is > 670")
            def user_has_good_credit_transformation(credit_scores):
                from pyspark.sql import functions as F

                (df = credit_scores.withColumn("user_has_good_credit",
                    F.when(credit_scores["credit_score"] > 670, 1).otherwise(0))
                return df.select("user_id", df["date"].alias("timestamp"), "user_has_good_credit") )

            # Create a Pandas transformation.
            @transformation(mode="pandas",
                            description="Whether the transaction amount is considered high (over $10000)")
            def transaction_amount_is_high(transaction_request):
                import pandas as pd

                df = pd.DataFrame()
                df['amount_is_high'] = (request['amount'] >= 10000).astype('int64')
                return df

            @transformation(mode="python",
                            description="Whether the transaction amount is considered high (over $10000)")
            # Create a Python transformation.
            def transaction_amount_is_high(transaction_request):

                result = {}
                result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
                return result
    """

    def decorator(user_function):
        transform_name = name or user_function.__name__
        transform = Transformation(transform_name, mode, user_function, description, owner, family=None, tags=tags)
        functools.update_wrapper(wrapper=transform, wrapped=user_function)

        return transform

    return decorator
