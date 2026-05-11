from fastapi import APIRouter, Depends, Response

from app.core.config import settings
from app.core.dependencies import get_auth_service, get_current_medico
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.medico import MedicoResponse
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.login(payload.email, payload.senha)
    response.set_cookie(
        key=settings.session_cookie_name,
        value=result["session_token"],
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
        max_age=settings.session_ttl_seconds,
    )
    return {"medico": result["medico"]}


@router.get("/me", response_model=MedicoResponse)
async def me(medico=Depends(get_current_medico)):
    return medico
