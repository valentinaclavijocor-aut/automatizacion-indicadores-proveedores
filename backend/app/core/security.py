"""Hash de contrasenas (bcrypt) y creacion/validacion de tokens JWT."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8")[:72], password_hash.encode("utf-8"))
    except ValueError:
        return False


# Hash de relleno: permite gastar el mismo tiempo cuando el correo no existe,
# para no revelar que correos estan registrados.
DUMMY_HASH = hash_password("relleno-no-se-usa")


def create_access_token(usuario_id: int, rol: str, proveedor_id: int | None) -> str:
    settings = get_settings()
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    claims = {"sub": str(usuario_id), "rol": rol, "proveedor_id": proveedor_id, "exp": expira}
    return jwt.encode(claims, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict | None:
    """Devuelve los claims o None si el token es invalido o esta vencido."""
    settings = get_settings()
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None
