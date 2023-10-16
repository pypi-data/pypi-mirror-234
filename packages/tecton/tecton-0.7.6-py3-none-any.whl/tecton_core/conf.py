import builtins
import contextlib
import json
import logging
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

from tecton_core import errors


logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)

_ConfigSettings = Dict[str, Any]

_CONFIG_OVERRIDES: _ConfigSettings = {}


class ConfSource(Enum):
    # (Always supported) This key can be overriden in the Python runtime.
    SESSION_OVERRIDE = 1
    # (Always supported) This key can be read from the local environment.
    OS_ENV = 2
    # This key can be written to and read from the tecton config file.
    LOCAL_TECTON_CONFIG = 3
    # This key can be written to and read from the tecton tokens file.
    LOCAL_TECTON_TOKENS = 4
    # This key can read from the MDS get-configs endpoint.
    REMOTE_MDS_CONFIG = 5
    # This key can read from the Databricks secrets manager.
    DATABRICKS_SECRET = 6
    # This key can read from the AWS secrets manager.
    AWS_SECRET_MANAGER = 7
    # The default value of this key was used. Used for debug printing. Not an "allowable" source.
    DEFAULT = 8
    # A value for this key was not found. Used for debug printing. Not an "allowable" source.
    NOT_FOUND = 9


RUNTIME_ALLOWED_SOURCES = (ConfSource.SESSION_OVERRIDE, ConfSource.OS_ENV)
DEFAULT_ALLOWED_SOURCES = (
    ConfSource.SESSION_OVERRIDE,
    ConfSource.OS_ENV,
    ConfSource.REMOTE_MDS_CONFIG,
    ConfSource.DATABRICKS_SECRET,
    ConfSource.AWS_SECRET_MANAGER,
)


class _Debugger(object):
    @classmethod
    def _debug_enabled(cls) -> bool:
        debug_value = _get_runtime_only("TECTON_DEBUG")
        return debug_value is not None and debug_value.lower() in ("1", "true", "yes")

    @classmethod
    def preamble(cls, key: str):
        if cls._debug_enabled():
            print(f"Looking up {key}", file=sys.stderr)

    @classmethod
    def print(cls, src: ConfSource, key: str, val: Optional[str] = None, details: Optional[str] = None):
        if not cls._debug_enabled():
            return

        if src == ConfSource.NOT_FOUND:
            print(f"Unable to find {key}\n", file=sys.stderr)
            return

        details_str = f"({details})" if details else ""
        val_str = val if val is not None else "not found"
        symbol_str = "[x]" if val is not None else "[ ]"
        print(symbol_str, f"{key} in {src.name} -> {val_str}", details_str, file=sys.stderr)


def set(key, value):
    _set(key, value)


def unset(key):
    del _CONFIG_OVERRIDES[key]


def _set(key, value):
    _CONFIG_OVERRIDES[key] = value


@contextlib.contextmanager
def _temporary_set(key, value):
    curr_val = _CONFIG_OVERRIDES.get(key)
    _CONFIG_OVERRIDES[key] = value
    try:
        yield
    finally:
        if curr_val:
            _CONFIG_OVERRIDES[key] = curr_val
        else:
            del _CONFIG_OVERRIDES[key]


def _does_key_have_valid_prefix(key) -> bool:
    for prefix in _VALID_KEY_PREFIXES:
        if key.startswith(prefix):
            return True
    return False


