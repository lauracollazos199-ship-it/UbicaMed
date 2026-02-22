from fastapi import FastAPI
from app.routes.hospitals import router as hospital_router

app = FastAPI()

app.include_router(hospital_router)

@app.get("/")
def root():
    return{"mensaje": "Hospital service funcionando"}
