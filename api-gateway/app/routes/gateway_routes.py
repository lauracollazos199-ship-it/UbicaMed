import os
from fastapi import APIRouter, HTTPException
import requests

from dotenv import load_dotenv
from requests.exceptions import Timeout
from pydantic import BaseModel, EmailStr
from app.routes.models_user import UserUpdate, UserCreate

class GoogleLoginRequest(BaseModel):
    token: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    password: str


router = APIRouter()

load_dotenv()

HOSPITAL_SERVICE = os.getenv("HOSPITAL_SERVICE_URL", "http://127.0.0.1:8001")
GEO_SERVICE = os.getenv("GEO_SERVICE_URL", "http://127.0.0.1:8002")
USER_SERVICE = os.getenv("USER_SERVICE_URL", "http://127.0.0.1:8003")

# AUTH - GOOGLE
@router.post("/auth/google")
def login_google(data: GoogleLoginRequest):

    try:
        response = requests.post(
            f"{USER_SERVICE}/auth/google",
            json=data.model_dump(),
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error en autenticación con Google"
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="user-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e


# LOGIN NORMAL
@router.post("/auth/login")
def login(data: LoginRequest):

    try:
        response = requests.post(
            f"{USER_SERVICE}/auth/login",
            json=data.model_dump(),
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error en login"
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="user-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e


@router.post("/auth/forgot-password")
def forgot_password(data: ForgotPasswordRequest):

    try:
        response = requests.post(
            f"{USER_SERVICE}/auth/forgot-password",
            json=data.model_dump(),
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error en recuperación de contraseña")
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="user-service no respondió a tiempo"
        ) from e

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail="Error de conexión con user-service"
        ) from e


@router.post("/auth/reset-password")
def reset_password(data: ResetPasswordRequest):

    try:
        response = requests.post(
            f"{USER_SERVICE}/auth/reset-password",
            json=data.model_dump(),
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error al cambiar contraseña")
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="user-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= "Error interno del servidor"
        ) from e


@router.post("/users")
def registrar_usuario(data: UserCreate):
    try:
        response = requests.post(
            f"{USER_SERVICE}/users",
            json=data.model_dump(),
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error autenticando usuario")
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="user-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= "Error interno del servidor"
        ) from e

@router.put("/users/{user_id}")
def actualizar_usuario(user_id: int, data: UserUpdate):

    try:
        response = requests.put(
            f"{USER_SERVICE}/users/{user_id}",
            json=data.model_dump(),
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error al actualizar usuario")
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="user-service no respondió a tiempo"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e


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
            detail= "Error interno del servidor"
        ) from e


# ENDPOINT PRINCIPAL
@router.get("/hospitales")
def hospitales_cercanos(eps: str, lat: float, lng: float):

    try:
        # Validaciones
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

        # Validar lista vacía
        if not hospitales:
            return []

        # 2. Calcular distancias en geo-service
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
            detail= "Error interno del servidor"
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
            detail="Error interno del servidor"
        ) from e