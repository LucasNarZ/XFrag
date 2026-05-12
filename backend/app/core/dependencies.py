from collections.abc import AsyncGenerator

from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.security import generate_session_token, verify_password
from app.services import (
    AuthService,
    AvaliacaoService,
    MedicoService,
    PacienteService,
    SintomaService,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def build_auth_service(session: AsyncSession) -> AuthService:
    return AuthService(
        session=session,
        verify_password=verify_password,
        generate_session_token=generate_session_token,
        session_ttl_seconds=settings.session_ttl_seconds,
    )


def build_medico_service(session: AsyncSession) -> MedicoService:
    return MedicoService(session)


def build_paciente_service(session: AsyncSession) -> PacienteService:
    return PacienteService(session)


def build_sintoma_service(session: AsyncSession) -> SintomaService:
    return SintomaService(session)


def build_avaliacao_service(session: AsyncSession) -> AvaliacaoService:
    return AvaliacaoService(session)


def build_avaliacao_read_service(session: AsyncSession) -> AvaliacaoService:
    return AvaliacaoService(session)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return build_auth_service(session)


def get_medico_service(session: AsyncSession = Depends(get_session)) -> MedicoService:
    return build_medico_service(session)


def get_paciente_service(
    session: AsyncSession = Depends(get_session),
) -> PacienteService:
    return build_paciente_service(session)


def get_sintoma_service(session: AsyncSession = Depends(get_session)) -> SintomaService:
    return build_sintoma_service(session)


def get_avaliacao_service(
    session: AsyncSession = Depends(get_session),
) -> AvaliacaoService:
    return build_avaliacao_service(session)


def get_avaliacao_read_service(
    session: AsyncSession = Depends(get_session),
) -> AvaliacaoService:
    return build_avaliacao_read_service(session)


async def get_current_medico(
    session_token: str | None = Cookie(
        default=None, alias=settings.session_cookie_name
    ),
    service: AuthService = Depends(get_auth_service),
):
    return await service.get_authenticated_medico(session_token)
