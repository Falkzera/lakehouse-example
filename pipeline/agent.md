# pipeline · agent.md

## Propósito
A parte em Python do pipeline. Gera a fonte, grava a bronze e chama o dbt. Nenhuma regra de limpeza mora aqui; isso é do `dbt/`.

## Arquivos
- `config.py` · todos os caminhos do projeto. Mudou pasta, muda só aqui.
- `gerar_dados.py` · simula o sistema de origem. Semente fixa (42), então gera sempre os mesmos CSVs.
- `bronze.py` · lê cada CSV da landing como texto puro e grava um parquet por carga, com `_arquivo_origem`, `_lote` e `_linha`.
- `run.py` · orquestra. Cria as pastas, roda a bronze e chama `dbt build` pelo `dbtRunner`.

## Padrões
- Cada camada expõe uma função `executar()`.
- Os módulos importam os caminhos de `config.py` por nome, para o pytest poder trocar com `monkeypatch`.

## Decisões recentes
- 2026-10-08: silver e gold em SQL, no dbt, e não em pandas. Aqui fica só carga e exportação.
- 2026-10-08: o nome do lote ganhou microssegundos, porque duas cargas no mesmo segundo gravavam no mesmo arquivo.

## Pendências conhecidas
- Nenhuma.
