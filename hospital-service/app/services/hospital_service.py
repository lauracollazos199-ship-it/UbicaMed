from sqlalchemy.orm import Session
from app.database.models_db import HospitalDB, EPSDB


def obtener_hospitales(db: Session):
    hospitales = db.query(HospitalDB).all()

    if not hospitales:
        raise ValueError("No hay hospitales registrados")

    return hospitales


def obtener_hospital_por_id(db: Session, hospital_id: int):

    hospital = db.query(HospitalDB).filter(
        HospitalDB.id == hospital_id
    ).first()

    if hospital is None:
        raise ValueError("Hospital no encontrado")

    return hospital


def obtener_hospitales_por_eps(db: Session, eps_nombre: str):

    hospitales = (
        db.query(HospitalDB)
        .join(EPSDB)
        .filter(EPSDB.nombre == eps_nombre)
        .all()
    )

    if not hospitales:
        raise ValueError("No hay hospitales para esa EPS")

    return hospitales


def crear_hospital(db: Session, nombre: str, latitud: float, longitud: float):

    hospital = HospitalDB(
        nombre=nombre,
        latitud=latitud,
        longitud=longitud
    )

    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    return hospital


def eliminar_hospital(db: Session, hospital_id: int):

    hospital = db.query(HospitalDB).filter(
        HospitalDB.id == hospital_id
    ).first()

    if hospital is None:
        raise ValueError("Hospital no encontrado")

    db.delete(hospital)
    db.commit()

    return True