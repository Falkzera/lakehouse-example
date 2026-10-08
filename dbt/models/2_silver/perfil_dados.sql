-- Perfil de cada coluna antes (bronze) e depois (silver) da limpeza
{{ perfilar('bronze', 'clientes', ref('bronze_clientes')) }}
union all
{{ perfilar('silver', 'clientes', ref('clientes')) }}
union all
{{ perfilar('bronze', 'vendas', ref('bronze_vendas')) }}
union all
{{ perfilar('silver', 'vendas', ref('vendas')) }}
