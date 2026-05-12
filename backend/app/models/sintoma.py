from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Sintoma(Base):
    __tablename__ = "sintoma"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(String(200), nullable=False)
    peso_m: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    peso_f: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
