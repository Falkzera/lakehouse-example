-- Pedidos e receita por status, base da taxa de cancelamento
select
    status,
    count(*)                                                as pedidos,
    sum(receita)                                            as receita,
    round(100 * count(*) / sum(count(*)) over (), 1)        as pct
from {{ ref('fato_vendas') }}
group by status
order by pedidos desc
