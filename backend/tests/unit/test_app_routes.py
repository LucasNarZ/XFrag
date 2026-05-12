from contextlib import contextmanager
from datetime import date, datetime

from fastapi.testclient import TestClient

from app.core.dependencies import get_current_medico, get_paciente_service
from app.main import app
from app.models.medico import Medico


def test_app_has_routes() -> None:
    paths = {route.path for route in app.routes}

    assert "/api/auth/login" in paths
    assert "/api/medicos/" in paths
    assert "/api/medicos/{medico_id}" in paths
    assert "/api/pacientes/" in paths
    assert "/api/pacientes/{paciente_id}" in paths
    assert "/api/pacientes/{paciente_id}/avaliacoes" in paths
    assert "/api/sintomas/" in paths
    assert "/api/sintomas/{sintoma_id}" in paths
    assert "/api/avaliacoes" in paths
    assert "/api/avaliacoes/{avaliacao_id}" in paths
    assert "/api/avaliacoes/{avaliacao_id}/relatorio" in paths


@contextmanager
def make_test_client():
    client = TestClient(app)

    try:
        yield client
    finally:
        client.close()


def test_me_route_allows_dependency_override() -> None:
    async def override_current_medico():
        return Medico(
            id=1,
            nome="Dra. Ana",
            crm="12345",
            especialidade="Cardiologia",
            email="ana@example.com",
            senha_hash="hash",
            criado_em=datetime(2025, 1, 1, 10, 0, 0),
        )

    app.dependency_overrides[get_current_medico] = override_current_medico

    try:
        with make_test_client() as client:
            response = client.get("/api/auth/me")

        assert response.status_code == 200
        assert response.json()["email"] == "ana@example.com"
    finally:
        app.dependency_overrides.clear()


def test_list_pacientes_route_allows_service_override() -> None:
    class FakePacienteService:
        async def list(self, *, medico_id: int):
            assert medico_id == 1
            return [
                {
                    "id": 10,
                    "medico_id": 1,
                    "nome": "Paciente Teste",
                    "data_nascimento": date(2000, 5, 20),
                    "sexo": "M",
                    "responsavel": "Responsavel Teste",
                    "observacoes": "Observacao teste",
                    "criado_em": datetime(2025, 1, 1, 9, 0, 0),
                }
            ]

    async def override_current_medico():
        return Medico(
            id=1,
            nome="Dra. Ana",
            crm="12345",
            especialidade="Cardiologia",
            email="ana@example.com",
            senha_hash="hash",
            criado_em=datetime(2025, 1, 1, 10, 0, 0),
        )

    async def override_paciente_service():
        return FakePacienteService()

    app.dependency_overrides[get_current_medico] = override_current_medico
    app.dependency_overrides[get_paciente_service] = override_paciente_service

    try:
        with make_test_client() as client:
            response = client.get("/api/pacientes/")

        body = response.json()

        assert response.status_code == 200
        assert len(body) == 1
        assert body[0]["nome"] == "Paciente Teste"
        assert "idade" not in body[0]
    finally:
        app.dependency_overrides.clear()
