from pydantic import BaseModel

class Location (BaseModel):
    latitud: float
    longitud: float 


class HospitalLocation(BaseModel):
    id: int
    nombre: str
    latitud: float
    longitud: float