from sqlalchemy.orm import Session
from app.database.models_db import HospitalDB, EPSDB, ConvenioDB
from app.models.hospital import HospitalCrear


# Obtener todos los hospitales
def obtener_hospitales(db: Session):
    return db.query(HospitalDB).all()


# Obtener hospital por id
def obtener_hospital_por_id(db: Session, hospital_id: int):
    hospital = db.query(HospitalDB).filter(HospitalDB.id == hospital_id).first()
    return hospital


# Crear hospital
def crear_hospital(db: Session, hospital : HospitalCrear):
    
    nuevo_hospital = HospitalDB(
        nombre= hospital.nombre,
        latitud= hospital.latitud,
        longitud= hospital.longitud
    )

    db.add(nuevo_hospital)
    db.commit()
    db.refresh(nuevo_hospital)

    return nuevo_hospital


# Eliminar hospital
def eliminar_hospital(db: Session, hospital_id: int):

    hospital = db.query(HospitalDB).filter(HospitalDB.id == hospital_id).first()

    if hospital:
        db.delete(hospital)
        db.commit()
        return True
    
    return False


# Obtener hospitales por EPS
def obtener_hospitales_por_eps(db: Session, nombre_eps: str):

    hospitales = (
        db.query(HospitalDB)
        .join(ConvenioDB, HospitalDB.id == ConvenioDB.hospital_id)
        .join(EPSDB, EPSDB.id == ConvenioDB.eps_id)
        .filter(EPSDB.nombre == nombre_eps)
        .distinct()
        .all()
    )

    return hospitales


# Crear EPS
def crear_eps(db: Session, nombre: str):

    nueva_eps = EPSDB(nombre=nombre)

    db.add(nueva_eps)
    db.commit()
    db.refresh(nueva_eps)

    return nueva_eps


# Crear convenio hospital - eps
def crear_convenio(db: Session, hospital_id: int, eps_id: int):

    convenio = ConvenioDB(
        hospital_id=hospital_id,
        eps_id=eps_id
    )

    db.add(convenio)
    db.commit()
    db.refresh(convenio)

    return convenio