from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.medico import Medico


class MedicoService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        nome: str,
        crm: str,
        especialidade: str,
        email: str,
        senha: str,
    ) -> Medico:
        if await self.session.scalar(select(Medico).where(Medico.email == email)):
            raise ConflictError("E-mail ja cadastrado.")
        if await self.session.scalar(select(Medico).where(Medico.crm == crm)):
            raise ConflictError("CRM ja cadastrado.")

        entity = Medico(
            nome=nome,
            crm=crm,
            especialidade=especialidade,
            email=email,
            senha_hash=hash_password(senha),
        )
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def list(self) -> list[Medico]:
        result = await self.session.scalars(select(Medico).order_by(Medico.id))
        return list(result)

    async def get_by_id(self, medico_id: int) -> Medico:
        medico = await self.session.scalar(select(Medico).where(Medico.id == medico_id))
        if medico is None:
            raise NotFoundError("Medico nao encontrado.")
        return medico
