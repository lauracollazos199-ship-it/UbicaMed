from math import radians, sin, cos, sqrt, atan2
from app.models.location import Location, HospitalLocation

class UbicacionInvalidaError(Exception):
    pass

class HospitalNoEncontradoError(Exception):
    pass

def calcular_distancia(usuario: Location, hospital: HospitalLocation):
    try:

        R = 6371

        lat1 = radians(usuario.latitud)
        lon1 = radians(usuario.longuitud)

        lat2 = radians(hospital.latitud)
        lon2 = radians(hospital.longitud)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) + cos(lat2) * sin(dlon /2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        distancia = R * c

        return distancia 
    
    except Exception as e: 
        raise UbicacionInvalidaError (
            "No se pudo calcular la distancia"
        ) from e 
    
    

