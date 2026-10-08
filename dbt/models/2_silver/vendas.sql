-- Vendas que passaram em todas as regras de qualidade
select * exclude (motivo) from {{ ref('vendas_padronizadas') }} where motivo is null
