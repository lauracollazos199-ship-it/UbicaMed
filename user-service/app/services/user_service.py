from sqlalchemy.orm import Session
from app.database.crud import obtener_usuarios as crud_listar, obtener_usuario_por_id as crud_por_id, crear_usuario as crud_crear, eliminar_usuario as crud_eliminar
from app.models.user import User
from app.database.models_db import UserDB

# Excepciones personalizadas
class UsuarioNoExisteError(Exception): pass
class UsuarioYaExisteError(Exception): pass
class ListaUsuariosVaciaError(Exception): pass

# Listar usuarios
def obtener_usuarios(db: Session):
    usuarios = crud_listar(db)
    if not usuarios:
        raise ListaUsuariosVaciaError("No existen usuarios registrados")
    return usuarios

# Obtener usuario por ID
def obtener_usuario_por_id(db: Session, user_id: int):
    usuario = crud_por_id(db, user_id)
    if usuario is None:
        raise UsuarioNoExisteError(f"El usuario con ID {user_id} no existe")
    return usuario

# Crear usuario
def crear_usuario(db: Session, user: User):
    existente = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existente:
        raise UsuarioYaExisteError(f"El usuario con email {user.email} ya existe")
    return crud_crear(db, user)

# Eliminar usuario
def eliminar_usuario(db: Session, user_id: int):
    usuario = crud_por_id(db, user_id)
    if usuario is None:
        raise UsuarioNoExisteError(f"El usuario con ID {user_id} no existe")
    crud_eliminar(db, user_id)
    return True