-- Uma linha por venda válida, com as chaves das dimensões e a receita calculada
select
    id_venda,
    data_venda,
    id_cliente,
    produto,
    status,
    quantidade,
    preco_unitario,
    quantidade * preco_unitario as receita
from {{ ref('vendas') }}
