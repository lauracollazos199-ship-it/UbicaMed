from sqlalchemy.orm import Session
from app.database.models_db import UserDB
from app.models.user import UserCreate


# obtener usuarios
def obtener_usuarios(db: Session):
    return db.query(UserDB).all()


# obtener usuario por id
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
