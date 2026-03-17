from sqlalchemy.orm import Session

from app.database import crud
from app.models.user import User


class UsuarioNoExisteError(Exception):
    pass


class UsuarioYaExisteError(Exception):
    pass


class ListaUsuariosVaciaError(Exception):
    pass


# Obtener usuarios
def obtener_usuarios(db: Session):

    usuarios = crud.obtener_usuarios(db)

    if not usuarios:
        raise ListaUsuariosVaciaError("No existen usuarios registrados")

    return usuarios


# Obtener usuario por id
def obtener_usuario_por_id(db: Session, user_id: int):

    usuario = crud.obtener_usuario_por_id(db, user_id)

    if usuario is None:
        raise UsuarioNoExisteError("El usuario no existe")

    return usuario


# Crear usuario
def crear_usuario(db: Session, user: User):

    usuario = crud.crear_usuario(db, user)

    return usuario


# Eliminar usuario
def eliminar_usuario(db: Session, user_id: int):

    eliminado = crud.eliminar_usuario(db, user_id)

    if not eliminado:
        raise UsuarioNoExisteError("El usuario no existe")

    return True


