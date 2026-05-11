from datetime import datetime
from decimal import Decimal

from app.schemas.common import BaseSchema, Recomendacao
from app.schemas.medico import MedicoResumo
from app.schemas.paciente import PacienteResumo
from app.schemas.sintoma import SintomaResponse


class CreateAvaliacaoSintomaRequest(BaseSchema):
    codigo: str
    presente: int


class CreateAvaliacaoRequest(BaseSchema):
    sintomas: list[CreateAvaliacaoSintomaRequest]
    observacoes: str | None = None


class AvaliacaoSintomaResponse(BaseSchema):
    sintoma: SintomaResponse
    presente: int


class AvaliacaoResponse(BaseSchema):
    id: int
    paciente: PacienteResumo
    medico: MedicoResumo
    data_avaliacao: datetime
    score_total: Decimal
    limiar: Decimal
    recomendacao: Recomendacao
    observacoes: str | None = None
    sintomas: list[AvaliacaoSintomaResponse]


class AvaliacaoResumo(BaseSchema):
    id: int
    paciente: PacienteResumo
    medico: MedicoResumo
    data_avaliacao: datetime
    score_total: Decimal
    limiar: Decimal
    recomendacao: Recomendacao

class RelatorioAvaliacaoResponse(BaseSchema):
    avaliacao_id: int
    paciente: PacienteResumo
    medico: MedicoResumo
    data_avaliacao: datetime
    score_total: Decimal
    limiar: Decimal
    recomendacao: Recomendacao
    mensagem_recomendacao: str
    observacoes: str | None = None
