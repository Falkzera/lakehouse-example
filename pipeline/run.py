"""Orquestra o pipeline medallion: landing -> bronze (Python) -> dbt."""
import os
import sys

from dbt.cli.main import dbtRunner

import bronze
from config import DBT, LAKEHOUSE

if __name__ == "__main__":
    bronze.executar()
    os.environ["LAKEHOUSE"] = str(LAKEHOUSE)
    if not dbtRunner().invoke(["build", "--project-dir", str(DBT), "--profiles-dir", str(DBT)]).success:
        sys.exit("[dbt] o build falhou, veja o erro ou o teste reprovado acima")
