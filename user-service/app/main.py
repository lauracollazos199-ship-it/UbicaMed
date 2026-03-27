from fastapi import FastAPI
from app.routes.users import router as user_router
from app.database.database import Base, engine
from app.database import models_db
from app.routes import google_login

app = FastAPI()

app.include_router(google_login.router)


Base.metadata.create_all(bind=engine)


app.include_router(user_router)

@app.get("/")
def root():
    return {"mensaje": "User Service funcionando"}