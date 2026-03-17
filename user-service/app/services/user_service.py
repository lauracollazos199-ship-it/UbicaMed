from sqlalchemy.orm import Session
from app.database import crud
from app.models.user import User
from app.database.models_db import UserDB


class UsuarioNoExisteError(Exception):
    pass


class UsuarioYaExisteError(Exception):
    pass



# Obtener usuarios
def obtener_usuarios(db: Session):
    return crud.obtener_usuarios(db)


# Obtener usuario por id
def obtener_usuario_por_id(db: Session, user_id: int):

    usuario = crud.obtener_usuario_por_id(db, user_id)

    if usuario is None:
        raise UsuarioNoExisteError("El usuario no existe")

    return usuario


# Crear usuario
def crear_usuario(db: Session, user: User):

    existente = db.query(UserDB).filter(UserDB.email == user.email).first()

    if existente:
        raise UsuarioYaExisteError("El usuario ya existe")

    return crud.crear_usuario(db, user)


# Eliminar usuario
def eliminar_usuario(db: Session, user_id: int):

    usuario = crud.obtener_usuario_por_id(db, user_id)

    if usuario is None:
        raise UsuarioNoExisteError("El usuario no existe")

    crud.eliminar_usuario(db, user_id)

    return True


