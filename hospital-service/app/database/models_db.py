from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class HospitalDB(Base):
    __tablename__ = "hospitales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    latitud = Column(Float)
    longitud = Column(Float)


class EPSDB(Base):
    __tablename__ = "eps"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)


class ConvenioDB(Base):
    __tablename__ = "convenios"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitales.id"))
    eps_id = Column(Integer, ForeignKey("eps.id"))