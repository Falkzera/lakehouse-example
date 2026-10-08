"""A bronze guarda o dado exatamente como chegou."""
import pandas as pd

import bronze


def test_bronze_guarda_texto_cru(tmp_path, monkeypatch):
    landing = tmp_path / "landing"
    landing.mkdir()
    (landing / "vendas.csv").write_text("id_venda;preco;status\n1;R$ 1.234,56; pago \n2;N/A;\n", encoding="utf-8")
    monkeypatch.setattr(bronze, "LANDING", landing)
    monkeypatch.setattr(bronze, "BRONZE", tmp_path / "bronze")
    monkeypatch.setattr(bronze, "RAIZ", tmp_path)

    bronze.executar()

    cargas = sorted((tmp_path / "bronze" / "vendas").glob("*.parquet"))
    assert len(cargas) == 1
    lote = pd.read_parquet(cargas[0])
    assert lote["preco"].tolist() == ["R$ 1.234,56", "N/A"]  # nada é convertido nem limpo
    assert lote["status"].tolist() == [" pago ", ""]
    assert lote["_linha"].tolist() == [2, 3]
    assert set(lote["_arquivo_origem"]) == {"vendas.csv"}
