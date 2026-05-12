from enum import Enum

from pydantic import BaseModel, ConfigDict


class Sexo(str, Enum):
    M = "M"
    F = "F"


class Recomendacao(str, Enum):
    ENCAMINHAR = "ENCAMINHAR"
    NAO_ENCAMINHAR = "NAO_ENCAMINHAR"


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
