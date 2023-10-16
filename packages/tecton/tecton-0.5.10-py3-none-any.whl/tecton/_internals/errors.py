from datetime import datetime
from typing import Iterable
from typing import List
from typing import Set

from tecton._internals.utils import KEY_DELETION_MAX
from tecton.fco import Fco
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError

# Generic
INTERNAL_ERROR = lambda message: TectonInternalError(
    f"We seem to have encountered an error. Please contact support for assistance. Error details: {message}."
)
MDS_INACCESSIBLE = lambda host_port: TectonInternalError(
    f"Failed to connect to Tecton at {host_port}, please check your connectivity or contact support"
)
VALIDATION_ERROR_FROM_MDS = lambda message, trace_id: TectonValidationError(f"{message}, trace ID: {trace_id}")

INTERNAL_ERROR_FROM_MDS = lambda message, trace_id: TectonInternalError(
    f"Internal Tecton server error, please contact support with error details: {message}, trace ID: {trace_id}"
)

INVALID_SPINE_TYPE = lambda t: TectonValidationError(
    f"Invalid type of spine '{t}'. Spine must be an instance of [pyspark.sql.dataframe.DataFrame, " "pandas.DataFrame]."
)
UNSUPPORTED_OPERATION = lambda op, reason: TectonValidationError(f"Operation '{op}' is not supported: {reason}")
INVALID_SPINE_TIME_KEY_TYPE = lambda t: TectonValidationError(
    f"Invalid type of timestamp_key column in the given spine. Expected TimestampType, got {t}"
)
MISSING_SPINE_COLUMN = lambda param, col, existing_cols: TectonValidationError(
    f"{param} column is missing from the spine. Expected to find '{col}' among available spine columns: '{', '.join(existing_cols)}'."
)
MISSING_REQUEST_DATA_IN_SPINE = lambda key, existing_cols: TectonValidationError(
    f"Request context key '{key}' not found in spine schema. Expected to find '{key}' among available spine columns: '{', '.join(existing_cols)}'."
)
NONEXISTENT_WORKSPACE = lambda name, workspaces: TectonValidationError(
    f'Workspace "{name}" not found. Available workspaces: {workspaces}'
)
INCORRECT_MATERIALIZATION_ENABLED_FLAG = lambda user_set_bool, server_side_bool: TectonValidationError(
    f"'is_live={user_set_bool}' argument does not match the value on the server: {server_side_bool}"
)
UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE = lambda op: TectonValidationError(
    f"Operation '{op}' is not supported in a development workspace"
)
INVALID_JOIN_KEYS_TYPE = lambda t: TectonValidationError(
    f"Invalid type for join_keys. Expected Dict[str, Union[int, str, bytes]], got {t}"
)
INVALID_REQUEST_DATA_TYPE = lambda t: TectonValidationError(
    f"Invalid type for request_data. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
)
INVALID_REQUEST_CONTEXT_TYPE = lambda t: TectonValidationError(
    f"Invalid type for request_context_map. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
)


def INVALID_INDIVIDUAL_JOIN_KEY_TYPE(key: str, type_str: str):
    return TectonValidationError(
        f"Invalid type for join_key '{key}'. Expected either type int, str, or bytes, got {type_str}"
    )


def EMPTY_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not be empty.")


def EMPTY_ELEMENT_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have an empty element.")


def DUPLICATED_ELEMENTS_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have duplicated elements.")


def FCO_NOT_FOUND(fco: Fco, fco_reference: str):
    raise TectonValidationError(
        f"{fco._fco_type_name_singular_capitalized()} '{fco_reference}' not found. "
        f"Try running `tecton.list_{fco._fco_type_name_plural_snake_case()}()` to view all registered "
        f"{fco._fco_type_name_plural_capitalized()}"
    )


def DATA_SOURCE_NOT_FOUND(fco_reference: str):
    raise TectonValidationError(
        f"Data source '{fco_reference}' not found. "
        f"Try running `tecton.list_data_sources()` to view all registered BatchDataSource/StreamDataSource."
    )


def FCO_NOT_FOUND_WRONG_TYPE(fco: Fco, fco_reference: str, expected_method):
    raise TectonValidationError(
        f"{fco._fco_type_name_singular_capitalized()} '{fco_reference}' not found. "
        f"Did you mean tecton.{expected_method}?"
    )


