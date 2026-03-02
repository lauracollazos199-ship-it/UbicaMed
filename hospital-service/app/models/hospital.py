from typing import List
from pydantic import BaseModel


class HospitalBase(BaseModel):
    nombre: str
    latitud: float
    longitud: float


class HospitalCrear(HospitalBase):
    eps_ids: List[int]


class Hospital(HospitalBase):
    id: int
    eps: List[str]

    model_config = {
        "from_attributes": True
    }