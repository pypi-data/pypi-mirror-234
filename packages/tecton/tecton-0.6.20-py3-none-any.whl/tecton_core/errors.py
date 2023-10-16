from datetime import datetime
from typing import List


class TectonValidationError(ValueError):
    """
    Exception that indicates a problem in validating user inputs against
    the data in the system. Typically recoverable by the user.
    """


class AccessError(ValueError):
    """
    Exception that indicates a problem in accessing raw data. Information about connecting to data sources can be found here:
    https://docs.tecton.ai/v2/setting-up-tecton/03-connecting-data-sources.html
    """


class TectonInternalError(RuntimeError):
    """
    Exception that indicates an unexpected error within Tecton.
    Can be persistent or transient. Recovery typically requires involving
    Tecton support.
    """


class InvalidDatabricksTokenError(Exception):
    """
    Exception that indicates user's databricks token is invalid.
    """


class TectonSnowflakeNotImplementedError(NotImplementedError):
    """
    Exception that indicates a feature is not yet implemented with Snowflake compute.
    """


class TectonAPIValidationError(ValueError):
    """
    Exception that indicates a problem in validating user inputs against
    the data in the system. Typically recoverable by the user.
    """


class TectonNotFoundError(Exception):
    """
    Exception that indicates that the user's request cannot be found in the system.
    """


class TectonAPIInaccessibleError(Exception):
    """
    Exception that indicates a problem connecting to Tecton cluster.
    """


class FailedPreconditionError(Exception):
    """
    Exception that indicates some prequisite has not been met (e.g the CLI/SDK needs to be updated).
    """


def INGEST_DF_MISSING_COLUMNS(columns: List[str]):
    return TectonValidationError(f"Missing columns in the DataFrame: {', '.join(columns)}")


def INGEST_COLUMN_TYPE_MISMATCH(column_name: str, expected_type: str, actual_type: str):
    return TectonValidationError(
        f"Column type mismatch for column '{column_name}', expected {expected_type}, got {actual_type}"
    )


def UDF_ERROR(error: Exception):
    return TectonValidationError(
        "UDF Error: please review and ensure the correctness of your feature definition and the input data passed in. Otherwise please contact Tecton Support for assistance."
        + f" Running the transformation resulted in the following error: {type(error).__name__}: {str(error)} "
    )


def INVALID_SPINE_SQL(error: Exception):
    return TectonValidationError(
        f"Invalid SQL: please review your SQL for the spine passed in. Received error: {type(error).__name__}: {str(error)} "
    )


def START_TIME_NOT_BEFORE_END_TIME(start_time: datetime, end_time: datetime):
    return TectonValidationError(f"start_time ({start_time}) must be less than end_time ({end_time}).")


def DS_ARGS_MISSING_FIELD(ds_type: str, field: str):
    return TectonValidationError(f"{ds_type} data source args must contain field {field}.")


REDSHIFT_DS_EITHER_TABLE_OR_QUERY = TectonValidationError(
    "Redshift data source must contain either table or query, but not both."
)


REDSHIFT_DS_MISSING_SPARK_TEMP_DIR = TectonValidationError(
    'Cannot use a locally defined Redshift data source without a tempdir, e.g. spark.read.format("redshift").option("tempdir", "s3a:///"). See the tempdir that Tecton should use via tecton.conf.set("SPARK_REDSHIFT_TEMP_DIR", <your path>) or by setting the SPARK_REDSHIFT_TEMP_DIR= as an environment variable.'
)


class TectonAthenaValidationError(TectonValidationError):
    """
    Exception that indicates a ValidationError with Athena.
    """


class TectonAthenaNotImplementedError(NotImplementedError):
    """
    Exception that indicates a feature is not yet implemented with Athena compute.
    """


FV_BFC_SINGLE_FROM_SOURCE = TectonValidationError(
    f"Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
    + "Enable offline materialization for this feature view in a live workspace to use `get_historical_features()`. Alternatively, use `run()` to test this feature view without materializing data."
)
FV_NEEDS_TO_BE_MATERIALIZED = lambda fv_name: TectonValidationError(
    f"Feature View '{fv_name}' has not been configured for materialization. "
    + "Please use from_source=True when getting features or "
    + "configure offline materialization for this Feature View in a live workspace."
)

FT_DF_TOO_LARGE = TectonValidationError(
    "Dataframe too large for a single ingestion, consider splitting into smaller ones"
)


def FT_UPLOAD_FAILED(reason):
    return TectonValidationError(f"Failed to upload dataframe: {reason}")
