from datetime import datetime, timedelta
import os

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database.database import get_db
from app.services.user_service import crear_usuario, obtener_usuario_por_email
from app.models.user import UserCreate, UserLogin

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


class GoogleLoginRequest(BaseModel):
    token: str  


@router.post("/google")
def login_google(data: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        # 1. Verificar token de Google
        idinfo = id_token.verify_oauth2_token(
            data.token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        name = idinfo.get("name") or email.split("@")[0]  

        if not email:
            raise HTTPException(
                status_code=400,
                detail="No se pudo obtener el email del usuario"
            )

        # 🔹 2. Buscar usuario en BD
        usuario = obtener_usuario_por_email(db, email)

        # 🔹 3. Crear usuario si no existe
        if not usuario:
            user_create = UserCreate(
                nombre=name,
                email=email,
                password="GoogleAuth123!"  # cumple validaciones
            )
            usuario = crear_usuario(db, user_create)

        # 🔹 4. Generar JWT con expiración
        payload = {
            "user_id": usuario.id,
            "email": usuario.email,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }

        token_jwt = jwt.encode(
            payload,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        # 🔹 5. Respuesta
        return {
            "access_token": token_jwt,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error login con Google: {str(e)}"
        ) from e
    
    
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        # 🔹 1. Buscar usuario
        usuario = obtener_usuario_por_email(db, data.email)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="El usuario no existe"
            )

        # 🔹 2. Validar contraseña
        if usuario.password != data.password:
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )

        # 🔹 3. Generar JWT
        payload = {
            "user_id": usuario.id,
            "email": usuario.email,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }

        token_jwt = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": token_jwt,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e