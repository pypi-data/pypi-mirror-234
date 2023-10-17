{% macro ocean_spark__concat(fields) -%}
    concat({{ fields|join(', ') }})
{%- endmacro %}
