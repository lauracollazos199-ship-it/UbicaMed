from fastapi import FastAPI
from app.routes.gateway_routes import router

app = FastAPI(
    title="API Gateway"
)

app.include_router(router)

@app.get("/")
def root():
    return {"mensaje": "API Gateway funcionando"}