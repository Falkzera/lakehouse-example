"""Resultados: exporta as tabelas de consumo para CSV (padrão Excel pt-BR) e desenha o dashboard."""
import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import GOLD, RESULTADOS, SILVER

EXPORTAR = {SILVER: ["perfil_dados", "qualidade"],
            GOLD: ["receita_mensal", "receita_categoria", "receita_uf", "top_clientes", "status_pedidos"]}
COR, TINTA, TINTA_2, GRADE, FUNDO = "#2a78d6", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def brl(v):
    return f"R$ {v / 1e3:,.0f} mil".replace(",", ".")


def executar():
    t = {}
    for pasta, tabelas in EXPORTAR.items():
        for nome in tabelas:
            t[nome] = duckdb.read_parquet(str(pasta / f"{nome}.parquet")).df()  # decimal chega como float
            t[nome].to_csv(RESULTADOS / f"{nome}.csv", index=False, sep=";", decimal=",", encoding="utf-8-sig")
    print(f"[resultados] {len(t)} tabelas -> resultados/")
    dashboard(t)


def dashboard(t):
    plt.rcParams.update({"font.size": 10, "text.color": TINTA, "axes.edgecolor": GRADE, "axes.labelcolor": TINTA_2,
                         "xtick.color": TINTA_2, "ytick.color": TINTA_2, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titlelocation": "left", "axes.titleweight": "bold"})
    fig = plt.figure(figsize=(13, 9), facecolor=FUNDO)
    grid = fig.add_gridspec(2, 2, top=.80, height_ratios=[1, 1], hspace=.55, wspace=.3)
    fig.suptitle("Vendas · visão executiva (pedidos pagos)", x=.06, y=.97, ha="left", fontsize=15, fontweight="bold")

    m = t["receita_mensal"]
    receita, pedidos = m.receita.sum(), m.pedidos.sum()
    cancel = t["status_pedidos"].set_index("status").loc["cancelado", "pct"]
    kpis = [("Receita", f"R$ {receita / 1e6:.1f} mi".replace(".", ",")),
            ("Pedidos", f"{pedidos:,}".replace(",", ".")),
            ("Ticket médio", f"R$ {receita / pedidos:,.0f}".replace(",", ".")),
            ("Cancelamento", f"{cancel:.1f}%".replace(".", ","))]
    for i, (rotulo, valor) in enumerate(kpis):
        fig.text(.06 + i * .23, .91, rotulo, color=TINTA_2)
        fig.text(.06 + i * .23, .865, valor, fontsize=20, fontweight="bold")

    ax = fig.add_subplot(grid[0, :], facecolor=FUNDO)
    ax.plot(m.ano_mes, m.receita, color=COR, lw=2, marker="o", ms=4)
    ax.set_title("Receita mensal")
    ax.yaxis.set_major_formatter(lambda v, _: brl(v))
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", color=GRADE, lw=.8)

    for pos, nome, eixo, titulo in [(grid[1, 0], "receita_categoria", "categoria", "Receita por categoria"),
                                    (grid[1, 1], "receita_uf", "uf", "Receita por UF")]:
        d = t[nome].sort_values("receita")
        ax = fig.add_subplot(pos, facecolor=FUNDO)
        ax.barh(d[eixo], d.receita, color=COR, height=.6)
        ax.bar_label(ax.containers[0], labels=[brl(v) for v in d.receita], padding=4, color=TINTA_2, fontsize=9)
        ax.set_title(titulo)
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)

    fig.savefig(RESULTADOS / "dashboard.png", dpi=150, bbox_inches="tight", facecolor=FUNDO)
    print("[resultados] dashboard -> resultados/dashboard.png")
