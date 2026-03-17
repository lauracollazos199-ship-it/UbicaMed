from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) 
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True)

    eps = Column(String, ForeignKey("eps.id"))  

    eps = relationship("EPSDB")


