import os
from fastapi import APIRouter, HTTPException, Body
import requests

from dotenv import load_dotenv
from requests.exceptions import Timeout
from pydantic import BaseModel, EmailStr

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
                detail="No se pudo iniciar sesión con Google. Intente nuevamente."
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="El servicio tardó demasiado en responder. Intente nuevamente."
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado al iniciar sesión con Google. Intente nuevamente más tarde.")from e


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
                detail=response.json().get(
                    "detail", 
                    "No se pudo iniciar sesión. Verifique sus datos.")
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="El servicio no respondió a tiempo. Intente nuevamente"
        ) from e
    
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=""
        )from e
    
    except HTTPException:
        raise

    except Exception as e:
        print("ERROR INTERNO LOGIN:", e)
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado al iniciar sesión. Intente nuevamente más tarde."
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
                detail=response.json().get(
                    "detail", 
                    "No se pudo procesar la solicitud. Intente nuevamente."
            )
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="El servicio no respondió a tiempo. Intente nuevamente."
        ) from e

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail="No fue posible enviar el correo para restablecer la contraseña. Inténtelo nuevamente más tarde."
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
                detail=response.json().get(
                    "detail", 
                    "No se pudo actualizar la contraseña.")
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="El servicio no respondió a tiempo. Intente nuevamente."
        ) from e
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado al actualizar la contraseña. Intente nuevamente más tarde."
        ) from e


@router.post("/users")
def registrar_usuario(data: dict):
    try:
        response = requests.post(
            f"{USER_SERVICE}/users",
            json=data,
            timeout=5
        )

        try:
            response_data = response.json()
        except ValueError:
            response_data = {}

        if not response.ok:
            detail = response_data.get("detail", response_data)

            if isinstance(detail, list):
                detail = " | ".join(
                    str(e.get("msg", e)) if isinstance(e, dict) else str(e)
                    for e in detail
                )

            raise HTTPException(
                status_code=response.status_code,
                detail=detail
            )

        return response_data

    except HTTPException:
        raise

    except Timeout as e:
        raise HTTPException (
            status_code=504,
            detail="El servicio no respondió a tiempo. Intente nuevamente."
        )from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Se produjo un error al procesar el registro. Por favor, inténtelo de nuevo más tarde."
        ) from e
    

@router.put("/users/{user_id}")
def actualizar_usuario(user_id: int, data= Body(...)):

    try:
        response = requests.put(
            f"{USER_SERVICE}/users/{user_id}",
            json=data,
            timeout=5
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get(
                    "detail", 
                    "No se pudo actualizar la información.")
            )

        return response.json()

    except HTTPException:
        raise

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="El servicio no respondió a tiempo."
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado al actualizar la información. Intente nuevamente más tarde."
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
                detail="No se pudieron cargar las EPS."
            )

        return response.json()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="El servicio no respondió a tiempo."
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="No se pudo cargar la información necesaria para la búsqueda. Inténtelo más tarde."
        ) from e 


# ENDPOINT PRINCIPAL
@router.get("/hospitales")
def hospitales_cercanos(eps: str, lat: float, lng: float):

    try:
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

        if not hospitales:
            return []

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
    
    except HTTPException:
        raise

    except requests.exceptions.ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail="No fue posible conectar con el servicio de geolocalización."
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado al cargar los hospitales. Intente nuevamente más tarde."
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
            detail="Un microservicio no respondió a tiempo"
        ) from e
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado al obtener la información del hospital. Intente nuevamente más tarde."
        ) from e