from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.security import verify_password, create_access_token
from app.database import crud
from app.auth_dependencies import obtener_usuario_actual
from app.google_auth import verificar_token_google
from app.database.models_db import UserDB, AuthAccountDB

router = APIRouter(prefix="/auth", tags=["auth"])


# LOGIN NORMAL
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = crud.obtener_usuario_por_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# LOGIN CON GOOGLE
@router.post("/google")
def login_google(token: str, db: Session = Depends(get_db)):

    payload = verificar_token_google(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token Google inválido")

    email = payload["email"]
    google_id = payload["sub"]

    # buscar cuenta google
    account = db.query(AuthAccountDB).filter(
        AuthAccountDB.provider == "google",
        AuthAccountDB.provider_user_id == google_id
    ).first()

    if account:
        user = account.user

    else:
        user = db.query(UserDB).filter(UserDB.email == email).first()

        if not user:
            user = UserDB(email=email)
            db.add(user)
            db.commit()
            db.refresh(user)

        account = AuthAccountDB(
            user_id=user.id,
            provider="google",
            provider_user_id=google_id
        )

        db.add(account)
        db.commit()

    access_token = create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# USUARIO ACTUAL
@router.get("/me")
def get_me(current_user=Depends(obtener_usuario_actual)):
    return {"email": current_user}