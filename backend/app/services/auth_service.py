from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AuthenticationError
from app.models.medico import Medico
from app.models.session import Session


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        verify_password: Callable[[str, str], bool],
        generate_session_token: Callable[[], str],
        session_ttl_seconds: int,
    ) -> None:
        self.session = session
        self.verify_password = verify_password
        self.generate_session_token = generate_session_token
        self.session_ttl_seconds = session_ttl_seconds

    async def login(self, email: str, senha: str) -> dict[str, object]:
        medico = await self.session.scalar(select(Medico).where(Medico.email == email))
        if medico is None or not self.verify_password(senha, medico.senha_hash):
            raise AuthenticationError("Credenciais invalidas.")

        token = self.generate_session_token()
        expira_em = datetime.now(UTC) + timedelta(seconds=self.session_ttl_seconds)
        self.session.add(Session(medico_id=medico.id, token=token, expira_em=expira_em))
        await self.session.commit()
        return {"medico": medico, "session_token": token, "expira_em": expira_em}

    async def get_authenticated_medico(self, token: str | None) -> Medico:
        if not token:
            raise AuthenticationError("Sessao ausente.")

        statement = (
            select(Session)
            .options(selectinload(Session.medico))
            .where(Session.token == token)
        )
        session = await self.session.scalar(statement)
        if (
            session is None
            or session.revogada_em is not None
            or session.expira_em <= datetime.now(UTC).replace(tzinfo=None)
        ):
            raise AuthenticationError("Sessao invalida ou expirada.")
        if session.medico is None:
            raise AuthenticationError("Sessao sem medico associado.")
        return session.medico
