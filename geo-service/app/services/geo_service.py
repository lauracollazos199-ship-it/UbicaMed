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
        lon1 = radians(usuario.longitud)

        lat2 = radians(hospital.latitud)
        lon2 = radians(hospital.longitud)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distancia = R * c

        return distancia

    except Exception as e:
        raise UbicacionInvalidaError(
            "No se pudo calcular la distancia"
        ) from e


def hospitales_ordenados(usuario: Location, hospitales: list[HospitalLocation]):

    try:

        if not hospitales:
            raise HospitalNoEncontradoError("No hay hospitales disponibles")

        resultado = []

        for hospital in hospitales:

            distancia = round(calcular_distancia(usuario, hospital),2)

            resultado.append({
                **hospital.dict(),
                "distancia_km": distancia
            })

        resultado.sort(key=lambda x: x["distancia_km"])

        return resultado

    except Exception as e:

        raise UbicacionInvalidaError(
            "Error al ordenar hospitales por distancia"
        ) from e


def hospital_mas_cercano(usuario: Location, hospitales: list[HospitalLocation]):

    hospitales_distancia = hospitales_ordenados(usuario, hospitales)

    if not hospitales_distancia:

        raise HospitalNoEncontradoError(
            "No hay hospitales disponibles"
        )

    return hospitales_distancia[0]