from sqlalchemy.orm import Session
from app.database.models_db import UserDB
from app.models.user import UserCreate
from app.database.models_db import AuthAccountDB



# Obtener usuario por email
def obtener_usuario_por_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()
# ==============================
# google

def crear_auth_google(db: Session, user_id: int, google_id: str):

    auth = AuthAccountDB(
        user_id=user_id,
        provider="google",
        provider_user_id=google_id
    )

    db.add(auth)
    db.commit()
    db.refresh(auth)

    return auth

def obtener_usuario_por_google(db: Session, google_id: str):

    return db.query(AuthAccountDB).filter(
        AuthAccountDB.provider_user_id == google_id
    ).first()
# ==============================
# OBTENER TODOS LOS USUARIOS
# ==============================

def obtener_usuarios(db: Session):
    return db.query(UserDB).all()


# ==============================
# OBTENER USUARIO POR ID
# ==============================

def obtener_usuario_por_id(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()


# ==============================
# CREAR USUARIO
# ==============================

def crear_usuario(db: Session, user: UserCreate):

    nuevo_usuario = UserDB(
        nombre=user.nombre,
        email=user.email,
        password=user.password,
        fecha_nacimiento=user.fecha_nacimiento,
        eps_id=user.eps_id
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# ==============================
# ELIMINAR USUARIO
# ==============================

def eliminar_usuario(db: Session, user_id: int):

    usuario = db.query(UserDB).filter(UserDB.id == user_id).first()

    if usuario:
        db.delete(usuario)
        db.commit()
        return True

    return False