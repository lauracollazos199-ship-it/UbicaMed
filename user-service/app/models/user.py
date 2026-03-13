from pydantic import BaseModel

class User(BaseModel):
    nombre: str
    email: str
