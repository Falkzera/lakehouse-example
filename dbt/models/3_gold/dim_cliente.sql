-- Dimensão cliente sem nome nem e-mail: a gold é a camada de consumo amplo (LGPD, minimização)
select id_cliente, coalesce(uf, 'N/I') as uf, data_cadastro
from {{ ref('clientes') }}
