from fastapi import APIRouter, HTTPException
from app.services.user_service import (
    obtener_usuarios,
    obtener_usuario_por_id,
    crear_usuario,
    eliminar_usuario
)
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("")
def listar_usuarios():
    return obtener_usuarios()

@router.get("/{user_id}")
def usuario_por_id(user_id: int):
    try:
        return obtener_usuario_por_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@router.post("")
def agregar_usuario(user: User):
    try:
        return crear_usuario(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.delete("/{user_id}")
def borrar_usuario(user_id: int):
    try:
        eliminar_usuario(user_id)
        return {"mensaje": "Usuario eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e