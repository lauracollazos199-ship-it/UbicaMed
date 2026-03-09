from app.exceptions import (
    UsuarioNoExisteError,
    UsuarioYaExisteError,
    ListaUsuariosVaciaError
)

usuarios = []

def obtener_usuarios():
    if not usuarios:
        raise ListaUsuariosVaciaError("No existen usuarios registrados")
    return usuarios


def obtener_usuario_por_id(user_id: int):
    usuario = next((u for u in usuarios if u.id == user_id), None)

    if usuario is None:
        raise UsuarioNoExisteError("El usuario no existe")

    return usuario


def crear_usuario(user):
    if any(u.id == user.id for u in usuarios):
        raise UsuarioYaExisteError("El usuario ya existe")

    usuarios.append(user)
    return user


def eliminar_usuario(user_id: int):
    usuario = next((u for u in usuarios if u.id == user_id), None)

    if usuario is None:
        raise UsuarioNoExisteError("El usuario no existe")

    usuarios.remove(usuario)