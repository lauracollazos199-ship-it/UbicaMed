from fastapi import APIRouter, HTTPException
from app.services.hospital_service import (
    obtener_hospitales,
    obtener_hospitales_por_eps,
    obtener_hospital_por_id,
    crear_hospital,
    eliminar_hospital
)

from app.models.hospital import Hospital

router = APIRouter()


@router.get("/hospitales")
def listar_hospitales():
    return obtener_hospitales()

@router.get("/hospitales/eps/{eps}")
def hospitales_por_eps(eps: str):
    try:
        return obtener_hospitales_por_eps(eps)
    except ValueError as e:
        raise HTTPException (status_code=404, detail=str(e)) from e
    


@router.get("/hospitales/{id}")
def hospital_por_id(hospital_id: int):
    try: 
        return obtener_hospital_por_id(hospital_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/hospitales")
def agregar_hospital(hospital: Hospital):
    try:
        return crear_hospital(hospital)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/hospitales/{id}")
def borrar_hospital(hospital_id: int):
    try:
        return eliminar_hospital(hospital_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e