{# Grava cada modelo na pasta da sua camada, ex.: lakehouse/2_silver/vendas.parquet #}
{%- macro external_location(relation, config) -%}
  {{- adapter.external_root() }}/{{ model.fqn[1] }}/{{ relation.identifier }}.parquet
{%- endmacro -%}
