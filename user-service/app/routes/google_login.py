from datetime import datetime, timedelta
import os
import smtplib
from email.mime.text import MIMEText



from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google.auth.exceptions import GoogleAuthError
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

class ForgotPasswordRequest(BaseModel):
    email: str




@router.post("/google")
def login_google(data: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            data.token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        name = idinfo.get("name")


        if not email:
            raise HTTPException(
                status_code=400,
                detail="No se pudo obtener el email del usuario"
            )
        
        if not name:
            name = email.split("@")[0].capitalize()

        usuario = obtener_usuario_por_email(db, email)

    
        if not usuario:
            user_create = UserCreate(
                nombre=name,
                email=email,
                password="GoogleLogin123!"  
            )
            usuario = crear_usuario(db, user_create)

        else:
            if not usuario.nombre or usuario.nombre == email.split("@")[0]:
                usuario.nombre = name
                db.commit()
                db.refresh(usuario)


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

        return {
            "access_token": token_jwt,
            "token_type": "bearer",
            "nombre": usuario.nombre,
            "email": usuario.email,
            "user_id": usuario.id 
        }

    except GoogleAuthError as e:
        raise HTTPException(400, detail= "Token de Google inválido")from e

    except Exception as e:
        raise HTTPException(500, detail= "Error interno en login con Google") from e
    
    
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        usuario = obtener_usuario_por_email(db, data.email)

        if not usuario or usuario.password != data.password:
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )

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

    except HTTPException:
        raise
    
    except Exception as e:
        print("Error en login:", e)
        raise HTTPException(status_code=500, detail="Error interno en login") from e

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        email = data.email

        if not email:
            raise HTTPException(status_code=400, detail="Email requerido")

        usuario = obtener_usuario_por_email(db, email)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="No se encontró ninguna cuenta asociada a este correo electrónico."
            )

        if usuario.password == "GoogleLogin123!":
            raise HTTPException(status_code=400, detail="Este usuario usa Google para iniciar sesión")

        token = jwt.encode({
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=10)
        }, JWT_SECRET, algorithm="HS256")

        link = f"https://ubicamed.duckdns.org/reset.html?token={token}"

        send_reset_email(email, link)

        return {
            "message": "Si el correo existe, se enviará un enlace para recuperar la contraseña"
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Error en forgot password:", e)
        raise HTTPException(status_code=500, detail="Error al procesar solicitud")from e

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        if not data.password:
            raise HTTPException(status_code=400, detail="Debe ingresar una nueva contraseña")

        try:
            payload = jwt.decode(data.token, JWT_SECRET, algorithms=["HS256"])
            email = payload["email"]

        except ExpiredSignatureError as e:
            raise HTTPException(status_code=400, detail="Token expirado")from e

        except JWTError as e:
            raise HTTPException(status_code=400, detail="Token inválido") from e

        usuario = obtener_usuario_por_email(db, email)

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no existe")

        usuario.password = data.password
        db.commit()
        db.refresh(usuario)

        return {"message": "Contraseña actualizada"}

    except HTTPException:
        raise


    except Exception as e:
        print("Error en reset password:", e)
        raise HTTPException(status_code=500, detail="Error interno") from e


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

    except smtplib.SMTPAuthenticationError as e:
        print("Error de autenticación SMTP", e)
        raise HTTPException(status_code=500, detail="Error al enviar correo") from e
    
    except smtplib.SMTPException as e:
        print("Error SMTP", e)
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo")from e