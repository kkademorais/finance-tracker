from sqlalchemy import INTEGER, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

"""
cartoesTable = Table(
    "Cartoes",
    metadata_obj,
    Column("id", INTEGER, primary_key=True),
    Column("nome", VARCHAR(40), nullable=False, unique=True)
)
"""

class Cartao(Base):
    __tablename__ = "cartoes"

    id: Mapped[INTEGER] = mapped_column(primary_key=True)
    nome: Mapped[VARCHAR] = mapped_column(VARCHAR(40), nullable=False, unique=True)