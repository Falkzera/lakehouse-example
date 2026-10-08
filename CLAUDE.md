# CLAUDE.md · lakehouse-example

## O que é

Lakehouse medallion local, de demonstração e público. CSVs sintéticos e sujos entram na landing, o Python grava a bronze (texto cru, um parquet por carga), o dbt com DuckDB transforma silver e gold em SQL, e o Python exporta os CSVs de consumo e o dashboard. Não há dado real nem segredo no repositório.

## Stack

| Peça | Versão (fixada em `requirements.txt`) |
|---|---|
| Python | 3.14 |
| dbt-core e dbt-duckdb | 1.12.5 e 1.11.0 |
| DuckDB | 1.5.6 |
| pandas, pyarrow | 3.0.6, 25.0.1 |
| pytest | 9.1.1 |

## Comandos

```bash
python pipeline/gerar_dados.py              # fonte suja em lakehouse/0_landing
python pipeline/run.py                      # bronze e dbt build
pytest                                      # testes do Python
cd dbt && dbt build --profiles-dir .        # só o dbt; sem LAKEHOUSE definida, usa ../lakehouse
```

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `pipeline/` | Python: geração da fonte, ingestão na bronze e orquestração |
| `dbt/` | SQL: views da bronze |
| `tests/` | pytest |
| `lakehouse/` | dados gerados, fora do git |

## Regras

- Transformação só em SQL, no dbt. O Python carrega e exporta, nada mais.
- A bronze nunca sobrescreve.

## Gotchas

- `profiles.yml` cai em `../lakehouse` quando `LAKEHOUSE` não está definida. Rode o dbt de dentro de `dbt/` ou pelo `run.py`, que define o caminho absoluto.

## Documentação por pasta (agent.md)

`pipeline/` e `dbt/` têm um `agent.md` cada, com o propósito da pasta, os arquivos e as decisões locais. Antes de mexer numa delas, leia o `agent.md`. Ao terminar uma mudança significativa (arquivo novo, regra nova, decisão de arquitetura), atualize-o. Pasta nova com código ganha o seu.
