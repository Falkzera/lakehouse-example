"""Orquestra o pipeline medallion: landing -> bronze (Python) -> silver e gold (dbt)."""
import os
import sys

from dbt.cli.main import dbtRunner

import bronze
from config import DBT, GOLD, LAKEHOUSE, SILVER

if __name__ == "__main__":
    for pasta in (SILVER, GOLD):  # o dbt grava os parquet, mas não cria pasta
        pasta.mkdir(parents=True, exist_ok=True)
    bronze.executar()
    os.environ["LAKEHOUSE"] = str(LAKEHOUSE)
    if not dbtRunner().invoke(["build", "--project-dir", str(DBT), "--profiles-dir", str(DBT)]).success:
        sys.exit("[dbt] o build falhou, veja o erro ou o teste reprovado acima")
