-- Dimensão produto, com a categoria já padronizada
select distinct produto, categoria from {{ ref('vendas') }}
