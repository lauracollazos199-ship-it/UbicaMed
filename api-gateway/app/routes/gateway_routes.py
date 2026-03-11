from fastapi import APIRouter, HTTPException
import requests
from requests.exceptions import Timeout

router = APIRouter()

HOSPITAL_SERVICE = "http://127.0.0.1:8001"
GEO_SERVICE = "http://127.0.0.1:8002"


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
    
    except HTTPException:
        raise

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


@router.get("/hospitales/eps/{eps}")
def hospitales_por_eps(eps: str):

    try:
        response = requests.get(
            f"{HOSPITAL_SERVICE}/hospitales/eps/{eps}",
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al filtrar hospitales"
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
# GEO SERVICE
# =================================

@router.post("/hospitales-ordenados")
def hospitales_ordenados(data: dict):

    try:
        response = requests.post(
            f"{GEO_SERVICE}/hospitales-ordenados",
            json=data,
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error en geo-service"
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="geo-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e


@router.post("/hospital-mas-cercano")
def hospital_mas_cercano(data: dict):

    try:
        response = requests.post(
            f"{GEO_SERVICE}/hospital-mas-cercano",
            json=data,
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error en geo-service"
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="geo-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e


# =================================
# ORQUESTACIÓN DE MICROSERVICIOS
# =================================

@router.post("/hospitales-cercanos")
def hospitales_cercanos(data: dict):

    try:

        eps = data.get("eps")
        usuario = data.get("usuario")

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

        # enviar hospitales a geo-service
        response_geo = requests.post(
            f"{GEO_SERVICE}/hospitales-ordenados",
            json={
                "usuario": usuario,
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
            detail="Uno de los microservicios no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e