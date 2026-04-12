from datetime import datetime, timedelta
import os
import smtplib
from email.mime.text import MIMEText
import smtplib


from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session
from dotenv import load_dotenv


from app.database.database import get_db
from app.services.user_service import crear_usuario, obtener_usuario_por_email
from app.models.user import UserCreate, UserLogin, ResetPasswordRequest


load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


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
        name = idinfo.get("name")

        if not name:
            name = email.split("@")[0].capitalize()

        if not email:
            raise HTTPException(
                status_code=400,
                detail="No se pudo obtener el email del usuario"
            )

        # 2. Buscar usuario en BD
        usuario = obtener_usuario_por_email(db, email)

        # 3. Crear usuario si no existe
        if not usuario:
            user_create = UserCreate(
                nombre=name,
                email=email,
                password="GoogleAuth123!"  # cumple validaciones
            )
            usuario = crear_usuario(db, user_create)

        else:
            if not usuario.nombre or usuario.nombre == email.split("@")[0]:
                usuario.nombre = name
                db.commit()
                db.refresh(usuario)


        # 4. Generar JWT con expiración
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

        # 5. Respuesta
        return {
            "access_token": token_jwt,
            "token_type": "bearer",
            "nombre": usuario.nombre,
            "email": usuario.email,
            "user_id": usuario.id 
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error login con Google: {str(e)}"
        ) from e
    
    
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        # 1. Buscar usuario
        usuario = obtener_usuario_por_email(db, data.email)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="El usuario no existe"
            )

        # 2. Validar contraseña
        if usuario.password != data.password:
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )

        # 3. Generar JWT
        payload = {
            "user_id": usuario.id,
            "email": usuario.email,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }

        token_jwt = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            "access_token": token_jwt,
            "token_type": "bearer",
            "nombre": usuario.nombre,
            "email": usuario.email,
            "user_id": usuario.id 
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e
    

@router.post("/forgot-password")
def forgot_password(data: dict, db: Session = Depends(get_db)):

    email = data.get("email")

    usuario = obtener_usuario_por_email(db, email)

    if not usuario:
        raise HTTPException(404, "Usuario no existe")

    # bloquear usuarios Google
    if usuario.password == "GoogleLogin123!":
        raise HTTPException(400, "Este usuario usa Google para iniciar sesión")

    token = jwt.encode({
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }, JWT_SECRET, algorithm="HS256")

    link = f"http://127.0.0.1:5500/reset.html?token={token}"
    
    # enviar correo
    send_reset_email(email, link)

    return {
    "message": "Si el correo existe, se enviará un enlace para recuperar la contraseña"
    }


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):

    token = data.token
    new_password = data.password

    if not new_password:
        raise HTTPException(400, "Debe ingresar una nueva contraseña")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = payload["email"]
    except Exception as e:
        raise HTTPException(400, "Token inválido o expirado") from e

    usuario = obtener_usuario_por_email(db, email)

    if not usuario:
        raise HTTPException(404, "Usuario no existe")

    usuario.password = new_password
    db.commit()
    db.refresh(usuario)

    return {"message": "Contraseña actualizada"}

# Mensaje para recuperar contraseña
def send_reset_email(email, link):

    msg = MIMEText(f"""
    <html>
      <body style="font-family: Arial; text-align: center;">
        <h2 style="color:#1E6FB9;">Recuperar contraseña</h2>
        
        <p>Hola,</p>
        
        <p>Haz clic en el siguiente botón para cambiar tu contraseña:</p>

        <a href="{link}" 
           style="
             display:inline-block;
             padding:12px 20px;
             background:#1E6FB9;
             color:white;
             text-decoration:none;
             border-radius:5px;
             font-weight:bold;
           ">
           Cambiar contraseña
        </a>

        <p style="margin-top:20px; font-size:12px; color:gray;">
          Este enlace expira en 10 minutos.
        </p>
      </body>
    </html>
    """, "html")

    msg["Subject"] = "Recuperar contraseña"
    msg["From"] = EMAIL   
    msg["To"] = email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Correo enviado correctamente")

    except smtplib.SMTPAuthenticationError:
        print("Error de autenticación (correo o contraseña incorrecta)")
    
    except smtplib.SMTPException as e:
        print("Error SMTP:", e)