from enum import Enum

from tecton_core import conf
from tecton_core.query import sql_compat
from tecton_proto.common import compute_mode_pb2


class ComputeMode(str, Enum):
    """Represents the compute mode for training data generation queries."""

    SPARK = "spark"
    SNOWFLAKE = "snowflake"
    ATHENA = "athena"
    DUCK_DB = "duckdb"


def get_compute_mode() -> ComputeMode:
    """Returns the default ComputeMode based on the environment."""

    compute_mode = conf.get_or_raise("TECTON_COMPUTE_MODE")
    if compute_mode == ComputeMode.DUCK_DB:
        return ComputeMode.DUCK_DB
    elif conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED") or compute_mode == ComputeMode.SNOWFLAKE:
        return ComputeMode.SNOWFLAKE
    elif conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED") or compute_mode == ComputeMode.ATHENA:
        return ComputeMode.ATHENA
    elif compute_mode == ComputeMode.SPARK:
        return ComputeMode.SPARK
    else:
        msg = f"Invalid Tecton compute mode: {compute_mode}. Must be one of {[[e.value for e in ComputeMode]]}"
        raise ValueError(msg)


def ensure_correct_dialect_for_compute_mode():
    """Check the correct dialect is set for the compute mode, if not set 'SQL_DIALECT' to the correct language.

    Currently, this is only implemented for snowflake, but it can be extended to others."""

    if get_compute_mode() == ComputeMode.SNOWFLAKE and sql_compat.dialect() != sql_compat.Dialect.SNOWFLAKE:
        conf.set("SQL_DIALECT", "snowflake")


class BatchComputeMode(Enum):
    """Represents that compute mode for batch jobs associated with a FeatureView."""

    SPARK = compute_mode_pb2.ComputeMode.COMPUTE_MODE_SPARK
    SNOWFLAKE = compute_mode_pb2.ComputeMode.COMPUTE_MODE_SNOWFLAKE
    TECTON = compute_mode_pb2.ComputeMode.COMPUTE_MODE_TECTON

    @classmethod
    def from_string(cls, string) -> "BatchComputeMode":
        modes = {
            "spark": BatchComputeMode.SPARK,
            "snowflake": BatchComputeMode.SNOWFLAKE,
            "tecton": BatchComputeMode.TECTON,
        }
        if string in modes:
            return modes[string]
        else:
            choices = ", ".join(modes.keys().map(repr))
            msg = f"Invalid BatchComputeMode {repr(string)}. Must be one of: ${choices}."
            raise ValueError(msg)
