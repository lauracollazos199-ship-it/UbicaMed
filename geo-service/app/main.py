from fastapi import FastAPI
from app.routes.geo_routes import router as geo_router

app = FastAPI()

app.include_router(geo_router)

@app.get("/")
def root():
    return {"mensaje": "Geo service funcionando"}