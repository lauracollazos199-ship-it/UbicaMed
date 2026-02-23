from fastapi import APIRouter, HTTPException

from app.models.location import Location, HospitalLocation
from app.services.geo_service import (
    calcular_distancia,
    hospitales_ordenados,
    hospital_mas_cercano,
    UbicacionInvalidaError,
    HospitalNoEncontradoError
)

router = APIRouter(
    prefix="/geo",
    tags=["Geo Service"]
)


@router.post("/distancia")

def obtener_distancia(usuario: Location, hospital: HospitalLocation):

    try:

        distancia = calcular_distancia(usuario, hospital)

        return {
            "distancia_km": distancia
        }

    except UbicacionInvalidaError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e


@router.post("/hospitales-cercanos")

def obtener_hospitales_cercanos(
        usuario: Location,
        hospitales: list[HospitalLocation]
):

    try:

        resultado = hospitales_ordenados(usuario, hospitales)

        return resultado

    except UbicacionInvalidaError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e


@router.post("/hospital-mas-cercano")
def obtener_hospital_mas_cercano(
        usuario: Location,
        hospitales: list[HospitalLocation]
):

    try:

        resultado = hospital_mas_cercano(usuario, hospitales)

        return resultado

    except HospitalNoEncontradoError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        ) from e

    except UbicacionInvalidaError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e