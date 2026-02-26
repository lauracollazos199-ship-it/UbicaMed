from app.models.user import User

usuarios = []

def obtener_usuarios():
    return usuarios

def obtener_usuario_por_id(user_id: int):
    for usuario in usuarios:
        if usuario.id == user_id:
            return usuario
    raise ValueError("Usuario no encontrado")

def crear_usuario(user: User):
    for u in usuarios:
        if u.id == user.id:
            raise ValueError("El usuario ya existe")
    usuarios.append(user)
    return user

def eliminar_usuario(user_id: int):
    for usuario in usuarios:
        if usuario.id == user_id:
            usuarios.remove(usuario)
            return
    raise ValueError("Usuario no encontrado")