"""Simula o sistema de origem: gera CSVs de clientes e vendas propositalmente poluídos na landing."""
import random
import unicodedata
from datetime import date, timedelta

import pandas as pd

from config import LANDING

random.seed(42)

UFS = {"SP": "São Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais", "AL": "Alagoas", "BA": "Bahia", "PE": "Pernambuco"}
PRODUTOS = {"Notebook": ("Eletrônicos", 3500), "Celular": ("Eletrônicos", 1800), "Fone": ("Eletrônicos", 150),
            "Cadeira": ("Móveis", 600), "Mesa": ("Móveis", 900), "Camiseta": ("Vestuário", 60),
            "Tênis": ("Vestuário", 300), "Livro": ("Livros", 50)}
NOMES = ["Ana", "João", "Maria", "Pedro", "Lucas", "Júlia", "Carla", "José", "Bruna", "Rafael"]
SOBRENOMES = ["Silva", "Souza", "Oliveira", "Lima", "Falcão", "Costa", "Pereira", "Araújo"]
NULOS = ["", "N/A", "null", "-", "NULL"]


def chance(p):
    return random.random() < p


def sem_acento(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def texto(s):  # mesma informação, digitada de jeitos diferentes
    return random.choice([s, s.upper(), s.lower(), f" {s} ", f"{s}  "])


def data(d):  # cada sistema exporta a data num formato
    return d.strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"]))


def preco(v):  # 1234.56 | 1234,56 | R$ 1.234,56 | 1235
    br = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return random.choice([f"{v:.2f}", f"{v:.2f}".replace(".", ","), f"R$ {br}", str(round(v))])


clientes = []
for i in range(1, 301):
    uf, nome = random.choice(list(UFS)), f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"
    email = sem_acento(nome).lower().replace(" ", ".") + str(i) + ("@email.com" if not chance(.05) else "email.com")
    clientes.append({
        "id_cliente": f"C{i:04d}" if not chance(.05) else f" c{i:04d}",
        "nome": texto(nome),
        "email": random.choice(NULOS) if chance(.08) else email,
        "uf": random.choice(NULOS) if chance(.04) else random.choice([uf, uf.lower(), f" {uf}", UFS[uf], sem_acento(UFS[uf])]),
        "data_cadastro": data(date(2023, 1, 1) + timedelta(days=random.randint(0, 700))),
    })
clientes += random.sample(clientes, 15)  # registros duplicados

vendas = []
for i in range(1, 5001):
    prod = random.choice(list(PRODUTOS))
    cat, valor = PRODUTOS[prod]
    valor *= random.uniform(.85, 1.15) * (100 if chance(.005) else 1)  # 0,5% com erro de digitação
    vendas.append({
        "id_venda": i,
        "data_venda": random.choice(NULOS + ["31/02/2025"]) if chance(.02)
        else data(date(2025, 1, 1) + timedelta(days=random.randint(0, 637))),
        "id_cliente": f"C{random.randint(1, 310):04d}",  # >300 = cliente que não existe no cadastro
        "produto": texto(prod),
        "categoria": random.choice([cat, cat.upper(), sem_acento(cat).lower()]),
        "quantidade": random.choice(["0", "-1", "dois", ""]) if chance(.03) else str(random.randint(1, 5)),
        "preco_unitario": random.choice(NULOS) if chance(.02) else preco(valor),
        "status": texto(random.choices(["pago", "cancelado", "pendente"], [.8, .12, .08])[0]),
    })
vendas += random.sample(vendas, 120)
random.shuffle(vendas)

LANDING.mkdir(parents=True, exist_ok=True)
for nome, linhas in {"clientes": clientes, "vendas": vendas}.items():
    pd.DataFrame(linhas).to_csv(LANDING / f"{nome}.csv", sep=";", index=False)
    print(f"[fonte] {nome}.csv: {len(linhas)} linhas")
