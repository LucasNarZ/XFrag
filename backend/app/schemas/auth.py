from app.schemas.common import BaseSchema
from app.schemas.medico import MedicoResponse


class LoginRequest(BaseSchema):
    email: str
    senha: str


class LoginResponse(BaseSchema):
    medico: MedicoResponse
