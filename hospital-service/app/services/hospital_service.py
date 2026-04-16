from sqlalchemy.orm import Session
from app.database import crud
from app.database.models_db import HospitalDB, ConvenioDB, EPSDB
from app.models.hospital import HospitalCrear

class HospitalNoEncontradoError(Exception):
    pass


class EPSNoEncontradaError(Exception):
    pass


class HospitalDuplicadoError(Exception):
    pass


def obtener_hospitales(db: Session):
    return crud.obtener_hospitales(db)
   

def obtener_eps(db: Session):
    return crud.obtener_eps(db)
  


def obtener_hospital_por_id(db: Session, hospital_id: int):
    hospital = crud.obtener_hospital_por_id(db, hospital_id)
   
    if hospital is None:
        raise HospitalNoEncontradoError("Hospital no encontrado")
    
    return hospital


def obtener_hospitales_por_eps(db: Session, eps_nombre: str):
    hospitales = crud.obtener_hospitales_por_eps(db, eps_nombre)
    
    if not hospitales:
        raise EPSNoEncontradaError(f"No hay hospitales para esa EPS '{eps_nombre}'")
    
    return hospitales


def crear_hospital(db: Session, hospital: HospitalCrear):
    try:
        # VALIDAR SI YA EXISTE
        hospital_existente = db.query(HospitalDB).filter(
            HospitalDB.nombre == hospital.nombre,
            HospitalDB.direccion == hospital.direccion
        ).first()

        if hospital_existente:
            raise HospitalDuplicadoError(
                "Ya existe un hospital con ese nombre y dirección"
            )

        # VALIDAR EPS EXISTEN
        eps_existentes = db.query(EPSDB).filter(
            EPSDB.id.in_(hospital.eps_ids)
        ).all()

        if len(eps_existentes) != len(hospital.eps_ids):
            raise EPSNoEncontradaError(
                "Una o más EPS no existen"
            )

        # CREAR HOSPITAL
        nuevo_hospital = HospitalDB(
            nombre=hospital.nombre,
            direccion=hospital.direccion,
            latitud=hospital.latitud,
            longitud=hospital.longitud
        )

        db.add(nuevo_hospital)
        db.flush()  

        # CREAR RELACIONES (CONVENIOS)
        for eps_id in hospital.eps_ids:
            convenio = ConvenioDB(
                hospital_id=nuevo_hospital.id,
                eps_id=eps_id
            )
            db.add(convenio)

        db.commit()
        db.refresh(nuevo_hospital)

        return nuevo_hospital

    except:
        db.rollback()
        raise

def eliminar_hospital(db: Session, hospital_id: int):
    hospital = crud.eliminar_hospital(db, hospital_id)
    if hospital is None:
        raise HospitalNoEncontradoError("Hospital no encontrado")
    
    return {"mensaje": "Hospital eliminado correctamente"}