def _get(key) -> Optional[str]:
    """Get the config value for the given key, or return None if not found."""
    _Debugger.preamble(key)

    if key in _VALID_KEYS_TO_ALLOWED_SOURCES:
        allowed_sources = _VALID_KEYS_TO_ALLOWED_SOURCES[key]
    elif _does_key_have_valid_prefix(key):
        allowed_sources = DEFAULT_ALLOWED_SOURCES
    else:
        msg = f"Tried accessing invalid configuration key '{key}'"
        raise errors.TectonInternalError(msg)

    # Session-scoped override.
    if ConfSource.SESSION_OVERRIDE in allowed_sources:
        val = _CONFIG_OVERRIDES.get(key)
        _Debugger.print(ConfSource.SESSION_OVERRIDE, key, val)
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # Environment variable.
    if ConfSource.OS_ENV in allowed_sources:
        val = os.environ.get(key)
        _Debugger.print(ConfSource.OS_ENV, key, val)
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # ~/.tecton/config
    if ConfSource.LOCAL_TECTON_CONFIG in allowed_sources:
        val = _LOCAL_TECTON_CONFIG.get(key)
        _Debugger.print(ConfSource.LOCAL_TECTON_CONFIG, key, val, details=str(_LOCAL_TECTON_CONFIG_FILE))
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # ~/.tecton/config.tokens
    if ConfSource.LOCAL_TECTON_TOKENS in allowed_sources:
        val = _LOCAL_TECTON_TOKENS.get(key)
        _Debugger.print(ConfSource.LOCAL_TECTON_TOKENS, key, val, details=str(_LOCAL_TECTON_CONFIG_FILE))
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    # Config from MDS
    if ConfSource.REMOTE_MDS_CONFIG in allowed_sources:
        val = _REMOTE_MDS_CONFIGS.get(key)
        _Debugger.print(ConfSource.REMOTE_MDS_CONFIG, key, val)
        if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
            return val

    if _get_runtime_env() == TectonEnv.UNKNOWN:
        # Fallback attempt to set env if user has not set it.
        _set_tecton_runtime_env()

    # NOTE: although originally intended for internal use. Some customers have
    # found this configuration or have required this behavior. Care should be
    # exercised in changing any behavior here to ensure no customer breakages.
    if ConfSource.DATABRICKS_SECRET in allowed_sources and not _get_runtime_only("TECTON_CONF_DISABLE_DBUTILS"):
        # Databricks secrets
        for scope in _get_secret_scopes():
            value = _get_from_db_secrets(key, scope)
            _Debugger.print(ConfSource.DATABRICKS_SECRET, key, value, details=f"{scope}:{key}")
            if value is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
                return value

    # NOTE: although originally intended for internal use. Some customers have
    # found this configuration or have required this behavior. Care should be
    # exercised in changing any behavior here to ensure no customer breakages.
    if ConfSource.AWS_SECRET_MANAGER in allowed_sources and not _get_runtime_only("TECTON_CONF_DISABLE_AWS_SECRETS"):
        # AWS secret manager
        for scope in _get_secret_scopes():
            value = _get_from_secretsmanager(key, scope)
            _Debugger.print(ConfSource.AWS_SECRET_MANAGER, key, value, details=f"{scope}/{key}")
            if value is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
                return value

    if key in _DEFAULTS:
        value = _DEFAULTS[key]()
        _Debugger.print(ConfSource.DEFAULT, key, value)
        return value

    _Debugger.print(ConfSource.NOT_FOUND, key)
    return None


def _get_runtime_only(key) -> Optional[str]:
    """An alternate _get() that will look up only from runtime sources. Used to avoid infinite loops."""
    if key not in _VALID_KEYS_TO_ALLOWED_SOURCES:
        msg = f"_get_runtime_only should only used with valid keys. {key}"
        raise errors.TectonInternalError(msg)

    allowed_sources = _VALID_KEYS_TO_ALLOWED_SOURCES[key]
    # Use `builtins.set` since we shadowed the `set` built-in in this module.
    if builtins.set(allowed_sources) != builtins.set(RUNTIME_ALLOWED_SOURCES):
        msg = "_get_runtime_only should only used with keys that only allow run time sources."
        raise errors.TectonInternalError(msg)

    # Session-scoped override.
    val = _CONFIG_OVERRIDES.get(key)
    if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
        return val

    # Environment variable.
    val = os.environ.get(key)
    if val is not None:  # NOTE: check explicitly against None so we can set a value to False or ""
        return val

    if key in _DEFAULTS:
        value = _DEFAULTS[key]()
        return value

    return None


def get_or_none(key) -> Optional[str]:
    return _get(key)


def get_or_raise(key) -> str:
    val = _get(key)
    if val is None:
        msg = f"{key} not set"
        raise errors.TectonInternalError(msg)
    return val


def get_bool(key) -> bool:
    val = _get(key)
    if val is None:
        return False
    # bit of a hack for if people set a boolean value in a local override
    if isinstance(val, bool):
        return val
    if not isinstance(val, str):
        msg = f"{key} should be an instance of str, not {type(val)}"
        raise ValueError(msg)
    if val.lower() in {"yes", "true"}:
        return True
    if val.lower() in {"no", "false"}:
        return False
    msg = f"{key} should be 'true' or 'false', not {val}"
    raise ValueError(msg)


