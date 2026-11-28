"""Conexion a PostgreSQL con SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """Dependencia de FastAPI: una sesion por solicitud, siempre cerrada al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
