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
    
    model_config = {
        "extra": "ignore"
    }

class HospitalConDistancia(BaseModel):
    hospital: HospitalLocation
    distancia_km: float

    
class HospitalesRequest(BaseModel):
    usuario: Location
    hospitales: List[HospitalLocation]