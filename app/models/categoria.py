from sqlalchemy import INTEGER, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

"""
metadata_obj = MetaData()
categoriasTable = Table(
    "Categorias",
    metadata_obj,
    Column("id", INTEGER, primary_key=True),
    Column("nome", VARCHAR(50), nullable=False, unique=True)
)
"""


class Categoria(Base):
    __tablename__  = "categorias"

    id: Mapped[INTEGER] = mapped_column(primary_key=True)
    nome: Mapped[VARCHAR] = mapped_column(VARCHAR(50), nullable=False, unique=True)