"""Bronze: guarda cada CSV da landing exatamente como veio (tudo texto) + metadados de ingestão. Append-only."""
from datetime import datetime

import pandas as pd

from config import BRONZE, LANDING, RAIZ


def executar():
    lote = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # com microssegundos: duas cargas nunca caem no mesmo arquivo
    for csv in sorted(LANDING.glob("*.csv")):
        df = pd.read_csv(csv, sep=";", dtype=str, keep_default_na=False)  # nada é interpretado
        df["_arquivo_origem"], df["_lote"] = csv.name, lote
        df["_linha"] = df.index + 2  # linha no arquivo de origem (a 1 é o cabeçalho)
        destino = BRONZE / csv.stem / f"lote_{lote}.parquet"
        destino.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(destino, index=False)
        print(f"[bronze] {csv.name}: {len(df)} linhas -> {destino.relative_to(RAIZ)}")
