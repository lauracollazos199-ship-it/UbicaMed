from sqlalchemy.orm import Session
from app.database.crud import obtener_usuarios as crud_listar, obtener_usuario_por_id as crud_por_id, crear_usuario as crud_crear, eliminar_usuario as crud_eliminar, actualizar_usuario as crud_actualizar
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

# Obtener usuario por email
def obtener_usuario_por_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

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


def actualizar_usuario(db: Session, user_id: int, datos: dict):
    usuario = obtener_usuario_por_id(db, user_id)
    if not usuario:
        raise UsuarioNoExisteError(f"El usuario con ID {user_id} no existe")

    es_google = usuario.password == "GoogleAuth123!"

    # Bloquear cambio de contraseña para Google
    if es_google and "password" in datos:
        raise ValueError("Los usuarios de Google no pueden cambiar contraseña")

    # Validar contraseña actual para usuarios normales
    if "password" in datos:
        old_password = datos.get("old_password")
        if not old_password:
            raise ValueError("Debes ingresar la contraseña actual")
        if usuario.password != old_password:
            raise ValueError("La contraseña actual no coincide")

    # Validar si realmente hay cambios
    cambios = {}
    for key, value in datos.items():
        if key in {"nombre", "email", "password"} and getattr(usuario, key) != value:
            cambios[key] = value

    if not cambios:
        raise ValueError("No hay cambios para actualizar")

    return crud_actualizar(db, user_id, cambios)