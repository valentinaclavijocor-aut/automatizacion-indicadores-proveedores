"""PUNTO DE INTEGRACION con el modulo de notificaciones (responsable: Andres).

El backend de la API NO envia correos. Solo llama a estas dos funciones:

1. notificar_publicacion(...)  -> se invoca justo despues de publicar un periodo.
   Ya existen los registros `notificaciones` en estado PENDIENTE. Hoy no hace nada.

2. enviar_notificacion(...)    -> se invoca desde POST /api/v1/notificaciones/{id}/enviar.
   Andres debe implementarla: enviar el correo (o simularlo), y actualizar en la
   notificacion `estado` (ENVIADO o FALLIDO), `fecha_envio` y `error`.
   Reglas del contrato: el correo NO incluye valores de indicadores, solo avisa que
   hay nuevos resultados. Un fallo se registra como FALLIDO (no lanza excepcion).

Mientras Andres no la implemente, el endpoint /enviar responde HTTP 501.
"""
from sqlalchemy.orm import Session

from app.models import Notificacion


def notificar_publicacion(db: Session, publicacion_id: int) -> None:
    """Hook posterior a la publicacion. Pendiente de implementar por Andres (puede dejarse vacio)."""
    return None


def enviar_notificacion(db: Session, notificacion: Notificacion) -> Notificacion:
    """Envia una notificacion PENDIENTE o FALLIDA y actualiza su estado.

    TODO (Andres): implementar el envio. Debe hacer db.commit() y devolver la notificacion actualizada.
    """
    raise NotImplementedError("El envio de correos lo implementa el modulo de notificaciones")
