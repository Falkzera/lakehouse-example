# dbt · agent.md

## Propósito
Projeto dbt com o adaptador DuckDB. Transforma a bronze em silver, em SQL, e testa tudo. Os modelos da silver são `external`: viram parquet em `lakehouse/2_silver`, e o `lakehouse/catalogo.duckdb` guarda views que apontam para eles.

## Arquivos
- `dbt_project.yml` · materialização por pasta (bronze em view, silver em parquet).
- `profiles.yml` · DuckDB em `$LAKEHOUSE/catalogo.duckdb`, com `../lakehouse` como padrão.
- `models/1_bronze/` · a source (todos os parquet da bronze, com `union_by_name`) e as views do lote mais recente.
- `models/2_silver/` · `clientes`, `vendas_padronizadas` (view com o motivo de reprovação), `vendas`, `quarentena_vendas`, `perfil_dados`, `qualidade`. Os testes unitários e de dados ficam em `_silver.yml`.
- `macros/limpeza.sql` · `limpar`, `chave`, `capitalizar`, `para_data`, `para_valor`.
- `macros/perfilar.sql` · perfil exato de cada coluna de uma relação.
- `macros/external_location.sql` · grava cada modelo na pasta da sua camada.
- `seeds/` · domínios válidos de UF e de categoria.
- `tests/` · testes SQL próprios (valores positivos na silver).

## Padrões
- Todo modelo começa com um comentário de uma linha dizendo o que entrega.
- Regra de qualidade nova entra no `concat_ws` de `vendas_padronizadas.sql` e ganha linha no teste unitário `regras_de_qualidade_apontam_cada_motivo`.

## Decisões recentes
- 2026-10-08: views da bronze, e não uma macro de "último lote", para os testes unitários terem a origem tipada e o grafo de linhagem mostrar a bronze.
- 2026-10-08: perfil por macro própria, e não pelo `SUMMARIZE`, que é aproximado na contagem de distintos e muda a cada execução.

## Pendências conhecidas
- Nenhuma.
