import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import require_admin
from app.models import Indicador, Notificacion, Proveedor, Publicacion
from app.schemas.schemas import PublicacionCreate, PublicacionOut
from app.services import notificaciones as servicio_notificaciones

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[PublicacionOut])
def listar_publicaciones(db: Session = Depends(get_db)):
    return db.scalars(select(Publicacion).order_by(Publicacion.periodo.desc())).all()


@router.post("", response_model=PublicacionOut, status_code=status.HTTP_201_CREATED)
def crear_publicacion(datos: PublicacionCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Publicacion).where(Publicacion.periodo == datos.periodo)):
        raise HTTPException(status_code=409, detail="Ya existe una publicación para ese período")
    publicacion = Publicacion(periodo=datos.periodo, estado="BORRADOR")
    db.add(publicacion)
    try:
        db.commit()
    except IntegrityError:  # dos solicitudes simultaneas: la restriccion UNIQUE gana
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe una publicación para ese período")
    db.refresh(publicacion)
    return publicacion


@router.post("/{publicacion_id}/publicar", response_model=PublicacionOut)
def publicar(publicacion_id: int, db: Session = Depends(get_db)):
    # with_for_update bloquea la fila en PostgreSQL: evita publicar dos veces en paralelo.
    publicacion = db.scalar(
        select(Publicacion).where(Publicacion.id == publicacion_id).with_for_update()
    )
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    if publicacion.estado != "BORRADOR":
        raise HTTPException(status_code=409, detail="La publicación ya está publicada")

    total = db.scalar(select(func.count()).select_from(Indicador).where(Indicador.publicacion_id == publicacion.id))
    if not total:
        raise HTTPException(status_code=409, detail="La publicación no tiene indicadores")

    publicacion.estado = "PUBLICADO"
    publicacion.fecha_publicacion = datetime.now(timezone.utc)

    # Una notificacion PENDIENTE por cada proveedor incluido en la publicacion.
    proveedores = db.scalars(
        select(Proveedor)
        .where(Proveedor.id.in_(select(Indicador.proveedor_id).where(Indicador.publicacion_id == publicacion.id)))
        .order_by(Proveedor.id)
    ).all()
    for proveedor in proveedores:
        db.add(
            Notificacion(
                proveedor_id=proveedor.id,
                publicacion_id=publicacion.id,
                correo_destino=proveedor.correo,
                estado="PENDIENTE",
            )
        )
    db.commit()
    db.refresh(publicacion)

    # Integracion con el modulo de Andres. Un fallo aqui NO debe deshacer la publicacion.
    try:
        servicio_notificaciones.notificar_publicacion(db, publicacion.id)
    except Exception:
        logger.exception("Fallo el hook de notificaciones para la publicacion %s", publicacion.id)

    return publicacion
