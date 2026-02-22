from app.models.hospital import Hospital

hospitales = [
    Hospital(
        id=1,
        nombre="Hospital Central",
        eps=["Sura", "Sanitas"],
        latitud=4.65,
        longitud=-74.05
    ),
    Hospital(
        id=2,
        nombre="Clínica Norte",
        eps=["Nueva EPS", "Sura"],
        latitud=4.70,
        longitud=-74.03
    ),
    Hospital(
        id=3,
        nombre="Hospital San José",
        eps=["Sanitas"],
        latitud=4.60,
        longitud=-74.08
    )
]


def obtener_hospitales():
    return hospitales


def obtener_hospitales_por_eps(eps: str):

    resultado = []

    for hospital in hospitales:
        if eps in hospital.eps:
            resultado.append(hospital)

    if len(resultado) == 0:
        raise ValueError("No hay hospitales para esa EPS")

    return resultado


def crear_hospital(hospital: Hospital):

    for h in hospitales:
        if h.id == hospital.id:
            raise ValueError("El hospital ya existe")

    hospitales.append(hospital)

    return hospital


def eliminar_hospital(hospital_id: int):

    for hospital in hospitales[:]:
        if hospital.id == hospital_id:
            hospitales.remove(hospital)
            return True

    raise ValueError("Hospital no encontrado")


def obtener_hospital_por_id(hospital_id: int):

    for hospital in hospitales:
        if hospital.id == hospital_id:
            return hospital

    raise ValueError("Hospital no encontrado")