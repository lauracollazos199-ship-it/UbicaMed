from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes.users import router as user_router
from app.database.database import Base, engine
from app.routes import google_login

app = FastAPI()


# MANEJADOR GLOBAL DE ERRORES (TRADUCCIÓN)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    errores = []

    for err in exc.errors():
        campo = err.get("loc")[-1]
        mensaje = err.get("msg")

        # Traducciones
        if "value is not a valid email" in mensaje:
            errores.append("El correo no es válido")
        elif "field required" in mensaje:
            errores.append(f"El campo '{campo}' es obligatorio")
        else:
            errores.append(mensaje)

    return JSONResponse(
        status_code=400,
        content={"detail": errores}
    )


app.include_router(google_login.router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"mensaje": "User Service funcionando"}