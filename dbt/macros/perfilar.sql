{# Uma linha por coluna da relação, com métricas exatas; ignora as colunas de controle (_lote, _linha...) #}
{% macro perfilar(camada, tabela, relacao) %}
  {%- set colunas = adapter.get_columns_in_relation(relacao) if execute else [] -%}
  {%- for col in colunas if not col.name.startswith('_') %}
  select
      '{{ camada }}' as camada, '{{ tabela }}' as tabela, '{{ col.name }}' as coluna, '{{ col.dtype }}' as tipo,
      min("{{ col.name }}")::varchar                                          as minimo,
      max("{{ col.name }}")::varchar                                          as maximo,
      count(distinct "{{ col.name }}")                                        as distintos,
      count(*)                                                                as linhas,
      round(100 * count(*) filter ("{{ col.name }}" is null) / count(*), 1)   as pct_nulos
  from {{ relacao }}
  {% if not loop.last %}union all{% endif %}
  {%- endfor %}
{% endmacro %}
