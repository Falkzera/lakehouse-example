# CLAUDE.md · lakehouse-example

## O que é

Lakehouse medallion local, de demonstração e público. CSVs sintéticos e sujos entram na landing, o Python grava a bronze (texto cru, um parquet por carga), o dbt com DuckDB transforma silver e gold em SQL, e o Python exporta os CSVs de consumo e o dashboard. Não há dado real nem segredo no repositório.

## Stack

| Peça | Versão (fixada em `requirements.txt`) |
|---|---|
| Python | 3.14 |
| pandas, pyarrow | 3.0.6, 25.0.1 |
| pytest | 9.1.1 |

## Comandos

```bash
python pipeline/gerar_dados.py              # fonte suja em lakehouse/0_landing
python pipeline/run.py                      # bronze
pytest                                      # testes do Python
```

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `pipeline/` | Python: geração da fonte, ingestão na bronze e orquestração |
| `tests/` | pytest |
| `lakehouse/` | dados gerados, fora do git |

## Regras

- Transformação só em SQL, no dbt. O Python carrega e exporta, nada mais.
- A bronze nunca sobrescreve.

## Documentação por pasta (agent.md)

`pipeline/` tem um `agent.md`, com o propósito da pasta, os arquivos e as decisões locais. Antes de mexer nela, leia o `agent.md`. Ao terminar uma mudança significativa (arquivo novo, regra nova, decisão de arquitetura), atualize-o. Pasta nova com código ganha o seu.