# Internal

_LOCAL_TECTON_CONFIG_FILE = Path(os.environ.get("TECTON_CONFIG_PATH", Path.home() / ".tecton/config"))
_LOCAL_TECTON_TOKENS_FILE = _LOCAL_TECTON_CONFIG_FILE.with_suffix(".tokens")

_VALID_KEYS_TO_ALLOWED_SOURCES = {
    "API_SERVICE": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_CONFIG,),
    "FEATURE_SERVICE": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_CONFIG,),
    "CLI_CLIENT_ID": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_CONFIG,),
    "TECTON_WORKSPACE": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_CONFIG,),
    "ALPHA_SNOWFLAKE_COMPUTE_ENABLED": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_CONFIG,),
    "TECTON_COMPUTE_MODE": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.REMOTE_MDS_CONFIG,
    ),
    "OAUTH_ACCESS_TOKEN": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_TOKENS,),
    "OAUTH_ACCESS_TOKEN_EXPIRATION": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_TOKENS,),
    "OAUTH_REFRESH_TOKEN": DEFAULT_ALLOWED_SOURCES + (ConfSource.LOCAL_TECTON_TOKENS,),
    # TECTON_CLUSTER_NAME is needed for looking up AWS and Databricks secrets. CLUSTER_REGION is used for looking up AWS
    # secrets. To avoid an infinite loop, these keys cannot be looked up from those sources.
    "TECTON_CLUSTER_NAME": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.REMOTE_MDS_CONFIG,
    ),
    "CLUSTER_REGION": (
        ConfSource.SESSION_OVERRIDE,
        ConfSource.OS_ENV,
        ConfSource.REMOTE_MDS_CONFIG,
        ConfSource.DATABRICKS_SECRET,
    ),
    # NOTE: TECTON_CONF* are meant for Tecton internal use.
    # TODO(TEC-8744): improve tecton.conf configurations such that end users have more
    # control of where secrets are fetched from.
    "SPARK_REDSHIFT_TEMP_DIR": RUNTIME_ALLOWED_SOURCES,
    "TECTON_CONF_DISABLE_DBUTILS": RUNTIME_ALLOWED_SOURCES,
    "TECTON_CONF_DISABLE_AWS_SECRETS": RUNTIME_ALLOWED_SOURCES,
    "TECTON_DEBUG": RUNTIME_ALLOWED_SOURCES,
    "TECTON_RUNTIME_ENV": RUNTIME_ALLOWED_SOURCES,
    "TECTON_RUNTIME_MODE": RUNTIME_ALLOWED_SOURCES,
    "TECTON_VALIDATION_MODE": RUNTIME_ALLOWED_SOURCES,
    "TECTON_FORCE_FUNCTION_SERIALIZATION": RUNTIME_ALLOWED_SOURCES,
    "TECTON_REPO_IGNORE_ALL_HIDDEN_DIRS": RUNTIME_ALLOWED_SOURCES,
    "SKIP_OBJECT_VERSION_CHECK": RUNTIME_ALLOWED_SOURCES,
    "ALPHA_ATHENA_COMPUTE_ENABLED": DEFAULT_ALLOWED_SOURCES,
    "SQL_DIALECT": DEFAULT_ALLOWED_SOURCES,
    "ATHENA_S3_PATH": DEFAULT_ALLOWED_SOURCES,
    "ATHENA_DATABASE": DEFAULT_ALLOWED_SOURCES,
    "ENABLE_TEMPO": DEFAULT_ALLOWED_SOURCES,
    "QUERY_REWRITE_ENABLED": DEFAULT_ALLOWED_SOURCES,
    "ALPHA_SNOWFLAKE_SNOWPARK_ENABLED": DEFAULT_ALLOWED_SOURCES,
    "AWS_ACCESS_KEY_ID": DEFAULT_ALLOWED_SOURCES,
    "AWS_SECRET_ACCESS_KEY": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_HOST": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_PORT": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_USERNAME": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_DATABASE": DEFAULT_ALLOWED_SOURCES,
    "HIVE_METASTORE_PASSWORD": DEFAULT_ALLOWED_SOURCES,
    "SPARK_DRIVER_LOCAL_IP": DEFAULT_ALLOWED_SOURCES,
    "METADATA_SERVICE": DEFAULT_ALLOWED_SOURCES,
    "TECTON_API_KEY": DEFAULT_ALLOWED_SOURCES,
    "QUERYTREE_SHORT_SQL_ENABLED": RUNTIME_ALLOWED_SOURCES,
    "REDSHIFT_USER": DEFAULT_ALLOWED_SOURCES,
    "REDSHIFT_PASSWORD": DEFAULT_ALLOWED_SOURCES,
    "SKIP_FEATURE_TIMESTAMP_VALIDATION": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_ACCOUNT_IDENTIFIER": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_DEBUG": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_SHORT_SQL_ENABLED": DEFAULT_ALLOWED_SOURCES,  # Whether to break up long SQL statements into temporary views for Snowflake
    "SNOWFLAKE_TEMP_TABLE_ENABLED": DEFAULT_ALLOWED_SOURCES,  # Whether to break up long SQL statements with temporary tables for Snowflake, takes precedence over SNOWFLAKE_SHORT_SQL_ENABLED
    "SNOWFLAKE_USER": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_PASSWORD": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_WAREHOUSE": DEFAULT_ALLOWED_SOURCES,
    "SNOWFLAKE_DATABASE": DEFAULT_ALLOWED_SOURCES,
    "REDIS_AUTH_TOKEN": DEFAULT_ALLOWED_SOURCES,
}

