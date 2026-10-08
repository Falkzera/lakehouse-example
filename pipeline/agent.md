# pipeline · agent.md

## Propósito
A parte em Python do pipeline. Gera a fonte, grava a bronze, chama o dbt e exporta os resultados em CSV e dashboard. Nenhuma regra de limpeza mora aqui; isso é do `dbt/`.

## Arquivos
- `config.py` · todos os caminhos do projeto. Mudou pasta, muda só aqui.
- `gerar_dados.py` · simula o sistema de origem. Semente fixa (42), então gera sempre os mesmos CSVs.
- `bronze.py` · lê cada CSV da landing como texto puro e grava um parquet por carga, com `_arquivo_origem`, `_lote` e `_linha`.
- `run.py` · orquestra. Cria as pastas, roda a bronze, chama `dbt build` pelo `dbtRunner` e, se tudo passar, os resultados.
- `resultados.py` · lê com o DuckDB o perfil e o placar da silver e as agregações da gold, exporta CSV com `;`, vírgula decimal e BOM de UTF-8 e desenha `resultados/dashboard.png`.

## Padrões
- Cada camada expõe uma função `executar()`.
- Os módulos importam os caminhos de `config.py` por nome, para o pytest poder trocar com `monkeypatch`.

## Decisões recentes
- 2026-10-08: silver e gold em SQL, no dbt, e não em pandas. Aqui fica só carga e exportação.
- 2026-10-08: o nome do lote ganhou microssegundos, porque duas cargas no mesmo segundo gravavam no mesmo arquivo.
- 2026-10-08: CSV com BOM de UTF-8, porque sem ele o Excel no Windows lê o arquivo como ANSI e quebra os acentos.

## Pendências conhecidas
- Nenhuma.
