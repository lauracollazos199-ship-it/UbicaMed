from fastapi import APIRouter, HTTPException

from app.models.location import Location, HospitalLocation, HospitalesRequest
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
def obtener_hospitales_cercanos(data: HospitalesRequest):

    try:

        resultado = hospitales_ordenados(
            data.usuario, 
            data.hospitales)

        return resultado

    except UbicacionInvalidaError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e


@router.post("/hospital-mas-cercano")
def obtener_hospital_mas_cercano(data: HospitalesRequest):

    try:

        resultado = hospital_mas_cercano(
            data.usuario, 
            data.hospitales)

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