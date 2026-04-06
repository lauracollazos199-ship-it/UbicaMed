import re
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator



def validar_password_rules(v: str):
    if len(v) > 64:
        raise ValueError("La contraseña no puede tener más de 64 caracteres")

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

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validar_password(cls, v):
        return validar_password_rules(v)

class UserCreate(BaseModel):

    nombre: str
    email: EmailStr
    password: str


    @field_validator("password")
    @classmethod
    def validar_password(cls, v):
        if v is None:
            return v
        return validar_password_rules(v)


class User(BaseModel):
    id: int
    nombre: str
    email: str
    password: str
   
  
    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

    @field_validator("password")
    @classmethod
    def validar_password(cls, v):
        return UserUpdate.validar_password(v)