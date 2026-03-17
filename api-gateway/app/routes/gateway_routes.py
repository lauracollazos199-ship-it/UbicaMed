from fastapi import APIRouter, HTTPException
import requests
from requests.exceptions import Timeout
from pydantic import BaseModel

router = APIRouter()

HOSPITAL_SERVICE = "http://127.0.0.1:8001"
GEO_SERVICE = "http://127.0.0.1:8002"
USER_SERVICE = "http://127.0.0.1:8003"


# ==============================
# MODELO DE ENTRADA
# ==============================

class Ubicacion(BaseModel):
    latitud: float
    longitud: float


# =================================
# HOSPITAL SERVICE
# =================================

@router.get("/hospitales")
def listar_hospitales():

    try:
        response = requests.get(
            f"{HOSPITAL_SERVICE}/hospitales",
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error en hospital-service"
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


# =================================
# ORQUESTACIÓN PRINCIPAL
# =================================

@router.post("/hospitales-cercanos/{user_id}")
def hospitales_cercanos(user_id: int, ubicacion: Ubicacion):

    try:
        # obtener usuario
        response_user = requests.get(
            f"{USER_SERVICE}/users/{user_id}",
            timeout=5
        )

        if response_user.status_code != 200:
            raise HTTPException(
                status_code=response_user.status_code,
                detail="Error obteniendo usuario"
            )

        usuario = response_user.json()
        eps = usuario["eps"]

        # obtener hospitales por EPS
        response_hospital = requests.get(
            f"{HOSPITAL_SERVICE}/hospitales/eps/{eps}",
            timeout=5
        )

        if response_hospital.status_code != 200:
            raise HTTPException(
                status_code=response_hospital.status_code,
                detail="Error obteniendo hospitales"
            )

        hospitales = response_hospital.json()

        # enviar a geo-service
        response_geo = requests.post(
            f"{GEO_SERVICE}/hospitales-cercanos",
            json={
                "usuario": ubicacion.dict(),
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