from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.sintoma import Sintoma


class SintomaService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> list[Sintoma]:
        result = await self.session.scalars(select(Sintoma).order_by(Sintoma.id))
        return list(result)

    async def get_by_id(self, sintoma_id: int) -> Sintoma:
        sintoma = await self.session.scalar(
            select(Sintoma).where(Sintoma.id == sintoma_id)
        )
        if sintoma is None:
            raise NotFoundError("Sintoma nao encontrado.")
        return sintoma
