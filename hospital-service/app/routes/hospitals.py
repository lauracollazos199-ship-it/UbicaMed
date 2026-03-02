from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.hospital import HospitalCrear
from app.database import crud

router = APIRouter()


@router.get("/hospitales")
def listar_hospitales(db: Session = Depends(get_db)):

    try:
        return crud.obtener_hospitales(db)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/hospitales/{hospital_id}")
def hospital_por_id(hospital_id: int, db: Session = Depends(get_db)):

    try:
        return crud.obtener_hospital_por_id(db, hospital_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/hospitales/eps/{eps}")
def hospitales_por_eps(eps: str, db: Session = Depends(get_db)):

    try:
        return crud.obtener_hospitales_por_eps(db, eps)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/hospitales")
def agregar_hospital(
    hospital: HospitalCrear,
    db: Session = Depends(get_db)
):

    try:
        return crud.crear_hospital(db, hospital)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/hospitales/{hospital_id}")
def borrar_hospital(hospital_id: int, db: Session = Depends(get_db)):

    try:
        return crud.eliminar_hospital(db,hospital_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e