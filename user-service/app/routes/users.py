from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db

from app.services.user_service import (
    obtener_usuarios,
    obtener_usuario_por_id,
    crear_usuario,
    eliminar_usuario,
    actualizar_usuario,
    ListaUsuariosVaciaError,
    UsuarioNoExisteError,
    UsuarioYaExisteError
)

from app.models.user import UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ==============================
# LISTAR USUARIOS
# ==============================

@router.get("")
def listar_usuarios(db: Session = Depends(get_db)):
    try:
        return obtener_usuarios(db)
    except ListaUsuariosVaciaError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# ==============================
# OBTENER USUARIO POR ID
# ==============================

@router.get("/{user_id}")
def usuario_por_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return obtener_usuario_por_id(db, user_id)
    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# ==============================
# CREAR USUARIO
# ==============================

@router.post("")
def agregar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return crear_usuario(db, user)

    except UsuarioYaExisteError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except ValueError as e:   # errores del validator de password
        raise HTTPException(status_code=400, detail=str(e)) from e


# ==============================
# ELIMINAR USUARIO
# ==============================

@router.delete("/{user_id}")
def borrar_usuario(user_id: int, db: Session = Depends(get_db)):
    try:
        eliminar_usuario(db, user_id)
        return {"mensaje": "Usuario eliminado correctamente"}

    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    

# ==============================
# ACTUALIZAR USUARIO
# ==============================

@router.put("/{user_id}")
def actualizar(user_id: int, datos: UserUpdate, db: Session = Depends(get_db)):
    try:
        return actualizar_usuario(
            db,
            user_id,
            datos.dict(exclude_unset=True)   
        )

    except UsuarioNoExisteError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e