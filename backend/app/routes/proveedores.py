from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import require_admin
from app.models import Proveedor
from app.schemas.schemas import ProveedorOut

router = APIRouter(prefix="/proveedores", tags=["Proveedores"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[ProveedorOut])
def listar_proveedores(db: Session = Depends(get_db)):
    return db.scalars(select(Proveedor).order_by(Proveedor.id)).all()


@router.get("/{proveedor_id}", response_model=ProveedorOut)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = db.get(Proveedor, proveedor_id)
    if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor
