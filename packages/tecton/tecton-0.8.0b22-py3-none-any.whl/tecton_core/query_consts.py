from tecton_core.query.sql_compat import default_case


ANCHOR_TIME = default_case("_anchor_time")
EFFECTIVE_TIMESTAMP = default_case("_effective_timestamp")
EXPIRATION_TIMESTAMP = default_case("_expiration_timestamp")
TIMESTAMP_PLUS_TTL = default_case("_timestamp_plus_ttl")
TECTON_SECONDARY_KEY_AGGREGATION_INDICATOR_COL = default_case("_tecton_secondary_key_aggregation_indicator")
TECTON_UNIQUE_ID_COL = default_case("_tecton_unique_id")

# Namespace used in `FeatureDefinitionAndJoinConfig` for dependent feature view
# columns. Dependent FVs to ODFVs have this prefix in the name and are
# filtered out before being returned to the user.
UDF_INTERNAL = default_case("_udf_internal")
ODFV_INTERNAL_STAGING_TABLE = default_case("_odfv_internal_table")

AGGREGATION_GROUP_ID = default_case("_tecton_aggregation_window_id")
INCLUSIVE_START_TIME = default_case("_tecton_inclusive_start_time")
EXCLUSIVE_END_TIME = default_case("_tecton_exclusive_end_time")
