from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import require_admin
from app.models import Notificacion
from app.schemas.schemas import NotificacionEnvioOut, NotificacionOut
from app.services import notificaciones as servicio_notificaciones

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[NotificacionOut])
def listar_notificaciones(db: Session = Depends(get_db)):
    return db.scalars(select(Notificacion).order_by(Notificacion.id)).all()


@router.post("/{notificacion_id}/enviar", response_model=NotificacionEnvioOut)
def enviar(notificacion_id: int, db: Session = Depends(get_db)):
    notificacion = db.get(Notificacion, notificacion_id)
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    if notificacion.estado == "ENVIADO":
        raise HTTPException(status_code=409, detail="La notificación ya fue enviada")
    try:
        return servicio_notificaciones.enviar_notificacion(db, notificacion)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="El envío de correos aún no está implementado")
