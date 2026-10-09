-- Vendas tipadas e sem duplicata, cada uma com o motivo de reprovação (nulo quando passa em tudo)
{{ config(materialized='view') }}

with tipado as (
    select
        try_cast(v.id_venda as integer)                     as id_venda,
        {{ para_data('v.data_venda') }}                     as data_venda,
        {{ chave('v.id_cliente') }}                         as id_cliente,
        {{ capitalizar('v.produto') }}                      as produto,
        cat.categoria,
        try_cast({{ limpar('v.quantidade') }} as integer)   as quantidade,
        {{ para_valor('v.preco_unitario') }}                as preco_unitario,
        lower({{ chave('v.status') }})                      as status,
        cli.id_cliente is not null                          as cliente_existe,
        v._lote,
        v._linha
    from {{ ref('bronze_vendas') }} v
    left join {{ ref('dominio_categoria') }} cat on cat.chave = {{ chave('v.categoria') }}
    left join {{ ref('clientes') }} cli on cli.id_cliente = {{ chave('v.id_cliente') }}
    qualify row_number() over (partition by v.id_venda order by v._linha) = 1
)

select
    * exclude (cliente_existe),
    nullif(concat_ws(';',
        case when data_venda is null then 'data_invalida' end,
        case when quantidade is null or quantidade <= 0 then 'quantidade_invalida' end,
        case when preco_unitario is null or preco_unitario <= 0 then 'preco_invalido' end,
        case when preco_unitario > 5 * median(preco_unitario) over (partition by produto) then 'preco_outlier' end,
        case when produto is null then 'produto_invalido' end,
        case when categoria is null then 'categoria_invalida' end,
        case when not cliente_existe then 'cliente_inexistente' end,
        case when status is null or status not in ('pago', 'cancelado', 'pendente') then 'status_invalido' end
    ), '') as motivo
from tipado
