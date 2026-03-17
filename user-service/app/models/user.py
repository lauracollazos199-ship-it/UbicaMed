from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    eps_id: str


class User(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    eps_id: str

    model_config = {
        "from_attributes": True
    }