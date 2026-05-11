from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Avaliacao(Base):
    __tablename__ = "avaliacao"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"), nullable=False, index=True
    )
    medico_id: Mapped[int] = mapped_column(
        ForeignKey("medico.id"), nullable=False, index=True
    )
    data_avaliacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    score_total: Mapped[Decimal] = mapped_column(Numeric(6, 4), nullable=False)
    limiar: Mapped[Decimal] = mapped_column(Numeric(6, 4), nullable=False)
    recomendacao: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    paciente = relationship("Paciente", back_populates="avaliacoes")
    medico = relationship("Medico")
    sintomas = relationship(
        "AvaliacaoSintoma", back_populates="avaliacao", cascade="all, delete-orphan"
    )


class AvaliacaoSintoma(Base):
    __tablename__ = "avaliacao_sintoma"

    avaliacao_id: Mapped[int] = mapped_column(
        ForeignKey("avaliacao.id", ondelete="CASCADE"), primary_key=True
    )
    sintoma_id: Mapped[int] = mapped_column(ForeignKey("sintoma.id"), primary_key=True)
    presente: Mapped[int] = mapped_column(nullable=False)

    avaliacao = relationship("Avaliacao", back_populates="sintomas")
    sintoma = relationship("Sintoma")
