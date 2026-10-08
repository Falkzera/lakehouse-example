-- Os 10 clientes que mais compraram em pedidos pagos, identificados só pelo código
select
    rank() over (order by sum(f.receita) desc)  as posicao,
    f.id_cliente,
    c.uf,
    count(*)                                    as pedidos,
    sum(f.receita)                              as receita
from {{ ref('fato_vendas') }} f
join {{ ref('dim_cliente') }} c using (id_cliente)
where f.status = 'pago'
group by f.id_cliente, c.uf
qualify posicao <= 10
order by posicao