def UNKNOWN_REQUEST_CONTEXT_KEY(keys, key):
    return TectonValidationError(f"Unknown request context key '{key}', expected one of: {keys}")


FV_NEEDS_TO_BE_BATCH_TRIGGER_MANUAL = lambda fv_name: TectonValidationError(
    f"FeatureView '{fv_name}' requires batch_trigger=BATCH_TRIGGER_TYPE_MANUAL to manually trigger materialization jobs"
)
FV_TIME_KEY_MISSING = lambda fv_name: TectonValidationError(
    f"Argument 'timestamp_key' is required for the feature definition '{fv_name}'"
)
FV_NO_MATERIALIZED_DATA = lambda fv_name: TectonValidationError(
    f"Feature definition '{fv_name}' doesn't have any materialized data. "
    "Materialization jobs may not have updated the offline feature store yet. "
    "Please monitor using materialization_status() or use from_source=True to compute from source data."
)

FV_NOT_SUPPORTED_PREVIEW = TectonValidationError(
    "This method cannot be used with this type of Feature Definition. Please use get_historical_features(spine=spine)."
)
FD_PREVIEW_NO_MATERIALIZED_OFFLINE_DATA = TectonValidationError(
    f"No materialized offline data found. If this Feature Definition was recently created,"
    + " its materialization backfill may still be in progress. This can be monitored using materialization_status()."
    + " In the meantime, you can set use_materialized_data=False on preview() to compute features directly from data sources."
)
FV_GET_FEATURE_DF_NO_SPINE = TectonValidationError("get_feature_dataframe() requires a 'spine' argument.")
FT_DF_TOO_LARGE = TectonValidationError(
    "Dataframe too large for a single ingestion, consider splitting into smaller ones"
)

FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE = lambda fd_name, workspace: TectonValidationError(
    f"Feature Definition {fd_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    "Please use from_source=True when getting features (not applicable for Feature Tables) or "
    "alternatively configure offline materialization for this Feature Definition in a live workspace."
)

FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE_GFD = lambda fv_name, workspace: TectonValidationError(
    f"Feature View {fv_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    "Please use use_materialized_data=False when getting features or "
    "alternatively configure offline materialization for this Feature View in a live workspace."
)

CBFV_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE = lambda fv_name, workspace: TectonValidationError(
    f"Feature view {fv_name} uses incremental backfills and is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    + "Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
    + "Enable offline materialization for this feature view in a live workspace to use `get_historical_features()`, or use `run()` to test this feature view without materializing data."
)

FD_GET_FEATURES_MATERIALIZATION_DISABLED = lambda fd_name: TectonValidationError(
    f"Feature Definition {fd_name} does not have offline materialization turned on. "
    f"Try calling this function with 'from_source=True' (not applicable for Feature Tables) "
    "or alternatively configure offline materialization for this Feature Definition."
)

FV_GET_FEATURES_MATERIALIZATION_DISABLED_GFD = lambda fv_name: TectonValidationError(
    f"Feature View {fv_name} does not have offline materialization turned on. "
    f"Try calling this function with 'use_materialized_data=False' "
    "or alternatively configure offline materialization for this Feature View."
)


def FT_UPLOAD_FAILED(reason):
    return TectonValidationError(f"Failed to upload dataframe: {reason}")


# DataSources
DS_STREAM_PREVIEW_ON_NON_STREAM = TectonValidationError("'start_stream_preview' called on non-streaming data source")

DS_DATAFRAME_NO_TIMESTAMP = TectonValidationError(
    "Cannot find timestamp column for this data source. Please call 'get_dataframe' without parameters 'start_time' or 'end_time'."
)

DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER = TectonValidationError(
    "The method 'get_dataframe()' cannot filter on timestamps when 'apply_translator' is False. "
    "'start_time' and 'end_time' must be None."
)

DS_INCORRECT_SUPPORTS_TIME_FILTERING = TectonValidationError(
    "Cannot filter on timestamps when supports_time_filtering on data source is False. "
    "'start_time' and 'end_time' must be None."
)


def FS_SPINE_JOIN_KEY_OVERRIDE_INVALID(spine_key, fv_key, possible_columns):
    return TectonValidationError(
        f"Spine join key '{spine_key}' (mapped from FeatureView join key '{fv_key}') not found in spine schema {possible_columns}"
    )


