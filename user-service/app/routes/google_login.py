from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app.database.database import get_db
from app.services.user_service import crear_usuario
from app.models.user import UserCreate

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
        # 1️⃣ Verificar token de Google
        idinfo = id_token.verify_oauth2_token(data.token, google_requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo.get("email")
        name = idinfo.get("name")
        if not name:
            name = email.split("@")[0]  

        
        user_create = UserCreate(
            nombre=name,
            email=email,
            password="GoogleLogin123!",  # Contraseña temporal obligatoria para el modelo
            
        )
        nuevo_usuario = crear_usuario(db, user_create)

        
        payload = {"user_id": nuevo_usuario.id, "email": nuevo_usuario.email}
        token_jwt = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {"access_token": token_jwt, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error login con Google: {str(e)}")