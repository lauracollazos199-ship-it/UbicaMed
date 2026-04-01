from fastapi import APIRouter, HTTPException
import requests
from requests.exceptions import Timeout

router = APIRouter()

HOSPITAL_SERVICE = "http://127.0.0.1:8001"
GEO_SERVICE = "http://127.0.0.1:8002"



# LISTAR EPS

@router.get("/eps")
def listar_eps():

    try:
        response = requests.get(
            f"{HOSPITAL_SERVICE}/eps",
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error obteniendo EPS"
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="hospital-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e



# ENDPOINT PRINCIPAL

@router.get("/hospitales")
def hospitales_cercanos(eps: str, lat: float, lng: float):

    try:
        # 🔹 Validaciones
        if lat < -90 or lat > 90:
            raise HTTPException(
                status_code=400,
                detail="Latitud inválida"
            )

        if lng < -180 or lng > 180:
            raise HTTPException(
                status_code=400,
                detail="Longitud inválida"
            )

        # 🔹 1. Obtener hospitales por EPS
        response_hospital = requests.get(
            f"{HOSPITAL_SERVICE}/hospitales?eps={eps}",
            timeout=5
        )

        if response_hospital.status_code != 200:
            raise HTTPException(
                status_code=response_hospital.status_code,
                detail="Error obteniendo hospitales"
            )

        hospitales = response_hospital.json()

        # 🔹 Validar lista vacía
        if not hospitales:
            return []

        # 🔹 2. Calcular distancias en geo-service
        response_geo = requests.post(
            f"{GEO_SERVICE}/geo/hospitales-cercanos",
            json={
                "usuario": {
                    "latitud": lat,
                    "longitud": lng
                },
                "hospitales": hospitales
            },
            timeout=5
        )

        if response_geo.status_code != 200:
            raise HTTPException(
                status_code=response_geo.status_code,
                detail="Error calculando distancias"
            )

        return response_geo.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="Un microservicio no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e



# DETALLE DE HOSPITAL

@router.get("/hospitales/{hospital_id}")
def hospital_por_id(hospital_id: int):

    try:
        response = requests.get(
            f"{HOSPITAL_SERVICE}/hospitales/{hospital_id}",
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al obtener hospital"
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="hospital-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e