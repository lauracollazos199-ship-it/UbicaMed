from pydantic import BaseModel, EmailStr, field_validator
import re
from datetime import date


class UserCreate(BaseModel):

    nombre: str
    email: EmailStr
    password: str
    fecha_nacimiento: date
    eps_id: int

    @field_validator("password")
    def validar_password(cls, v):

        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe tener una mayúscula")

        if not re.search(r"[a-z]", v):
            raise ValueError("Debe tener una minúscula")

        if not re.search(r"[0-9]", v):
            raise ValueError("Debe tener un número")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Debe tener un carácter especial")

        return v


class User(BaseModel):
    id: int
    nombre: str
    email: str
    eps_id: int
    password: str
    fecha_nacimiento: date
  
    model_config = {
        "from_attributes": True
    }