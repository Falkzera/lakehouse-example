-- Receita dos pedidos pagos por mês, com a variação sobre o mês anterior e o acumulado
with mensal as (
    select c.ano_mes, count(*) as pedidos, sum(f.receita) as receita
    from {{ ref('fato_vendas') }} f
    join {{ ref('dim_calendario') }} c on c.data = f.data_venda
    where f.status = 'pago'
    group by c.ano_mes
)

select
    ano_mes,
    pedidos,
    receita,
    round(receita / pedidos, 2)                                     as ticket_medio,
    round(100 * (receita / lag(receita) over (order by ano_mes) - 1), 1) as variacao_pct,
    sum(receita) over (order by ano_mes)                            as receita_acumulada
from mensal
order by ano_mes
