-- A bronze guarda todas as cargas; a silver processa só a mais recente
select * from {{ source('bronze', 'clientes') }}
where _lote = (select max(_lote) from {{ source('bronze', 'clientes') }})
