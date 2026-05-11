from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_medico, get_sintoma_service
from app.schemas.sintoma import SintomaResponse
from app.services import SintomaService

router = APIRouter(prefix="/sintomas", tags=["Sintomas"])


@router.get("/", response_model=list[SintomaResponse])
async def list_sintomas(
    _medico=Depends(get_current_medico),
    service: SintomaService = Depends(get_sintoma_service),
):
    return await service.list()


@router.get("/{sintoma_id}", response_model=SintomaResponse)
async def get_sintoma(
    sintoma_id: int,
    _medico=Depends(get_current_medico),
    service: SintomaService = Depends(get_sintoma_service),
):
    return await service.get_by_id(sintoma_id)
