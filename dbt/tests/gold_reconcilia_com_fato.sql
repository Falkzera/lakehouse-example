-- Toda agregação tem que somar o mesmo que a fato: nenhuma venda paga some ou duplica no caminho
with totais as (
    select
        (select sum(receita) from {{ ref('fato_vendas') }} where status = 'pago') as fato,
        (select sum(receita) from {{ ref('receita_mensal') }})                     as mensal,
        (select sum(receita) from {{ ref('receita_categoria') }})                  as categoria,
        (select sum(receita) from {{ ref('receita_uf') }})                         as uf
)
select * from totais where mensal != fato or categoria != fato or uf != fato
