from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import DUMMY_HASH, create_access_token, verify_password
from app.db.session import get_db
from app.deps import get_current_user
from app.models import Usuario
from app.schemas.schemas import LoginRequest, LoginResponse, UsuarioOut

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.scalar(select(Usuario).where(Usuario.correo == datos.correo.strip().lower()))
    # Siempre verificamos un hash (aunque el usuario no exista) para no filtrar que correos existen.
    hash_a_verificar = usuario.password_hash if usuario else DUMMY_HASH
    password_ok = verify_password(datos.password, hash_a_verificar)
    if usuario is None or not password_ok or not usuario.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token = create_access_token(usuario.id, usuario.rol, usuario.proveedor_id)
    return LoginResponse(access_token=token, usuario=UsuarioOut.model_validate(usuario))


@router.get("/me", response_model=UsuarioOut)
def me(usuario: Usuario = Depends(get_current_user)):
    return usuario
