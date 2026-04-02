from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class HospitalDB(Base):
    __tablename__ = "hospitales"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)

    # Relación principal que escribe en convenios
    convenios = relationship(
        "ConvenioDB",
        back_populates="hospital",
        cascade="all, delete"
    )

    # Relación derivada, solo lectura
    eps = relationship(
        "EPSDB",
        secondary="convenios",
        back_populates="hospitales",
        viewonly=True
    )


class EPSDB(Base):
    __tablename__ = "eps"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    # Relación principal que escribe en convenios
    convenios = relationship(
        "ConvenioDB",
        back_populates="eps"
    )

    # Relación derivada, solo lectura
    hospitales = relationship(
        "HospitalDB",
        secondary="convenios",
        back_populates="eps",
        viewonly=True
    )


class ConvenioDB(Base):
    __tablename__ = "convenios"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitales.id"), primary_key=True)
    eps_id = Column(Integer, ForeignKey("eps.id"), primary_key=True)

    hospital = relationship("HospitalDB", back_populates="convenios")
    eps = relationship("EPSDB", back_populates="convenios")