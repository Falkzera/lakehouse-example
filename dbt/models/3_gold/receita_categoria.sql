-- Receita dos pedidos pagos por categoria, com a participação no total
select
    p.categoria,
    count(*)                                                        as pedidos,
    sum(f.quantidade)                                               as unidades,
    sum(f.receita)                                                  as receita,
    round(100 * sum(f.receita) / sum(sum(f.receita)) over (), 1)    as participacao_pct
from {{ ref('fato_vendas') }} f
join {{ ref('dim_produto') }} p using (produto)
where f.status = 'pago'
group by p.categoria
order by receita desc
