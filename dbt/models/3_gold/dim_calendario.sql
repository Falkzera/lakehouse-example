-- Um dia por linha, do primeiro ao último dia com venda
select
    dia::date               as data,
    year(dia)               as ano,
    month(dia)              as mes,
    strftime(dia, '%Y-%m')  as ano_mes,
    quarter(dia)            as trimestre,
    isodow(dia) <= 5        as dia_util
from generate_series(
    (select min(data_venda) from {{ ref('vendas') }}),
    (select max(data_venda) from {{ ref('vendas') }}),
    interval 1 day
) as t(dia)
