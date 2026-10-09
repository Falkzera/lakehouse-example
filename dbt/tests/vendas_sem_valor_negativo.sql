-- Nenhuma venda da silver pode ter quantidade ou preço menor ou igual a zero
-- <= com nulo dá nulo e não reprova, por isso as duas colunas também têm not_null em _silver.yml
select * from {{ ref('vendas') }} where quantidade <= 0 or preco_unitario <= 0
