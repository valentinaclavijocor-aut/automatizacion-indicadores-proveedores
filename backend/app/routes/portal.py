"""Portal de proveedores. El proveedor_id SIEMPRE sale del usuario autenticado, nunca de la solicitud."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import require_proveedor
from app.models import Indicador, Publicacion, Usuario
from app.schemas.schemas import PERIODO_REGEX, MiIndicadorOut, MiPeriodoOut

router = APIRouter(tags=["Portal de proveedores"])


@router.get("/mis-indicadores", response_model=list[MiIndicadorOut])
def mis_indicadores(
    periodo: str | None = Query(default=None, pattern=PERIODO_REGEX, examples=["2026-10"]),
    usuario: Usuario = Depends(require_proveedor),
    db: Session = Depends(get_db),
):
    consulta = (
        select(Indicador, Publicacion.periodo)
        .join(Publicacion, Indicador.publicacion_id == Publicacion.id)
        .where(Indicador.proveedor_id == usuario.proveedor_id)  # aislamiento entre proveedores
        .where(Publicacion.estado == "PUBLICADO")  # los BORRADOR nunca se ven
        .order_by(Publicacion.periodo.desc(), Indicador.id)
    )
    if periodo is not None:
        consulta = consulta.where(Publicacion.periodo == periodo)
    return [
        MiIndicadorOut(id=i.id, periodo=per, nombre=i.nombre, valor=float(i.valor), unidad=i.unidad)
        for i, per in db.execute(consulta).all()
    ]


@router.get("/mis-periodos", response_model=list[MiPeriodoOut])
def mis_periodos(usuario: Usuario = Depends(require_proveedor), db: Session = Depends(get_db)):
    consulta = (
        select(Publicacion.periodo, Publicacion.fecha_publicacion)
        .where(Publicacion.estado == "PUBLICADO")
        .where(
            Publicacion.id.in_(
                select(Indicador.publicacion_id).where(Indicador.proveedor_id == usuario.proveedor_id)
            )
        )
        .order_by(Publicacion.periodo.desc())
    )
    return [MiPeriodoOut(periodo=p, fecha_publicacion=f) for p, f in db.execute(consulta).all()]
