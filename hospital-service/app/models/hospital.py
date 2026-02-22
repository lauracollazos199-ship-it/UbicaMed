from typing import List
from pydantic import BaseModel

class Hospital(BaseModel):
    id: int
    nombre: str
    eps: List[str]
    latitud : float
    longitud: float

class HospitalCrear(BaseModel):
    nombre: str
    eps: str
    latitud: float
    longitud: float