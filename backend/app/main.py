"""Punto de entrada de la API. Ejecutar con:  uvicorn app.main:app --reload"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (registra las tablas en Base.metadata)
from app.core.config import get_settings
from app.db.session import Base, engine
from app.routes import auth, indicadores, notificaciones, portal, proveedores, publicaciones

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # MVP: crea las tablas si no existen. (Para cambios de esquema en produccion se usaria Alembic.)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Indicadores de Proveedores - Haceb (MVP)",
    description="Backend del proyecto EstudIA. Contrato: docs/contrato-api.md",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    auth.router,
    proveedores.router,
    publicaciones.router,
    indicadores.router,
    portal.router,
    notificaciones.router,
):
    app.include_router(router, prefix=API_PREFIX)


@app.get("/", include_in_schema=False)
def raiz():
    return {"servicio": "API Indicadores Haceb", "docs": "/docs"}
