from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.common import BaseSchema


class CreateMedicoRequest(BaseSchema):
    nome: str = Field(min_length=1, max_length=150)
    crm: str = Field(min_length=1, max_length=20)
    especialidade: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8)


class MedicoResponse(BaseSchema):
    id: int
    nome: str
    crm: str
    especialidade: str
    email: EmailStr
    criado_em: datetime


class MedicoResumo(BaseSchema):
    id: int
    nome: str
    crm: str
    especialidade: str | None = None
