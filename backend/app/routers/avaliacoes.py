from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_avaliacao_read_service,
    get_avaliacao_service,
    get_current_medico,
)
from app.schemas.avaliacao import (
    AvaliacaoResponse,
    AvaliacaoResumo,
    CreateAvaliacaoRequest,
    RelatorioAvaliacaoResponse,
)
from app.services import AvaliacaoService, RelatorioService

router = APIRouter(tags=["Avaliacoes"])


@router.post(
    "/pacientes/{paciente_id}/avaliacoes",
    response_model=AvaliacaoResponse,
    status_code=201,
)
async def create_avaliacao(
    paciente_id: int,
    payload: CreateAvaliacaoRequest,
    medico=Depends(get_current_medico),
    service: AvaliacaoService = Depends(get_avaliacao_service),
):
    created = await service.create(
        payload=payload,
        paciente_id=paciente_id,
        medico_id=medico.id,
    )
    return await service.get_by_id(created.id, medico.id)


@router.get(
    "/pacientes/{paciente_id}/avaliacoes",
    response_model=list[AvaliacaoResumo],
)
async def list_avaliacoes_by_paciente(
    paciente_id: int,
    medico=Depends(get_current_medico),
    service: AvaliacaoService = Depends(get_avaliacao_service),
):
    return await service.list_by_paciente_id(paciente_id, medico.id)


@router.get("/avaliacoes", response_model=list[AvaliacaoResumo])
async def list_avaliacoes(
    medico=Depends(get_current_medico),
    service: AvaliacaoService = Depends(get_avaliacao_service),
):
    return await service.list(medico.id)


@router.get("/avaliacoes/{avaliacao_id}", response_model=AvaliacaoResponse)
async def get_avaliacao(
    avaliacao_id: int,
    medico=Depends(get_current_medico),
    service: AvaliacaoService = Depends(get_avaliacao_service),
):
    return await service.get_by_id(avaliacao_id, medico.id)


@router.get(
    "/avaliacoes/{avaliacao_id}/relatorio",
    response_model=RelatorioAvaliacaoResponse,
)
async def get_relatorio_avaliacao(
    avaliacao_id: int,
    medico=Depends(get_current_medico),
    service: AvaliacaoService = Depends(get_avaliacao_read_service),
):
    avaliacao = await service.get_by_id(avaliacao_id, medico.id)
    return RelatorioService.build(avaliacao)
