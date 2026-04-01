from sqlalchemy.orm import Session
from app.database.models_db import HospitalDB, EPSDB, ConvenioDB
from app.models.hospital import HospitalCrear
from sqlalchemy import func


# Obtener todos los hospitales (ordenados)
def obtener_hospitales(db: Session):
    return db.query(HospitalDB).order_by(HospitalDB.id.asc()).all()


# Obtener hospital por id
def obtener_hospital_por_id(db: Session, hospital_id: int):
    return db.query(HospitalDB).filter(
        HospitalDB.id == hospital_id
    ).first()


# Crear hospital + convenios 
def crear_hospital(db: Session, hospital: HospitalCrear):

    nuevo_hospital = HospitalDB(
        nombre=hospital.nombre,
        direccion= hospital.direccion, 
        latitud=hospital.latitud,
        longitud=hospital.longitud
    )

    db.add(nuevo_hospital)
    db.flush()  

    # Crear relaciones con EPS
    for eps_id in hospital.eps_ids:
        convenio = ConvenioDB(
            hospital_id=nuevo_hospital.id,
            eps_id=eps_id
        )
        db.add(convenio)

    db.commit()  
    db.refresh(nuevo_hospital)

    return nuevo_hospital


# Eliminar hospital
def eliminar_hospital(db: Session, hospital_id: int):

    hospital = db.query(HospitalDB).filter(
        HospitalDB.id == hospital_id
    ).first()

    if hospital:
        db.delete(hospital)
        db.commit()
        return hospital

    return None


# Obtener hospitales por EPS
def obtener_hospitales_por_eps(db: Session, nombre_eps: str):

    hospitales = (
        db.query(HospitalDB)
        .join(ConvenioDB, HospitalDB.id == ConvenioDB.hospital_id)
        .join(EPSDB, EPSDB.id == ConvenioDB.eps_id)
        .filter(func.lower(EPSDB.nombre) == nombre_eps.lower())
        .order_by(HospitalDB.id.asc())
        .distinct()
        .all()
    )

    return hospitales

# Obtener EPS
def obtener_eps(db: Session):
    return db.query(EPSDB).order_by(EPSDB.nombre.asc()).all()