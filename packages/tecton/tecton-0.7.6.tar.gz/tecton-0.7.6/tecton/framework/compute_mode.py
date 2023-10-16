from enum import Enum

from tecton_core import conf


class ComputeMode(str, Enum):
    SPARK = "spark"
    SNOWFLAKE = "snowflake"
    ATHENA = "athena"


def get_compute_mode() -> ComputeMode:
    """Returns the compute mode that Tecton is running in."""

    compute_mode = conf.get_or_raise("TECTON_COMPUTE_MODE")
    if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED") or compute_mode == ComputeMode.SNOWFLAKE:
        return ComputeMode.SNOWFLAKE
    elif conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED") or compute_mode == ComputeMode.ATHENA:
        return ComputeMode.ATHENA
    elif compute_mode == ComputeMode.SPARK:
        return ComputeMode.SPARK
    else:
        msg = f"Invalid Tecton compute mode: {compute_mode}. Must be one of {[[e.value for e in ComputeMode]]}"
        raise ValueError(msg)
