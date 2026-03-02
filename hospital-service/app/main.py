from fastapi import FastAPI
from app.routes.hospitals import router as hospital_router
from app.database.database import engine
from app.database.models_db import Base 

app = FastAPI(
    title = "Hospital Service"
)

Base.metadata.create_all(bind=engine)

app.include_router(hospital_router)

@app.get("/")
def root():
    return{"mensaje": "Hospital service funcionando"}


