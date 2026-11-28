"""Configuracion de pruebas: SQLite en memoria, sin necesidad de PostgreSQL ni de un .env."""
import os

# Deben definirse ANTES de importar la app (la configuracion se lee al importar).
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "clave-solo-para-pruebas-no-es-un-secreto-real-0123456789"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.db.session import Base, get_db
from app.main import app
from app.models import Indicador, Proveedor, Publicacion, Usuario

PASSWORD_PRUEBA = "ClavePrueba#1"  # solo existe dentro de las pruebas


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def client(db_session):
    def _get_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_db
    # Sin "with": no se dispara el lifespan (que crearia tablas en el engine real).
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def datos(db_session):
    """2 proveedores, 1 admin, 1 usuario por proveedor, una publicacion PUBLICADA y otra en BORRADOR."""
    a = Proveedor(nit="900000001", nombre="Proveedor Demo A", correo="contacto.a@demo.com")
    b = Proveedor(nit="900000002", nombre="Proveedor Demo B", correo="contacto.b@demo.com")
    db_session.add_all([a, b])
    db_session.flush()
    h = hash_password(PASSWORD_PRUEBA)
    db_session.add_all([
        Usuario(nombre="Admin", correo="admin@demo.com", password_hash=h, rol="ADMIN"),
        Usuario(nombre="Usuario A", correo="proveedor.a@demo.com", password_hash=h, rol="PROVEEDOR", proveedor_id=a.id),
        Usuario(nombre="Usuario B", correo="proveedor.b@demo.com", password_hash=h, rol="PROVEEDOR", proveedor_id=b.id),
        Usuario(nombre="Inactivo", correo="inactivo@demo.com", password_hash=h, rol="ADMIN", activo=False),
    ])
    pub_ok = Publicacion(periodo="2026-09", estado="PUBLICADO")
    pub_borrador = Publicacion(periodo="2026-10", estado="BORRADOR")
    db_session.add_all([pub_ok, pub_borrador])
    db_session.flush()
    db_session.add_all([
        Indicador(proveedor_id=a.id, publicacion_id=pub_ok.id, nombre="Cumplimiento de entregas", valor=95.5, unidad="%"),
        Indicador(proveedor_id=b.id, publicacion_id=pub_ok.id, nombre="Cumplimiento de entregas", valor=70.0, unidad="%"),
        Indicador(proveedor_id=a.id, publicacion_id=pub_borrador.id, nombre="Calidad de productos", valor=99.0, unidad="%"),
    ])
    db_session.commit()
    return {"a": a, "b": b, "pub_ok": pub_ok, "pub_borrador": pub_borrador}


def _login(client, correo):
    r = client.post("/api/v1/auth/login", json={"correo": correo, "password": PASSWORD_PRUEBA})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture()
def admin_h(client, datos):
    return _login(client, "admin@demo.com")


@pytest.fixture()
def prov_a_h(client, datos):
    return _login(client, "proveedor.a@demo.com")


@pytest.fixture()
def prov_b_h(client, datos):
    return _login(client, "proveedor.b@demo.com")
