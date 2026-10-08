-- Receita dos pedidos pagos por UF do cliente
select
    c.uf,
    count(*)                                                        as pedidos,
    sum(f.receita)                                                  as receita,
    round(100 * sum(f.receita) / sum(sum(f.receita)) over (), 1)    as participacao_pct
from {{ ref('fato_vendas') }} f
join {{ ref('dim_cliente') }} c using (id_cliente)
where f.status = 'pago'
group by c.uf
order by receita desc
