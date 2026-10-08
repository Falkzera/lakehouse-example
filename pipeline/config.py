"""Caminhos do projeto: as camadas do lakehouse."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
LAKEHOUSE = RAIZ / "lakehouse"
LANDING = LAKEHOUSE / "0_landing"
BRONZE = LAKEHOUSE / "1_bronze"
SILVER = LAKEHOUSE / "2_silver"
GOLD = LAKEHOUSE / "3_gold"
