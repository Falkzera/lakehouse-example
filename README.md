# Lakehouse medallion local

Pipeline de dados que recebe CSVs sujos e entrega tabelas confiáveis e um dashboard, passando pelas camadas bronze, silver e gold. Python carrega, o dbt transforma em SQL dentro do DuckDB, e cada passo tem teste.
