from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Paciente(Base):
    __tablename__ = "paciente"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    medico_id: Mapped[int] = mapped_column(
        ForeignKey("medico.id"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    responsavel: Mapped[str] = mapped_column(String(150), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    medico = relationship("Medico")
    avaliacoes = relationship("Avaliacao", back_populates="paciente")
