from sqlalchemy.orm import Session
from app.database.models_db import UserDB
from app.models.user import UserCreate


# obtener usuarios
def obtener_usuarios(db: Session):
    return db.query(UserDB).all()


# obtener usuario por id
def obtener_usuario_por_id(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()


# crear usuario
def crear_usuario(db: Session, user: UserCreate):

    nuevo_usuario = UserDB(
        nombre=user.nombre,
        email=user.email,
        eps=user.eps
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# eliminar usuario
def eliminar_usuario(db: Session, user_id: int):

    usuario = db.query(UserDB).filter(UserDB.id == user_id).first()

    if usuario:
        db.delete(usuario)
        db.commit()
        return True

    return False