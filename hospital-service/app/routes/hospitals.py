from fastapi import APIRouter
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
    return obtener_hospitales_por_eps(eps)


@router.get("/hospitales/{id}")
def hospital_por_id(hospital_id: int):
    return obtener_hospital_por_id(hospital_id)


@router.post("/hospitales")
def agregar_hospital(hospital: Hospital):
    return crear_hospital(hospital)


@router.delete("/hospitales/{id}")
def borrar_hospital(hospital_id: int):
    return eliminar_hospital(hospital_id)