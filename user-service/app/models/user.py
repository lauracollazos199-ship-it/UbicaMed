from pydantic import BaseModel


class UserCreate(BaseModel):
    nombre: str
    email: str
    eps_id: str


class User(BaseModel):
    id: int
    nombre: str
    email: str
    eps_id: str

    model_config = {
        "from_attributes": True
    }