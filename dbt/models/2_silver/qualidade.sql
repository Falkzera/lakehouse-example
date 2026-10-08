-- Placar da limpeza: o que entrou na bronze, o que chegou à silver e por que o resto ficou de fora
select 'clientes_bronze' as indicador, count(*) as linhas from {{ ref('bronze_clientes') }}
union all select 'clientes_silver', count(*) from {{ ref('clientes') }}
union all select 'vendas_bronze', count(*) from {{ ref('bronze_vendas') }}
union all select 'vendas_duplicadas', (select count(*) from {{ ref('bronze_vendas') }}) - count(*) from {{ ref('vendas_padronizadas') }}
union all select 'vendas_quarentena', count(*) from {{ ref('quarentena_vendas') }}
union all select 'vendas_silver', count(*) from {{ ref('vendas') }}
union all (
    select 'motivo_' || motivo, count(*)
    from (select unnest(string_split(motivo, ';')) as motivo from {{ ref('quarentena_vendas') }})
    group by motivo order by count(*) desc
)
