-- Vendas tipadas, padronizadas e sem duplicata
select
    try_cast(v.id_venda as integer)                     as id_venda,
    {{ para_data('v.data_venda') }}                     as data_venda,
    {{ chave('v.id_cliente') }}                         as id_cliente,
    {{ capitalizar('v.produto') }}                      as produto,
    cat.categoria,
    try_cast({{ limpar('v.quantidade') }} as integer)   as quantidade,
    {{ para_valor('v.preco_unitario') }}                as preco_unitario,
    lower({{ chave('v.status') }})                      as status,
    v._lote,
    v._linha
from {{ ref('bronze_vendas') }} v
left join {{ ref('dominio_categoria') }} cat on cat.chave = {{ chave('v.categoria') }}
qualify row_number() over (partition by v.id_venda order by v._linha) = 1
