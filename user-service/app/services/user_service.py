from sqlalchemy.orm import Session
from app.database.crud import (
    obtener_usuarios as crud_obtener_usuarios,
    obtener_usuario_por_id as crud_obtener_usuario_por_id,
    crear_usuario as crud_crear_usuario,
    eliminar_usuario as crud_eliminar_usuario
)

from app.models.user import User
from app.database.models_db import UserDB
from app import security


class UsuarioNoExisteError(Exception):
    pass


class UsuarioYaExisteError(Exception):
    pass


class ListaUsuariosVaciaError(Exception):
    pass


# Obtener usuarios
def obtener_usuarios(db: Session):

    usuarios = crud_obtener_usuarios(db)

    if not usuarios:
        raise ListaUsuariosVaciaError("No existen usuarios registrados")

    return usuarios


# Obtener usuario por id
def obtener_usuario_por_id(db: Session, user_id: int):

    usuario = crud_obtener_usuario_por_id(db, user_id)

    if usuario is None:
        raise UsuarioNoExisteError("El usuario no existe")

    return usuario


# Crear usuario
def crear_usuario(db: Session, user: User):

    existente = db.query(UserDB).filter(UserDB.email == user.email).first()

    if existente:
        raise UsuarioYaExisteError("El usuario ya existe")

    #  encriptar contraseña
    user.password = security.hash_password(user.password)

    return crud_crear_usuario(db, user)


# Eliminar usuario
def eliminar_usuario(db: Session, user_id: int):

    usuario = crud_obtener_usuario_por_id(db, user_id)

    if usuario is None:
        raise UsuarioNoExisteError("El usuario no existe")

    crud_eliminar_usuario(db, user_id)

    return True