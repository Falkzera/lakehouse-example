{# Funções de limpeza reaproveitadas pelos modelos da silver #}

{% macro limpar(col) -%}  {# trim, e toda forma de "vazio" vira nulo de verdade #}
  case when upper(trim({{ col }})) in ('', 'N/A', 'NA', 'NULL', 'NONE', '-') then null else trim({{ col }}) end
{%- endmacro %}

{% macro chave(col) -%}  {# forma canônica para comparar: sem acento e maiúscula #}
  upper(strip_accents({{ limpar(col) }}))
{%- endmacro %}

{% macro capitalizar(col) -%}  {# " ana SILVA " vira "Ana Silva" #}
  array_to_string(list_transform(string_split(lower({{ limpar(col) }}), ' '), lambda p: upper(p[1]) || p[2:]), ' ')
{%- endmacro %}

{% macro para_data(col) -%}  {# tenta cada formato conhecido; o que sobra (ex.: 31/02) vira nulo #}
  try_strptime({{ limpar(col) }}, ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y'])::date
{%- endmacro %}

{% macro para_valor(col) -%}  {# "R$ 1.234,56", "1234,56" e "1234.56" viram 1234.56 #}
  {%- set v = "trim(replace(" ~ limpar(col) ~ ", 'R$', ''))" -%}
  try_cast(case when {{ v }} like '%,%' then replace(replace({{ v }}, '.', ''), ',', '.') else {{ v }} end as decimal(12, 2))
{%- endmacro %}
