# dbt · agent.md

## Propósito
Projeto dbt com o adaptador DuckDB. Expõe a bronze em SQL, com views do lote mais recente.

## Arquivos
- `dbt_project.yml` · materialização por pasta (bronze em view).
- `profiles.yml` · DuckDB em `$LAKEHOUSE/catalogo.duckdb`, com `../lakehouse` como padrão.
- `models/1_bronze/` · a source (todos os parquet da bronze, com `union_by_name`) e as views do lote mais recente.

## Padrões
- Todo modelo começa com um comentário de uma linha dizendo o que entrega.

## Pendências conhecidas
- Nenhuma.
