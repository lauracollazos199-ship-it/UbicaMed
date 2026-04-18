from datetime import datetime, timedelta
import os
import smtplib
from email.mime.text import MIMEText


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

        if not name:
            name = email.split("@")[0].capitalize()

        if not email:
            raise HTTPException(
                status_code=400,
                detail="No se pudo obtener el email del usuario"
            )
        
        
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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error en login con Google"
        ) from e
    
    
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        usuario = obtener_usuario_por_email(db, data.email)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="El usuario no existe"
            )

        if usuario.password != data.password:
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
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        ) from e
    

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        email = data.email
        
        usuario = obtener_usuario_por_email(db, email)
        
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="No se encontró ninguna cuenta asociada a este correo electrónico."
            )
        
        if usuario.password == "GoogleLogin123!":
            raise HTTPException(
                status_code =400, 
                detail="Este usuario usa Google para iniciar sesión"
            )

        
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
        raise HTTPException(
            status_code=500,
            detail="Error enviando correo de recuperación"
        ) from e


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        token = data.token
        new_password = data.password

        if not new_password:
            raise HTTPException(
                status_code=400, 
                detail="Debe ingresar una nueva contraseña"
            )

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            email = payload["email"]
        except Exception as e:
            raise HTTPException(
                status_code= 400, 
                detail="Token inválido o expirado"
            ) from e

        usuario = obtener_usuario_por_email(db, email)

        if not usuario:
            raise HTTPException(
                status_code = 404, 
                detail= "Usuario no existe"
            )

        usuario.password = new_password
        db.commit()
        db.refresh(usuario)

        return {"message": "Contraseña actualizada"}
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error al resetear contraseña"
        ) from e


def send_reset_email(email, link):

    html = f"""
<html>
  <body style="margin:0; padding:0; background:#f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;">
      <tr>
        <td align="center">

          <!-- CARD -->
          <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.06);">

            <!-- HEADER -->
            <tr>
              <td style="padding:30px 40px 10px 40px; text-align:center;">
                <div style="font-size:22px; font-weight:700; color:#1E6FB9;">
                  UbicaMed
                </div>
                <div style="font-size:13px; color:#6b7280; margin-top:6px;">
                  Acceso seguro a hospitales según tu ubicación y EPS
                </div>
              </td>
            </tr>

            <!-- BODY -->
            <tr>
              <td style="padding:20px 40px; color:#111827; font-size:14px; line-height:1.6;">

                <p style="margin:0 0 10px;">Hola,</p>

                <p style="margin:0 0 15px;">
                  Recibimos una solicitud para restablecer la contraseña de tu cuenta.
                </p>

                <p style="margin:0 0 25px;">
                  Si fuiste tú, puedes continuar haciendo clic en el botón:
                </p>

                <!-- BUTTON -->
                <div style="text-align:center; margin:20px 0 30px;">
                  <a href="{link}"
                     style="
                       background:#1E6FB9;
                       color:#ffffff;
                       padding:12px 26px;
                       text-decoration:none;
                       border-radius:8px;
                       font-weight:600;
                       display:inline-block;
                       font-size:14px;
                     ">
                    Restablecer contraseña
                  </a>
                </div>

                <!-- WARNING BOX -->
                <div style="
                  background:#f9fafb;
                  border:1px solid #e5e7eb;
                  border-left:4px solid #1E6FB9;
                  padding:12px 14px;
                  border-radius:8px;
                  font-size:12px;
                  color:#4b5563;
                ">
                  <strong style="color:#111827;">Seguridad:</strong>
                  Este enlace expirará en <strong>10 minutos</strong>.  
                  Si no solicitaste este cambio, puedes ignorar este mensaje.
                </div>

              </td>
            </tr>

            <!-- FOOTER -->
            <tr>
              <td style="padding:20px 40px; text-align:center; font-size:11px; color:#9ca3af;">
                UbicaMed · Sistema de acceso seguro
              </td>
            </tr>

          </table>

        </td>
      </tr>
    </table>

  </body>
</html>
"""

    msg = MIMEText(html, "html")
    msg["Subject"] = "UbicaMed - Recuperación de contraseña"
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
        print("Error de autenticación")

    except smtplib.SMTPException as e:
        print("Error SMTP:", e)