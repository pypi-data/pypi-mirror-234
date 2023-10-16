{% from 'copier_macro.sql' import copy_into %}

{#
  This template uses Snowflake scripting features and needs to be run inside e.g. EXECUTE IMMEDIATE. The EXECUTE
  IMMEDIATE itself is not in the template so we can format the SQL before putting the whole thing into a string.

  This script materializes offline. It also optionally copies stuff online (if enabled). It does so by fetching offline rows matching some materialization_id.
#}

{# This starts a Snowflake scripting block and is unrelated to BEGIN TRANSACTION #}
BEGIN

{# create objects required for offline materialization if they do not currently exist #}
CREATE SCHEMA IF NOT EXISTS {{ workspace }};
CREATE TABLE IF NOT EXISTS {{ destination_table }}(
    {%- for column in materialization_schema.columns %}
    {{ column.name }} {{ tecton_type_to_snowflake_type(column.offline_data_type, column.name)}},
    {%- endfor %}
    __tecton_internal_materialization_id varchar
);
CREATE VIEW IF NOT EXISTS {{ destination_view }} AS (SELECT
    {%- for column in materialization_schema.columns %}
    {{ column.name }}{%- if not loop.last %}, {%- endif %}
    {%- endfor %}
FROM {{ destination_table }});

BEGIN TRANSACTION;

{# Insert into the snowflake table #}
{# Insert into is purely based on the order of the columns, not the name #}
{# So we have to do a select with the exact same order here. #}
INSERT INTO {{ destination_table }}(
    {%- for column in materialization_schema.columns %}
    {{ column.name }},
    {%- endfor %}
    __tecton_internal_materialization_id
)
WITH SOURCE AS ( {{  source }} )
SELECT
    {%- for column in materialization_schema.columns %}
    {{ column.name }},
    {%- endfor %}
    '{{ materialization_id }}' AS __tecton_internal_materialization_id
FROM SOURCE
;

{# copy inserted rows into the stage #}
{%- if materialize_online %}
    {% set copy_source %}
    SELECT *
    FROM {{ destination_table }}
    WHERE __tecton_internal_materialization_id = '{{ materialization_id }}'
    {% endset %}
    LET RES RESULTSET := (
        {{  copy_into(destination_stage, copy_source, materialization_schema, cast_types) }}
    );
{% else %}
LET RES RESULTSET := (select 0 "total_rows" ) ;
{% endif -%}
    COMMIT;
    RETURN TABLE(RES);
    END;
