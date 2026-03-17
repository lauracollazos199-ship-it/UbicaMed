import pandas as pd
from sqlalchemy.orm import Session
from app.database.database import engine
from app.database.models_db import HospitalDB, EPSDB, ConvenioDB

# leer archivos CSV
hospitales = pd.read_csv("hospitales.csv", sep=";")
eps = pd.read_csv("eps.csv", sep=";")
convenios = pd.read_csv("convenios.csv", sep=";")

# limpiar nombres de columnas
hospitales.columns = hospitales.columns.str.strip()
eps.columns = eps.columns.str.strip()
convenios.columns = convenios.columns.str.strip()

# convertir IDs a enteros
hospitales["id"] = hospitales["id"].astype(int)
eps["id"] = eps["id"].astype(int)
convenios["hospital_id"] = convenios["hospital_id"].astype(int)
convenios["eps_id"] = convenios["eps_id"].astype(int)

# crear sesión
session = Session(bind=engine)

# limpiar tablas para evitar duplicados
session.query(ConvenioDB).delete()
session.query(HospitalDB).delete()
session.query(EPSDB).delete()
session.commit()

# cargar hospitales
for _, row in hospitales.iterrows():
    hospital = HospitalDB(
        id=int(row["id"]),
        nombre=row["nombre"],
        direccion=row["direccion"],
        latitud=float(row["latitud"]),
        longitud=float(row["longitud"])
    )
    session.add(hospital)

session.commit()

# cargar EPS
for _, row in eps.iterrows():
    e = EPSDB(
        id=int(row["id"]),
        nombre=row["nombre"]
    )
    session.add(e)

session.commit()

# cargar convenios
for _, row in convenios.iterrows():
    convenio = ConvenioDB(
        hospital_id=int(row["hospital_id"]),
        eps_id=int(row["eps_id"])
    )
    session.add(convenio)

session.commit()

session.close()

print("Datos cargados correctamente")