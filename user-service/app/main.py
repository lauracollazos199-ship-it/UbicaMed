from fastapi import FastAPI
from app.routes.users import router as user_router

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def root():
    return {"mensaje": "User Service funcionando"}