def FS_SPINE_TIMESTAMP_KEY_INVALID(timestamp_key, possible_columns):
    return TectonValidationError(f"Spine timestamp key '{timestamp_key}' not found in spine schema {possible_columns}")


def FS_BACKEND_ERROR(message):
    return TectonInternalError(f"Error calling Feature Service API: {message}")


FS_GET_FEATURE_VECTOR_REQUIRED_ARGS = TectonValidationError(
    "get_feature_vector requires at least one of join_keys or request_context_map"
)

FS_API_KEY_MISSING = TectonValidationError(
    "API key is required for online feature requests, but was not found in the environment. Please generate a key and set TECTON_API_KEY "
    + "using https://docs.tecton.ai/v2/examples/fetch-real-time-features.html#generating-an-api-key"
)

# Entity
def FV_INVALID_MOCK_SOURCES(mock_sources_keys: Iterable[str], fn_param: Iterable[str]):
    mock_sources_keys = mock_sources_keys if mock_sources_keys else set()
    return TectonValidationError(
        f"Mock sources' keys {mock_sources_keys} do not match FeatureView's parameters {fn_param}"
    )


def FV_INVALID_MOCK_INPUTS(mock_inputs: Set[str], inputs: Set[str]):
    input_names = str(mock_inputs) if mock_inputs else "{}"
    return TectonValidationError(f"Mock input names {input_names} do not match FeatureView's inputs {inputs}")


def FV_INVALID_MOCK_INPUTS_NUM_ROWS(num_rows: List[int]):
    return TectonValidationError(
        f"Number of rows are not equal across all mock_inputs. Number of rows found are: {str(num_rows)}."
    )


def FV_INVALID_MOCK_INPUT_SCHEMA(input_name: str, mock_columns: Set[str], expected_columns: Set[str]):
    return TectonValidationError(
        f"mock_inputs['{input_name}'] has mismatch schema columns {mock_columns}, expected {expected_columns}"
    )


def FV_UNSUPPORTED_ARG(invalid_arg_name: str):
    return TectonValidationError(f"Argument '{invalid_arg_name}' is not supported for this FeatureView type.")


def FV_INVALID_ARG_VALUE(arg_name: str, value: str, expected: str):
    return TectonValidationError(f"Invalid argument value '{arg_name}={value}', supported value(s): '{expected}'")


def FV_INVALID_ARG_COMBO(arg_names: List[str]):
    return TectonValidationError(f"Invalid argument combinations; {str(arg_names)} cannot be used together.")


FT_UNABLE_TO_ACCESS_SOURCE_DATA = lambda fv_name: TectonValidationError(
    f"The source data for FeatureTable {fv_name} does not exist. "
    "Please use from_source=False when calling this function."
)


def END_TIME_BEFORE_START_TIME(start_time: datetime, end_time: datetime):
    return TectonValidationError(f"start_time ({start_time}) must be less than end_time ({end_time}).")


class InvalidTransformationMode(TectonValidationError):
    def __init__(self, name: str, got: str, allowed_modes: List[str]):
        super().__init__(f"Transformation mode for '{name}' got '{got}', must be one of: {', '.join(allowed_modes)}")


class InvalidConstantType(TectonValidationError):
    def __init__(self, value, allowed_types):
        allowed_types = [str(allowed_type) for allowed_type in allowed_types]
        super().__init__(
            f"Tecton const value '{value}' must have one of the following types: {', '.join(allowed_types)}"
        )


class InvalidTransformInvocation(TectonValidationError):
    def __init__(self, transformation_name: str, got: str):
        super().__init__(
            f"Allowed arguments for Transformation '{transformation_name}' are: "
            f"tecton.const, tecton.materialization_context, transformations, and DataSource inputs. Got: '{got}'"
        )


# Dataset
DATASET_SPINE_COLUMNS_NOT_SET = TectonValidationError(
    "Cannot retrieve spine DF when Dataset was created without a spine."
)

# Feature Retrevial
def GET_HISTORICAL_FEATURES_WRONG_PARAMS(params: List[str], if_statement: str):
    return TectonValidationError("Cannot provide parameters " + ", ".join(params) + f" if {if_statement}")


