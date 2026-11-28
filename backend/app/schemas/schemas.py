"""Esquemas Pydantic (entrada y salida). Siguen docs/contrato-api.md."""
from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

PERIODO_REGEX = r"^\d{4}-(0[1-9]|1[0-2])$"


def _a_utc(valor: datetime | None) -> datetime | None:
    """SQLite devuelve fechas sin zona horaria; las tratamos como UTC para responder ISO 8601 con 'Z'."""
    if valor is not None and valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor


class _Out(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Autenticacion ----------
class LoginRequest(BaseModel):
    correo: Annotated[str, StringConstraints(min_length=3, max_length=150)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=200)]


class UsuarioOut(_Out):
    id: int
    nombre: str
    correo: str
    rol: str
    proveedor_id: int | None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut


# ---------- Proveedores ----------
class ProveedorOut(_Out):
    id: int
    nit: str
    nombre: str
    correo: str
    activo: bool


# ---------- Publicaciones ----------
class PublicacionCreate(BaseModel):
    periodo: str = Field(pattern=PERIODO_REGEX, examples=["2026-10"])


class PublicacionOut(_Out):
    id: int
    periodo: str
    fecha_publicacion: datetime | None
    estado: str

    _utc = field_validator("fecha_publicacion")(_a_utc)


# ---------- Indicadores ----------
class IndicadorCreate(BaseModel):
    proveedor_id: int
    publicacion_id: int
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
    valor: float = Field(allow_inf_nan=False, ge=-9999999999.99, le=9999999999.99)
    unidad: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=30)]


class IndicadorOut(_Out):
    id: int
    proveedor_id: int
    publicacion_id: int
    nombre: str
    valor: float
    unidad: str


# ---------- Portal de proveedores ----------
class MiIndicadorOut(BaseModel):
    id: int
    periodo: str
    nombre: str
    valor: float
    unidad: str


class MiPeriodoOut(BaseModel):
    periodo: str
    fecha_publicacion: datetime | None

    _utc = field_validator("fecha_publicacion")(_a_utc)


# ---------- Notificaciones ----------
class NotificacionOut(_Out):
    id: int
    proveedor_id: int
    publicacion_id: int
    correo_destino: str
    fecha_envio: datetime | None
    estado: str
    error: str | None

    _utc = field_validator("fecha_envio")(_a_utc)


class NotificacionEnvioOut(_Out):
    id: int
    estado: str
    fecha_envio: datetime | None
    error: str | None

    _utc = field_validator("fecha_envio")(_a_utc)
