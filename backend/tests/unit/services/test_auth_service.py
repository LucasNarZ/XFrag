from datetime import UTC, datetime, timedelta

import pytest

from app.core.exceptions import AuthenticationError
from app.models.medico import Medico
from app.models.session import Session
from app.services import AuthService


class FakeSession:
    def __init__(self, scalar_values=None):
        self.scalar_values = list(scalar_values or [])
        self.added = []

    async def scalar(self, _statement):
        if not self.scalar_values:
            return None
        return self.scalar_values.pop(0)

    def add(self, entity) -> None:
        self.added.append(entity)

    async def commit(self) -> None:
        return None


def build_medico(**overrides) -> Medico:
    return Medico(
        id=overrides.get("id", 1),
        nome=overrides.get("nome", "Maria Oliveira"),
        crm=overrides.get("crm", "CRM-PR-123456"),
        especialidade=overrides.get("especialidade", "Geneticista"),
        email=overrides.get("email", "maria@email.com"),
        senha_hash=overrides.get("senha_hash", "hashed"),
        criado_em=overrides.get("criado_em", datetime.now(UTC)),
    )


@pytest.mark.asyncio
async def test_login_returns_medico_and_creates_session() -> None:
    medico = build_medico()
    session = FakeSession(scalar_values=[medico])

    service = AuthService(
        session=session,
        verify_password=lambda plain, hashed: (
            plain == "SenhaForte123" and hashed == "hashed"
        ),
        generate_session_token=lambda: "token-fixo",
        session_ttl_seconds=3600,
    )

    result = await service.login(email="maria@email.com", senha="SenhaForte123")

    assert result["medico"].id == 1
    assert result["session_token"] == "token-fixo"
    assert len(session.added) == 1
    assert isinstance(session.added[0], Session)
    assert session.added[0].medico_id == 1


@pytest.mark.asyncio
async def test_login_raises_for_invalid_password() -> None:
    medico = build_medico()
    service = AuthService(
        session=FakeSession(scalar_values=[medico]),
        verify_password=lambda plain, hashed: False,
        generate_session_token=lambda: "unused",
        session_ttl_seconds=3600,
    )

    with pytest.raises(AuthenticationError):
        await service.login(email="maria@email.com", senha="errada")


@pytest.mark.asyncio
async def test_get_authenticated_medico_raises_for_expired_session() -> None:
    expired_session = Session(
        token="expired",
        expira_em=datetime.now(UTC).replace(tzinfo=None) - timedelta(seconds=1),
        revogada_em=None,
    )
    service = AuthService(
        session=FakeSession(scalar_values=[expired_session]),
        verify_password=lambda plain, hashed: True,
        generate_session_token=lambda: "unused",
        session_ttl_seconds=3600,
    )

    with pytest.raises(AuthenticationError):
        await service.get_authenticated_medico("expired")