_VALID_KEY_PREFIXES = ["SECRET_"]


def _snowpark_enabled():
    ## Try to import snowpark, if it fails, return False
    try:
        import snowflake.snowpark  # noqa: F401

        return "true"
    except ImportError:
        return "false"


_DEFAULTS = {
    "TECTON_COMPUTE_MODE": (lambda: "spark"),
    "TECTON_WORKSPACE": (lambda: "prod"),
    "FEATURE_SERVICE": (lambda: _get("API_SERVICE")),
    "ALPHA_SNOWFLAKE_SNOWPARK_ENABLED": (_snowpark_enabled),
    "ENABLE_TEMPO": (lambda: "false"),
    "QUERY_REWRITE_ENABLED": (lambda: "true"),
    "SQL_DIALECT": (lambda: "spark"),
    "TECTON_VALIDATION_MODE": (lambda: "explicit"),
    "TECTON_REPO_IGNORE_ALL_HIDDEN_DIRS": (lambda: "true"),
}

_REMOTE_MDS_CONFIGS: _ConfigSettings = {}

_is_running_on_databricks_cache = None
_is_running_on_emr_cache = None
TectonEnv = Enum("TectonEnv", "DATABRICKS EMR UNKNOWN")


def _is_running_on_databricks():
    """Whether we're running in Databricks notebook or not."""
    global _is_running_on_databricks_cache
    if _is_running_on_databricks_cache is None:
        main = __import__("__main__")
        filename = os.path.basename(getattr(main, "__file__", ""))
        is_python_shell = filename == "PythonShell.py"
        is_databricks_env = "DBUtils" in main.__dict__
        _is_running_on_databricks_cache = is_python_shell and is_databricks_env
    return _is_running_on_databricks_cache


def _is_running_on_emr():
    """Whether we're running in EMR notebook or not."""
    global _is_running_on_emr_cache
    if _is_running_on_emr_cache is None:
        _is_running_on_emr_cache = "EMR_CLUSTER_ID" in os.environ
    return _is_running_on_emr_cache


def _set_tecton_runtime_env():
    key = "TECTON_RUNTIME_ENV"
    if _is_running_on_databricks():
        set(key, "DATABRICKS")
    elif _is_running_on_emr():
        set(key, "EMR")
    else:
        set(key, "UNKNOWN")


def _is_mode_materialization():
    runtime_mode = get_or_none("TECTON_RUNTIME_MODE")
    return runtime_mode == "MATERIALIZATION"


def _get_runtime_env():
    # Use _get_runtime_only() and not _get() to avoid an infinite loop.
    runtime_env = _get_runtime_only("TECTON_RUNTIME_ENV")
    if runtime_env == "DATABRICKS":
        return TectonEnv.DATABRICKS
    elif runtime_env == "EMR":
        return TectonEnv.EMR
    else:
        return TectonEnv.UNKNOWN


def _get_dbutils():
    # Returns dbutils import. Only works in Databricks notebook environment
    import IPython

    return IPython.get_ipython().user_ns["dbutils"]


