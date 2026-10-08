"""Orquestra o pipeline medallion: landing -> bronze (Python) -> silver e gold (dbt) -> resultados."""
import os
import sys

from dbt.cli.main import dbtRunner

import bronze
import resultados
from config import DBT, GOLD, LAKEHOUSE, RESULTADOS, SILVER

if __name__ == "__main__":
    for pasta in (SILVER, GOLD, RESULTADOS):  # o dbt e o resultados.py gravam aqui, mas não criam a pasta
        pasta.mkdir(parents=True, exist_ok=True)
    bronze.executar()
    os.environ["LAKEHOUSE"] = str(LAKEHOUSE)
    if not dbtRunner().invoke(["build", "--project-dir", str(DBT), "--profiles-dir", str(DBT)]).success:
        sys.exit("[dbt] o build falhou, veja o erro ou o teste reprovado acima")
    resultados.executar()
