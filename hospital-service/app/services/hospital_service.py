from sqlalchemy.orm import Session
from app.database import crud
from app.models.hospital import HospitalCrear


def obtener_hospitales(db: Session):
    hospitales = crud.obtener_hospitales(db)
    if not hospitales:
        raise ValueError("No hay hospitales registrados")
    return hospitales


def obtener_hospital_por_id(db: Session, hospital_id: int):
    hospital = crud.obtener_hospital_por_id(db, hospital_id)
    if hospital is None:
        raise ValueError("Hospital no encontrado")
    return hospital


def obtener_hospitales_por_eps(db: Session, eps_nombre: str):
    hospitales = crud.obtener_hospitales_por_eps(db, eps_nombre)
    if not hospitales:
        raise ValueError("No hay hospitales para esa EPS")
    return hospitales


def crear_hospital(db: Session, hospital: HospitalCrear):
    return crud.crear_hospital(db, hospital)


def eliminar_hospital(db: Session, hospital_id: int):
    hospital = crud.eliminar_hospital(db, hospital_id)
    if hospital is None:
        raise ValueError("Hospital no encontrado")
    return {"mensaje": "Hospital eliminado correctamente"}