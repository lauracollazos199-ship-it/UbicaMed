from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session

from app.database.models_db import UserDB, AuthAccountDB

GOOGLE_CLIENT_ID = "TU_CLIENT_ID_DE_GOOGLE"


def login_google(db: Session, token: str):

    # verificar token con Google
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

    google_id = idinfo["sub"]
    email = idinfo["email"]
    nombre = idinfo.get("name")

    # buscar si ya existe autenticación
    auth = db.query(AuthAccountDB).filter(
        AuthAccountDB.provider_user_id == google_id
    ).first()

    if auth:
        return auth.user

    # buscar usuario por email
    usuario = db.query(UserDB).filter(UserDB.email == email).first()

    # si no existe usuario lo creamos
    if not usuario:

        usuario = UserDB(
            nombre=nombre,
            email=email
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    # crear conexión con google
    nueva_auth = AuthAccountDB(
        user_id=usuario.id,
        provider="google",
        provider_user_id=google_id
    )

    db.add(nueva_auth)
    db.commit()

    return usuario