from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_medico, get_medico_service
from app.schemas.medico import (
    CreateMedicoRequest,
    MedicoResponse,
)
from app.services import MedicoService

router = APIRouter(prefix="/medicos", tags=["Medicos"])


@router.post("/", response_model=MedicoResponse, status_code=201)
async def create_medico(
    payload: CreateMedicoRequest,
    service: MedicoService = Depends(get_medico_service),
):
    return await service.create(
        nome=payload.nome,
        crm=payload.crm,
        especialidade=payload.especialidade,
        email=payload.email,
        senha=payload.senha,
    )


@router.get("/", response_model=list[MedicoResponse])
async def list_medicos(
    _medico=Depends(get_current_medico),
    service: MedicoService = Depends(get_medico_service),
):
    return await service.list()


@router.get("/{medico_id}", response_model=MedicoResponse)
async def get_medico(
    medico_id: int,
    _medico=Depends(get_current_medico),
    service: MedicoService = Depends(get_medico_service),
):
    return await service.get_by_id(medico_id)
