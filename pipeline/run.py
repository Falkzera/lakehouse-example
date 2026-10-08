"""Orquestra o pipeline medallion: landing -> bronze (Python) -> silver (dbt)."""
import os
import sys

from dbt.cli.main import dbtRunner

import bronze
from config import DBT, LAKEHOUSE, SILVER

if __name__ == "__main__":
    SILVER.mkdir(parents=True, exist_ok=True)  # o dbt grava os parquet, mas não cria pasta
    bronze.executar()
    os.environ["LAKEHOUSE"] = str(LAKEHOUSE)
    if not dbtRunner().invoke(["build", "--project-dir", str(DBT), "--profiles-dir", str(DBT)]).success:
        sys.exit("[dbt] o build falhou, veja o erro ou o teste reprovado acima")
