from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.hospital import Hospital, HospitalCrear, EPS
from app.services import hospital_service
from app.services.hospital_service import (
    HospitalNoEncontradoError,
    EPSNoEncontradaError,
    HospitalDuplicadoError
)

router = APIRouter()



# LISTAR HOSPITALES 

@router.get("/hospitales", response_model=List[Hospital])
def listar_hospitales(
    eps: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        if eps:
            return hospital_service.obtener_hospitales_por_eps(db, eps)
        return hospital_service.obtener_hospitales(db)

    except EPSNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# DETALLE DE HOSPITAL

@router.get("/hospitales/{hospital_id}", response_model=Hospital)
def hospital_por_id(hospital_id: int, db: Session = Depends(get_db)):
    try:
        return hospital_service.obtener_hospital_por_id(db, hospital_id)
    except HospitalNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e



# LISTAR EPS

@router.get("/eps", response_model=List[EPS])
def listar_eps(db: Session = Depends(get_db)):
    return hospital_service.obtener_eps(db)


# CREAR HOSPITAL

@router.post("/hospitales", response_model=Hospital)
def agregar_hospital(hospital: HospitalCrear, db: Session = Depends(get_db)):
    try:
        return hospital_service.crear_hospital(db, hospital)

    except HospitalDuplicadoError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except EPSNoEncontradaError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# ELIMINAR HOSPITAL

@router.delete("/hospitales/{hospital_id}")
def borrar_hospital(hospital_id: int, db: Session = Depends(get_db)):
    try:
        return hospital_service.eliminar_hospital(db, hospital_id)
    
    except HospitalNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e