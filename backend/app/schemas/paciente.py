from datetime import date, datetime

from pydantic import Field

from app.schemas.common import BaseSchema, Sexo


class CreatePacienteRequest(BaseSchema):
    nome: str = Field(min_length=1, max_length=150)
    data_nascimento: date
    sexo: Sexo
    responsavel: str = Field(min_length=1, max_length=150)
    observacoes: str | None = None


class UpdatePacienteRequest(CreatePacienteRequest):
    pass


class PacienteResponse(BaseSchema):
    id: int
    medico_id: int
    nome: str
    data_nascimento: date
    sexo: Sexo
    responsavel: str
    observacoes: str | None = None
    criado_em: datetime


class PacienteResumo(BaseSchema):
    id: int
    nome: str
    data_nascimento: date
    sexo: Sexo
    responsavel: str
