from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_medico, get_paciente_service
from app.schemas.paciente import (
    CreatePacienteRequest,
    PacienteResponse,
    UpdatePacienteRequest,
)
from app.services import PacienteService

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/", response_model=PacienteResponse, status_code=201)
async def create_paciente(
    payload: CreatePacienteRequest,
    medico=Depends(get_current_medico),
    service: PacienteService = Depends(get_paciente_service),
):
    return await service.create(payload=payload, medico_id=medico.id)


@router.get("/", response_model=list[PacienteResponse])
async def list_pacientes(
    medico=Depends(get_current_medico),
    service: PacienteService = Depends(get_paciente_service),
):
    return await service.list(medico_id=medico.id)


@router.get("/{paciente_id}", response_model=PacienteResponse)
async def get_paciente(
    paciente_id: int,
    medico=Depends(get_current_medico),
    service: PacienteService = Depends(get_paciente_service),
):
    return await service.get_by_id(
        paciente_id=paciente_id,
        medico_id=medico.id,
    )


@router.put("/{paciente_id}", response_model=PacienteResponse)
async def update_paciente(
    paciente_id: int,
    payload: UpdatePacienteRequest,
    medico=Depends(get_current_medico),
    service: PacienteService = Depends(get_paciente_service),
):
    return await service.update(
        paciente_id=paciente_id,
        payload=payload,
        medico_id=medico.id,
    )
