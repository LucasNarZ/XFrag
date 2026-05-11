from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError, ValidationError
from app.models.avaliacao import Avaliacao, AvaliacaoSintoma
from app.models.paciente import Paciente
from app.models.sintoma import Sintoma

MALE_THRESHOLD = Decimal("0.5600")
FEMALE_THRESHOLD = Decimal("0.5500")


class AvaliacaoService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def calculate_result(
        self, sexo: str, enviados, sintomas_por_codigo: dict[str, object]
    ):
        score_total = Decimal("0.0000")
        itens = []

        for item in enviados:
            if item.presente not in {0, 1}:
                raise ValidationError(
                    "Cada sintoma deve informar presente como 0 ou 1."
                )
            sintoma = sintomas_por_codigo[item.codigo]
            peso = sintoma.peso_m if sexo == "M" else (sintoma.peso_f or Decimal("0"))
            if item.presente == 1:
                score_total += Decimal(peso)
            itens.append({"sintoma_id": sintoma.id, "presente": item.presente})

        limiar = MALE_THRESHOLD if sexo == "M" else FEMALE_THRESHOLD
        recomendacao = "ENCAMINHAR" if score_total >= limiar else "NAO_ENCAMINHAR"
        return score_total.quantize(Decimal("0.0001")), limiar, recomendacao, itens

    async def create(self, *, payload, paciente_id: int, medico_id: int):
        if len(payload.sintomas) != 12:
            raise ValidationError("A avaliacao deve conter os 12 sintomas.")

        codigos = [item.codigo for item in payload.sintomas]
        if len(set(codigos)) != len(codigos):
            raise ValidationError("A avaliacao nao pode conter sintomas duplicados.")

        paciente = await self.session.scalar(
            select(Paciente).where(Paciente.id == paciente_id)
        )
        if paciente is None or paciente.medico_id != medico_id:
            raise NotFoundError("Paciente nao encontrado.")

        sintomas = await self.session.scalars(
            select(Sintoma).where(Sintoma.codigo.in_(codigos))
        )
        sintomas_por_codigo = {sintoma.codigo: sintoma for sintoma in sintomas}
        if len(sintomas_por_codigo) != 12:
            raise ValidationError("Checklist invalido: sintomas inexistentes.")

        score_total, limiar, recomendacao, itens = self.calculate_result(
            paciente.sexo,
            payload.sintomas,
            sintomas_por_codigo,
        )
        avaliacao = Avaliacao(
            paciente_id=paciente_id,
            medico_id=medico_id,
            score_total=score_total,
            limiar=limiar,
            recomendacao=recomendacao,
            observacoes=payload.observacoes,
        )
        avaliacao.sintomas = [AvaliacaoSintoma(**payload) for payload in itens]
        self.session.add(avaliacao)
        await self.session.commit()
        await self.session.refresh(avaliacao)
        return avaliacao

    async def get_by_id(self, avaliacao_id: int, medico_id: int) -> Avaliacao:
        statement = (
            select(Avaliacao)
            .options(
                selectinload(Avaliacao.paciente),
                selectinload(Avaliacao.medico),
                selectinload(Avaliacao.sintomas).selectinload(AvaliacaoSintoma.sintoma),
            )
            .where(Avaliacao.id == avaliacao_id)
        )
        avaliacao = await self.session.scalar(statement)
        if avaliacao is None or avaliacao.medico_id != medico_id:
            raise NotFoundError("Avaliacao nao encontrada.")
        return avaliacao

    async def list_by_paciente_id(
        self, paciente_id: int, medico_id: int
    ) -> list[Avaliacao]:
        paciente = await self.session.scalar(
            select(Paciente).where(Paciente.id == paciente_id)
        )
        if paciente is None or paciente.medico_id != medico_id:
            raise NotFoundError("Paciente nao encontrado.")
        statement = (
            select(Avaliacao)
            .options(selectinload(Avaliacao.paciente), selectinload(Avaliacao.medico))
            .where(Avaliacao.paciente_id == paciente_id)
            .order_by(Avaliacao.id)
        )
        result = await self.session.scalars(statement)
        return list(result)

    async def list(self, medico_id: int) -> list[Avaliacao]:
        statement = (
            select(Avaliacao)
            .options(selectinload(Avaliacao.paciente), selectinload(Avaliacao.medico))
            .where(Avaliacao.medico_id == medico_id)
            .order_by(Avaliacao.id)
        )
        result = await self.session.scalars(statement)
        return list(result)