FV_NOT_SUPPORTED_GET_HISTORICAL_FEATURES = TectonValidationError(
    "A spine must be provided to perform this method on an On-Demand Feature View. Please use get_historical_features(spine=spine)."
)

GET_ONLINE_FEATURES_REQUIRED_ARGS = TectonValidationError(
    "get_online_features requires at least one of join_keys or request_data to be set."
)

GET_ONLINE_FEATURES_ODFV_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this On-Demand Feature View since it has other Feature Views as inputs"
)

GET_ONLINE_FEATURES_FS_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this Feature Service"
)

GET_FEATURE_VECTOR_FS_JOIN_KEYS = TectonValidationError(
    "get_feature_vector requires the 'join_keys' argument for this Feature Service"
)

FS_GET_ONLINE_FEATURES_REQUIRED_ARGS = TectonValidationError(
    "get_online_features requires at least one of join_keys or request_data"
)


def GET_ONLINE_FEATURES_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError(f"The following required keys are missing in request_data: " + ", ".join(keys))


def GET_FEATURE_VECTOR_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError(f"The following required keys are missing in request_context_map: " + ", ".join(keys))


def GET_ONLINE_FEATURES_FS_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for this Feature Service since it contains an On-Demand Feature View. "
        + "Expected the following request data keys: "
        + ", ".join(keys)
    )


def GET_FEATURE_VECTOR_FS_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_feature_vector requires the 'request_context_map' argument for this Feature Service since it contains an On-Demand Feature View. "
        + "Expected the following request context keys: "
        + ", ".join(keys)
    )


def GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for On-Demand Feature Views. Expected the following request context keys: "
        + ", ".join(keys)
    )


def GET_FEATURE_VECTOR_FV_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_feature_vector requires the 'request_context_map' argument for On-Demand Feature Views. Expected the following request context keys: "
        + ", ".join(keys)
    )


FROM_SOURCE_WITH_FT = TectonValidationError(
    f"Computing features from source is not supported for Feature Tables. Try calling this method with from_source=False."
)

USE_MATERIALIZED_DATA_WITH_FT = TectonValidationError(
    f"Computing features from source is not supported for Feature Tables. Try calling this method with use_materialized_data=True."
)


FS_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    f"This Feature Service contains a Feature Table and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)


FV_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    f"This Feature View has a Feature Table input and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)


# Backfill Config Validation
BFC_MODE_SINGLE_REQUIRED_FEATURE_END_TIME_WHEN_START_TIME_SET = TectonValidationError(
    "feature_end_time is required when feature_start_time is set, for a FeatureView with "
    + "single_batch_schedule_interval_per_job backfill mode."
)

BFC_MODE_SINGLE_INVALID_FEATURE_TIME_RANGE = TectonValidationError(
    "Run with single_batch_schedule_interval_per_job backfill mode only supports time range equal to batch_schedule"
)

INCORRECT_KEYS = lambda keys, join_keys: TectonValidationError(
    f"Requested keys to be deleted ({keys}) do not match the expected join keys ({join_keys})."
)

NO_STORE_SELECTED = TectonValidationError(f"One of online or offline store must be selected.")

TOO_MANY_KEYS = TectonValidationError(f"Max number of keys to be deleted is {KEY_DELETION_MAX}.")

OFFLINE_STORE_NOT_SUPPORTED = TectonValidationError(
    "Only DeltaLake is supported for entity deletion in offline feature stores."
)

# FWv4
FV_UNSUPPORTED_AGGREGATION = TectonValidationError(
    f"Argument 'aggregation_level' is not supported for Feature Views with `aggregations` not specified."
)
INVALID_JOIN_KEY_TYPE = lambda t: TectonValidationError(
    f"Invalid type of join keys '{t}'. Keys must be an instance of [pyspark.sql.dataframe.DataFrame, "
    "pandas.DataFrame]."
)
DUPLICATED_COLS_IN_KEYS = lambda t: TectonValidationError(f"Argument keys {t} have duplicated column names. ")

MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS = lambda param: TectonValidationError(
    f"Snowflake connection is missing the variable {param}. Please ensure the following parameters are set when creating your snowflake connection:  database, warehouse, and schema. "
)

ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE = TectonValidationError(
    "Athena compute can only be used in live workspaces. Current workspace is not live. Please unset ALPHA_ATHENA_COMPUTE_ENABLED or switch to a live workspace."
)
