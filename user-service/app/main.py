from fastapi import FastAPI

from app.routes.users import router as user_router
from app.routes.auth_router import router as auth_router

from app.database.database import Base, engine
from app.database import models_db


app = FastAPI()

# crear tablas
Base.metadata.create_all(bind=engine)

# routers
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"mensaje": "API funcionando"}