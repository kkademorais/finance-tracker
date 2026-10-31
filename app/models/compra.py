from sqlalchemy import INTEGER, NUMERIC, TIMESTAMP, VARCHAR, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

"""
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
"""

class Compra(Base):
    __tablename__ = "compras"

    id: Mapped[INTEGER] = mapped_column(primary_key=True)
    valor: Mapped[NUMERIC] = mapped_column(NUMERIC, nullable=False) 
    data_compra: Mapped[TIMESTAMP] = mapped_column("data_compra", TIMESTAMP, nullable=False)
    estabelecimento: Mapped[VARCHAR] = mapped_column("estabelecimento", VARCHAR(50), nullable=False)
    descricao: Mapped[VARCHAR] = mapped_column("descricao", VARCHAR(100), nullable=True)
    categoria_id: Mapped[INTEGER] = mapped_column("categoria_id", ForeignKey("categoriasTable.id"), nullable=False)
    cartao_id: Mapped[INTEGER] = mapped_column("cartao_id", ForeignKey("cartoesTable.id"), nullable=False)
    forma_pagamemto: Mapped[INTEGER] = mapped_column("forma_pagamento", VARCHAR(15), nullable=True)
    criado_em: Mapped[TIMESTAMP] = mapped_column("criado_em", TIMESTAMP, nullable=True)