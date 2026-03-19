from pydantic import BaseModel
from typing import List

class Location (BaseModel):
    latitud: float
    longitud: float 


class HospitalLocation(BaseModel):
    id: int
    nombre: str
    latitud: float
    longitud: float
    direccion: str

class HospitalesRequest(BaseModel):
    usuario: Location
    hospitales: List[HospitalLocation]