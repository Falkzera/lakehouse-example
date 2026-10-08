# CLAUDE.md · lakehouse-example

## O que é

Lakehouse medallion local, de demonstração e público. CSVs sintéticos e sujos entram na landing, o Python grava a bronze (texto cru, um parquet por carga), o dbt com DuckDB transforma silver e gold em SQL, e o Python exporta os CSVs de consumo e o dashboard. Não há dado real nem segredo no repositório.

## Stack

| Peça | Versão (fixada em `requirements.txt`) |
|---|---|
| Python | 3.14 |
| dbt-core e dbt-duckdb | 1.12.5 e 1.11.0 |
| DuckDB | 1.5.6 |
| pandas, pyarrow, matplotlib | 3.0.6, 25.0.1, 3.11.2 |
| pytest | 9.1.1 |

## Comandos

```bash
python pipeline/gerar_dados.py              # fonte suja em lakehouse/0_landing
python pipeline/run.py                      # bronze, dbt build (modelos e testes), resultados
pytest                                      # testes do Python
cd dbt && dbt build --profiles-dir .        # só o dbt; sem LAKEHOUSE definida, usa ../lakehouse
```

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `pipeline/` | Python: geração da fonte, ingestão na bronze, orquestração, exportação e dashboard |
| `dbt/` | SQL: views da bronze, modelos da silver e da gold, macros, seeds de domínio e testes |
| `tests/` | pytest |
| `resultados/` | saídas versionadas (CSVs, perfil, placar de qualidade, dashboard) |
| `lakehouse/` | dados gerados, fora do git |

## Regras

- Transformação só em SQL, no dbt. O Python carrega e exporta, nada mais.
- Função de limpeza nova vira macro em `dbt/macros/limpeza.sql` e ganha caso no teste unitário de `dbt/models/2_silver/_silver.yml`.
- A bronze nunca sobrescreve. A silver lê só o lote mais recente, pelas views de `dbt/models/1_bronze`.
- Dinheiro em `DECIMAL`. A gold não carrega nome nem e-mail.
- `resultados/` é versionado e tem que ser determinístico. Rodar o pipeline sem mudar regra não pode alterar nenhum arquivo dali.
- Git: trabalho em `feature/*` (ou `fix/*`, `docs/*`...) com PR e squash merge na `main`, que é protegida pelo check "Pipeline e testes". Conventional Commits.

## Gotchas

- `profiles.yml` cai em `../lakehouse` quando `LAKEHOUSE` não está definida. Rode o dbt de dentro de `dbt/` ou pelo `run.py`, que define o caminho absoluto.
- O dbt não cria pasta. O `run.py` cria `2_silver`, `3_gold` e `resultados` antes do build.
- `macros/external_location.sql` sobrescreve a macro do dbt-duckdb para gravar cada modelo na pasta da camada (`model.fqn[1]`).
- O `SUMMARIZE` do DuckDB é aproximado e muda entre execuções. O perfil usa a macro `perfilar`, que é exata.
- O DuckDB não tem `initcap`. Use a macro `capitalizar`.

## Documentação por pasta (agent.md)

`pipeline/` e `dbt/` têm um `agent.md` cada, com o propósito da pasta, os arquivos e as decisões locais. Antes de mexer numa delas, leia o `agent.md`. Ao terminar uma mudança significativa (arquivo novo, regra nova, decisão de arquitetura), atualize-o. Pasta nova com código ganha o seu.

## Pendências

- Lakehouse no S3, trocando só os caminhos de `pipeline/config.py` e do `profiles.yml`.
- Silver em PySpark no Databricks, gravando em Delta Lake.
