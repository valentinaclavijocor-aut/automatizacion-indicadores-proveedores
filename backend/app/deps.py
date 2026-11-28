"""Dependencias de autenticacion y autorizacion por rol."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models import Usuario

# auto_error=False para responder nosotros con 401 (el contrato lo exige) cuando falta el token.
bearer_scheme = HTTPBearer(auto_error=False)


def _no_autenticado() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """Valida el token y carga el usuario desde la base de datos.

    Rol, proveedor_id y estado activo se toman SIEMPRE de la base de datos, no del token,
    para que un cambio de rol o una desactivacion tenga efecto inmediato.
    """
    if credentials is None:
        raise _no_autenticado()
    claims = decode_access_token(credentials.credentials)
    if claims is None:
        raise _no_autenticado()
    try:
        usuario_id = int(claims["sub"])
    except (KeyError, ValueError):
        raise _no_autenticado()
    usuario = db.get(Usuario, usuario_id)
    if usuario is None or not usuario.activo:
        raise _no_autenticado()
    return usuario


def require_role(rol: str):
    """Fabrica de dependencias: exige un rol concreto (403 si el usuario tiene otro)."""

    def verificar(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.rol != rol:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para esta operación")
        return usuario

    return verificar


require_admin = require_role("ADMIN")
require_proveedor = require_role("PROVEEDOR")
