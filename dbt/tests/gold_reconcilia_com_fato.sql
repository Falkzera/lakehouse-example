-- Toda agregação tem que somar o mesmo que a fato: nenhuma venda paga some ou duplica no caminho
with totais as (
    select
        (select sum(receita) from {{ ref('fato_vendas') }} where status = 'pago') as fato,
        (select sum(receita) from {{ ref('receita_mensal') }})                     as mensal,
        (select sum(receita) from {{ ref('receita_categoria') }})                  as categoria,
        (select sum(receita) from {{ ref('receita_uf') }})                         as uf
)
-- is distinct from, e não !=, porque a soma de uma tabela vazia é nula e != com nulo nunca reprova
select * from totais
where mensal is distinct from fato or categoria is distinct from fato or uf is distinct from fato
