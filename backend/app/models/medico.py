from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Role(str, Enum):
    ADMIN = "ADMIN"
    MEDICO = "MEDICO"


class Medico(Base):
    __tablename__ = "medico"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    crm: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    especialidade: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(
        SqlEnum(Role), default=Role.MEDICO, nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    sessions = relationship("Session", back_populates="medico")
