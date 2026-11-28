from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import require_admin
from app.models import Indicador, Proveedor, Publicacion
from app.schemas.schemas import IndicadorCreate, IndicadorOut

router = APIRouter(prefix="/indicadores", tags=["Indicadores (admin)"], dependencies=[Depends(require_admin)])


@router.post("", response_model=IndicadorOut, status_code=status.HTTP_201_CREATED)
def registrar_indicador(datos: IndicadorCreate, db: Session = Depends(get_db)):
    if db.get(Proveedor, datos.proveedor_id) is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    publicacion = db.get(Publicacion, datos.publicacion_id)
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    if publicacion.estado != "BORRADOR":
        raise HTTPException(status_code=409, detail="Solo se pueden agregar indicadores a publicaciones en BORRADOR")

    indicador = Indicador(**datos.model_dump())
    db.add(indicador)
    db.commit()
    db.refresh(indicador)
    return indicador


@router.get("", response_model=list[IndicadorOut])
def listar_indicadores(
    proveedor_id: int | None = None,
    publicacion_id: int | None = None,
    db: Session = Depends(get_db),
):
    consulta = select(Indicador).order_by(Indicador.id)
    if proveedor_id is not None:
        consulta = consulta.where(Indicador.proveedor_id == proveedor_id)
    if publicacion_id is not None:
        consulta = consulta.where(Indicador.publicacion_id == publicacion_id)
    return db.scalars(consulta).all()
