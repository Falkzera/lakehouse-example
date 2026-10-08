-- Vendas reprovadas: guardadas com o motivo, nunca apagadas
select * from {{ ref('vendas_padronizadas') }} where motivo is not null
