"""Modelos SQLAlchemy. Siguen docs/modelo-datos.md."""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nit: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint("rol IN ('ADMIN', 'PROVEEDOR')", name="ck_usuarios_rol"),
        # ADMIN no necesita proveedor; PROVEEDOR debe tenerlo.
        CheckConstraint(
            "(rol = 'ADMIN') OR (rol = 'PROVEEDOR' AND proveedor_id IS NOT NULL)",
            name="ck_usuarios_proveedor_segun_rol",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    proveedor_id: Mapped[int | None] = mapped_column(ForeignKey("proveedores.id"), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    proveedor: Mapped[Proveedor | None] = relationship()


class Publicacion(Base):
    __tablename__ = "publicaciones"
    __table_args__ = (
        CheckConstraint("estado IN ('BORRADOR', 'PUBLICADO')", name="ck_publicaciones_estado"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    periodo: Mapped[str] = mapped_column(String(7), unique=True, nullable=False)  # YYYY-MM
    fecha_publicacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="BORRADOR", nullable=False)


class Indicador(Base):
    __tablename__ = "indicadores"
    __table_args__ = (Index("ix_indicadores_proveedor_publicacion", "proveedor_id", "publicacion_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"), nullable=False)
    publicacion_id: Mapped[int] = mapped_column(ForeignKey("publicaciones.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    unidad: Mapped[str] = mapped_column(String(30), nullable=False)

    publicacion: Mapped[Publicacion] = relationship()


class Notificacion(Base):
    __tablename__ = "notificaciones"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('PENDIENTE', 'ENVIADO', 'FALLIDO')", name="ck_notificaciones_estado"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"), nullable=False)
    publicacion_id: Mapped[int] = mapped_column(ForeignKey("publicaciones.id"), nullable=False)
    correo_destino: Mapped[str] = mapped_column(String(150), nullable=False)
    fecha_envio: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="PENDIENTE", nullable=False)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
