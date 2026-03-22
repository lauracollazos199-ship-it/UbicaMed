from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database.database import Base


class UserDB(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String)
    email = Column(String, unique=True, index=True)

    password = Column(String, nullable=True)

    fecha_nacimiento = Column(Date)

    eps_id = Column(Integer)

    # relación con cuentas externas
    auth_accounts = relationship("AuthAccountDB", back_populates="user")

    

class AuthAccountDB(Base):

    __tablename__ = "auth_accounts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    provider = Column(String)  # google

    provider_user_id = Column(String)  # id único de google

    user = relationship("UserDB", back_populates="auth_accounts")

   


