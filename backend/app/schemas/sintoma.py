from decimal import Decimal

from app.schemas.common import BaseSchema


class SintomaResponse(BaseSchema):
    id: int
    codigo: str
    descricao: str
    peso_m: Decimal
    peso_f: Decimal | None = None
