from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    medico_id: Mapped[int] = mapped_column(
        ForeignKey("medico.id"), nullable=False, index=True
    )
    token: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revogada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    medico = relationship("Medico", back_populates="sessions")
