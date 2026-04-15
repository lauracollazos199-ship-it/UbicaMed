from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.gateway_routes import router

app = FastAPI(
    title="API Gateway"
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
    "https://ubicamed.duckdns.org"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def root():
    return {"mensaje": "API Gateway funcionando"}