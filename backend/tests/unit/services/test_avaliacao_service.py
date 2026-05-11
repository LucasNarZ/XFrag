from datetime import UTC, date, datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest

from app.models.avaliacao import Avaliacao
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.models.sintoma import Sintoma
from app.core.exceptions import NotFoundError, ValidationError
from app.schemas.common import Sexo
from app.services import AvaliacaoService


class FakeScalarResult:
    def __init__(self, values):
        self.values = values

    def __iter__(self):
        return iter(self.values)


class FakeSession:
    def __init__(self, scalar_values=None, scalars_values=None):
        self.scalar_values = list(scalar_values or [])
        self.scalars_values = list(scalars_values or [])
        self.added = []

    async def scalar(self, _statement):
        if not self.scalar_values:
            return None
        return self.scalar_values.pop(0)

    async def scalars(self, _statement):
        if not self.scalars_values:
            return FakeScalarResult([])
        return FakeScalarResult(self.scalars_values.pop(0))

    def add(self, entity) -> None:
        self.added.append(entity)

    async def commit(self) -> None:
        return None

    async def refresh(self, entity) -> None:
        entity.id = 100
        entity.data_avaliacao = datetime.now(UTC)


def build_paciente(medico_id: int = 1, sexo: str = Sexo.M.value) -> Paciente:
    return Paciente(
        id=10,
        medico_id=medico_id,
        nome="Joao",
        sexo=sexo,
        data_nascimento=date(2018, 4, 10),
        responsavel="Ana",
    )


def build_sintoma(
    sintoma_id: int,
    codigo: str,
    peso_m: str,
    peso_f: str | None,
) -> Sintoma:
    return Sintoma(
        id=sintoma_id,
        codigo=codigo,
        descricao=codigo,
        peso_m=Decimal(peso_m),
        peso_f=None if peso_f is None else Decimal(peso_f),
    )


def build_avaliacao(medico_id: int = 1) -> Avaliacao:
    avaliacao = Avaliacao(
        id=100,
        paciente_id=10,
        medico_id=medico_id,
        data_avaliacao=datetime.now(UTC),
        score_total=Decimal("0.5600"),
        limiar=Decimal("0.5600"),
        recomendacao="ENCAMINHAR",
    )
    avaliacao.paciente = build_paciente(medico_id=medico_id)
    avaliacao.medico = Medico(
        id=medico_id,
        nome="Medica",
        crm="CRM-1",
        especialidade="Genetica",
        email="medica@email.com",
        senha_hash="hash",
    )
    return avaliacao


@pytest.mark.asyncio
async def test_create_calculates_male_score_and_recommendation() -> None:
    paciente = build_paciente()
    sintomas = [
        build_sintoma(1, "DEFICIENCIA_INTELECTUAL", "0.3200", "0.2000"),
        build_sintoma(2, "FACE_ALONGADA_ORELHAS", "0.2900", "0.0900"),
        *[
            build_sintoma(index + 3, f"IGNORADO_{index}", "0.0000", "0.0000")
            for index in range(10)
        ],
    ]
    payload = SimpleNamespace(
        sintomas=[
            SimpleNamespace(codigo="DEFICIENCIA_INTELECTUAL", presente=1),
            SimpleNamespace(codigo="FACE_ALONGADA_ORELHAS", presente=1),
            *[
                SimpleNamespace(codigo=f"IGNORADO_{index}", presente=0)
                for index in range(10)
            ],
        ],
        observacoes="obs",
    )
    service = AvaliacaoService(
        FakeSession(scalar_values=[paciente], scalars_values=[sintomas])
    )

    created = await service.create(payload=payload, paciente_id=10, medico_id=1)

    assert created.score_total == Decimal("0.6100")
    assert created.limiar == Decimal("0.5600")
    assert created.recomendacao == "ENCAMINHAR"
    assert len(created.sintomas) == 12


@pytest.mark.asyncio
async def test_calculate_result_uses_zero_when_female_weight_is_null() -> None:
    service = AvaliacaoService(FakeSession())
    sintomas = {
        "A": build_sintoma(1, "A", "0.2600", None),
        "B": build_sintoma(2, "B", "0.2900", "0.5500"),
    }
    enviados = [
        SimpleNamespace(codigo="A", presente=1),
        SimpleNamespace(codigo="B", presente=1),
    ]

    score_total, limiar, recomendacao, itens = service.calculate_result(
        Sexo.F.value, enviados, sintomas
    )

    assert score_total == Decimal("0.5500")
    assert limiar == Decimal("0.5500")
    assert recomendacao == "ENCAMINHAR"
    assert itens[0]["presente"] == 1


@pytest.mark.asyncio
async def test_create_raises_when_patient_belongs_to_another_medico() -> None:
    paciente = build_paciente(medico_id=99)
    payload = SimpleNamespace(
        sintomas=[
            SimpleNamespace(codigo=f"S{index}", presente=0) for index in range(12)
        ],
        observacoes=None,
    )
    sintomas = [
        build_sintoma(index, f"S{index}", "0.0000", "0.0000") for index in range(12)
    ]
    service = AvaliacaoService(
        FakeSession(scalar_values=[paciente], scalars_values=[sintomas])
    )

    with pytest.raises(NotFoundError):
        await service.create(payload=payload, paciente_id=10, medico_id=1)


@pytest.mark.asyncio
async def test_create_raises_when_presente_is_not_zero_or_one() -> None:
    paciente = build_paciente()
    payload = SimpleNamespace(
        sintomas=[
            SimpleNamespace(codigo="S0", presente=2),
            *[
                SimpleNamespace(codigo=f"S{index}", presente=0)
                for index in range(1, 12)
            ],
        ],
        observacoes=None,
    )
    sintomas = [
        build_sintoma(index, f"S{index}", "0.0000", "0.0000") for index in range(12)
    ]
    service = AvaliacaoService(
        FakeSession(scalar_values=[paciente], scalars_values=[sintomas])
    )

    with pytest.raises(ValidationError):
        await service.create(payload=payload, paciente_id=10, medico_id=1)


@pytest.mark.asyncio
async def test_get_by_id_raises_when_avaliacao_belongs_to_another_medico() -> None:
    service = AvaliacaoService(
        FakeSession(scalar_values=[build_avaliacao(medico_id=99)])
    )

    with pytest.raises(NotFoundError):
        await service.get_by_id(avaliacao_id=100, medico_id=1)


@pytest.mark.asyncio
async def test_list_scopes_results_to_authenticated_medico() -> None:
    service = AvaliacaoService(
        FakeSession(scalars_values=[[build_avaliacao(medico_id=7)]])
    )

    result = await service.list(medico_id=7)

    assert len(result) == 1
    assert result[0].medico_id == 7
