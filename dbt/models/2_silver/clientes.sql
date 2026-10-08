-- Um registro por cliente: texto padronizado, UF como sigla e e-mail inválido virando nulo
select
    {{ chave('c.id_cliente') }}          as id_cliente,
    {{ capitalizar('c.nome') }}          as nome,
    case when regexp_matches({{ limpar('c.email') }}, '^[^@\s]+@[^@\s]+\.\w+$')
         then lower({{ limpar('c.email') }}) end as email,
    uf.uf,
    {{ para_data('c.data_cadastro') }}   as data_cadastro
from {{ ref('bronze_clientes') }} c
left join {{ ref('dominio_uf') }} uf on uf.chave = {{ chave('c.uf') }}
qualify row_number() over (partition by {{ chave('c.id_cliente') }} order by c._linha) = 1
