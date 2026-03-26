from typing import List
from pydantic import BaseModel


class HospitalBase(BaseModel):
    nombre: str
    direccion: str 
    latitud: float
    longitud: float

class EPS(BaseModel):
    id: int
    nombre: str

    model_config = {
        "from_attributes": True
    }

class Hospital(HospitalBase):
    id: int
    eps: List[EPS]

    model_config = {
        "from_attributes": True
    }

class HospitalCrear(HospitalBase):
    eps_ids: List[int]

