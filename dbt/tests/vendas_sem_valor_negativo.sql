-- Nenhuma venda da silver pode ter quantidade ou preço menor ou igual a zero
select * from {{ ref('vendas') }} where quantidade <= 0 or preco_unitario <= 0
