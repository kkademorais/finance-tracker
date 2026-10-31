from sqlalchemy import create_engine, MetaData, Table, Column,VARCHAR, INTEGER, NUMERIC, TIMESTAMP, ForeignKey

"""
from sqlalchemy import URL

url_object = URL.create(
    "postgresql+pg8000",
    username="dbuser",
    password="kx@jj5/g",  # plain (unescaped) text
    host="pghost10",
    database="appdb",
)

posgres: engine = create_engine("postgresql://scott:tiger@localhost/mydatabase")
mysql: engine = create_engine("mysql://scott:tiger@localhost/foo")

"""

#dialect+driver://username:password@host:port/database
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()
categoriasTable = Table(
    "Categorias",
    metadata_obj,
    Column("id", INTEGER, primary_key=True),
    Column("nome", VARCHAR(50), nullable=False, unique=True)
)
cartoesTable = Table(
    "Cartoes",
    metadata_obj,
    Column("id", INTEGER, primary_key=True),
    Column("nome", VARCHAR(40), nullable=False, unique=True)
)
comprasTable = Table(
    "Compras",
    metadata_obj,
    Column("id", INTEGER, primary_key=True),
    Column("valor", NUMERIC, nullable=False),
    Column("data_compra", TIMESTAMP, nullable=False),
    Column("estabelecimento", VARCHAR(50), nullable=False),
    Column("descricao", VARCHAR(100), nullable=True),
    Column("categoria_id", ForeignKey("categoriasTable.id"), nullable=False),
    Column("cartao_id", ForeignKey("cartoesTable.id"), nullable=False),
    Column("forma_pagamento", VARCHAR(15), nullable=True),
    Column("criado_em", TIMESTAMP)
)




with engine.connect() as conn:

    conn.commit()