def _get_keys_with_allowed_source(source: ConfSource) -> List[str]:
    """Returns all the keys that have the allowed ConfSource."""
    return [key for key, allowed_sources in _VALID_KEYS_TO_ALLOWED_SOURCES.items() if source in allowed_sources]


def save_tecton_configs():
    _save_tecton_config(_LOCAL_TECTON_CONFIG_FILE, _get_keys_with_allowed_source(ConfSource.LOCAL_TECTON_CONFIG))
    _save_tecton_config(_LOCAL_TECTON_TOKENS_FILE, _get_keys_with_allowed_source(ConfSource.LOCAL_TECTON_TOKENS))


def _save_tecton_config(path: Path, keys: Iterable[str]):
    tecton_config = {key: get_or_none(key) for key in keys if get_or_none(key) is not None}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(tecton_config, f, sort_keys=True, indent=2)
        f.write("\n")


# Get key by looking in TECTON_CLUSTER_NAME'd scope and falling back to "tecton"
def _get_secret_scopes():
    cluster_name = get_or_none("TECTON_CLUSTER_NAME")
    secret_scopes = []
    if cluster_name:
        secret_prefix = cluster_name if cluster_name.startswith("tecton-") else f"tecton-{cluster_name}"
        secret_scopes.append(secret_prefix)
    secret_scopes.append("tecton")
    return secret_scopes


def _get_from_secretsmanager(key: str, scope: str):
    try:
        # Try to Grab secret from AWS secrets manager
        from boto3 import client

        if _is_mode_materialization():
            aws_secret_client = client("secretsmanager")
        else:
            aws_secret_client = client("secretsmanager", region_name=get_or_none("CLUSTER_REGION"))
        secret = aws_secret_client.get_secret_value(SecretId=f"{scope}/{key}")
        return secret["SecretString"]
    except Exception:
        # Do not fail if secret is not found
        return None


def _get_from_db_secrets(key: str, scope: str):
    try:
        dbutils = _get_dbutils()
        return dbutils.secrets.get(scope, key)
    except Exception:
        return None


def save_okta_tokens(access_token, access_token_expiration, refresh_token=None):
    _set("OAUTH_ACCESS_TOKEN", access_token)
    _set("OAUTH_ACCESS_TOKEN_EXPIRATION", access_token_expiration)
    if refresh_token:
        _set("OAUTH_REFRESH_TOKEN", refresh_token)
    _save_tecton_config(_LOCAL_TECTON_TOKENS_FILE, _get_keys_with_allowed_source(ConfSource.LOCAL_TECTON_TOKENS))


def _read_json_config(file_path: Path) -> _ConfigSettings:
    """If the file exists, reads it and returns parsed JSON. Otherwise returns empty dictionary."""
    if not file_path.exists():
        return {}
    content = file_path.read_text()
    if not content:
        return {}
    try:
        return json.loads(content)
    except json.decoder.JSONDecodeError as e:
        raise ValueError(
            f"Unable to decode JSON configuration file {file_path} ({str(e)}). "
            + "To regenerate configuration, delete this file and run `tecton login`."
        )


def validate_api_service_url(url: str):
    """Validate Tecton API URL.
    Returns nothing for valid URLs or raises an error."""
    if "localhost" in url or "ingress" in url:
        return
    if not url.endswith("/api"):
        msg = f'Tecton API URL ("{url}") should be formatted "https://<deployment>.tecton.ai/api"'
        raise errors.TectonAPIValidationError(msg)


# Config values written to and read from the local .tecton/config file.
_LOCAL_TECTON_CONFIG: _ConfigSettings = {}

# Config values read from the local .tecton/config.tokens file.
_LOCAL_TECTON_TOKENS: _ConfigSettings = {}


def _init_configs():
    if not _is_mode_materialization():
        global _LOCAL_TECTON_CONFIG
        _LOCAL_TECTON_CONFIG = _read_json_config(_LOCAL_TECTON_CONFIG_FILE)

        global _LOCAL_TECTON_TOKENS
        _LOCAL_TECTON_TOKENS = _read_json_config(_LOCAL_TECTON_TOKENS_FILE)


def _init_metadata_server_config(mds_response):
    global _REMOTE_MDS_CONFIGS
    _REMOTE_MDS_CONFIGS = dict(mds_response.key_values)


_init_configs()
