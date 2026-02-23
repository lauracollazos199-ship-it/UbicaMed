from fastapi import FastAPI
from app.routes.geo_routes import router

app = FastAPI(
    title="Geo service"
)

app.include_router(router)