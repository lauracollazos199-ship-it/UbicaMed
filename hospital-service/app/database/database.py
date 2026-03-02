from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:Hospital2026@hospital-service-db.cnasocgwavdn.us-east-2.rds.amazonaws.com:5432/postgres?sslmode=require"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

