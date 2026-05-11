from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.paciente import Paciente
from app.schemas.common import Sexo


def calculate_age(birth_date: date, today: date | None = None) -> int:
    current_date = today or date.today()
    return (
        current_date.year
        - birth_date.year
        - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    )


class PacienteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, *, payload, medico_id: int) -> Paciente:
        sexo = payload.sexo.value if isinstance(payload.sexo, Sexo) else payload.sexo
        entity = Paciente(
            medico_id=medico_id,
            nome=payload.nome,
            data_nascimento=payload.data_nascimento,
            sexo=sexo,
            responsavel=payload.responsavel,
            observacoes=payload.observacoes,
        )
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def list(self, *, medico_id: int) -> list[Paciente]:
        statement = (
            select(Paciente)
            .where(Paciente.medico_id == medico_id)
            .order_by(Paciente.id)
        )
        result = await self.session.scalars(statement)
        return list(result)

    async def get_by_id(self, *, paciente_id: int, medico_id: int) -> Paciente:
        paciente = await self.session.scalar(
            select(Paciente).where(Paciente.id == paciente_id)
        )
        if paciente is None or paciente.medico_id != medico_id:
            raise NotFoundError("Paciente nao encontrado.")
        return paciente

    async def update(self, *, paciente_id: int, payload, medico_id: int) -> Paciente:
        paciente = await self.get_by_id(paciente_id=paciente_id, medico_id=medico_id)
        paciente.nome = payload.nome
        paciente.data_nascimento = payload.data_nascimento
        paciente.sexo = (
            payload.sexo.value if isinstance(payload.sexo, Sexo) else payload.sexo
        )
        paciente.responsavel = payload.responsavel
        paciente.observacoes = payload.observacoes
        await self.session.commit()
        await self.session.refresh(paciente)
        return paciente
