from datetime import date
from types import SimpleNamespace

import pytest

from app.models.paciente import Paciente
from app.schemas.common import Sexo
from app.services import PacienteService, calculate_age


def test_calculate_age_returns_integer_for_birth_date() -> None:
    result = calculate_age(date(2018, 4, 10), today=date(2026, 5, 5))

    assert result == 8


class FakeSession:
    def __init__(self) -> None:
        self.added = []

    def add(self, entity) -> None:
        self.added.append(entity)

    async def commit(self) -> None:
        return None

    async def refresh(self, entity) -> None:
        entity.id = 1
        entity.criado_em = None


@pytest.mark.asyncio
async def test_create_assigns_authenticated_medico_id() -> None:
    session = FakeSession()
    service = PacienteService(session)
    payload = SimpleNamespace(
        nome="Joao Silva",
        data_nascimento=date(2018, 4, 10),
        sexo=Sexo.M,
        responsavel="Ana Silva",
        observacoes="Paciente acompanhado.",
    )

    paciente = await service.create(payload=payload, medico_id=7)

    assert isinstance(paciente, Paciente)
    assert paciente.medico_id == 7
    assert paciente.nome == "Joao Silva"
