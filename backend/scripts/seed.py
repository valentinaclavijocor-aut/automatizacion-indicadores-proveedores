"""Carga datos FICTICIOS de prueba (docs/modelo-datos.md, seccion 6). Es seguro ejecutarlo varias veces.

Uso (desde la carpeta backend/):  python -m scripts.seed
Las contrasenas se leen de variables de entorno (.env); no estan escritas en el codigo.
"""
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models import Indicador, Proveedor, Publicacion, Usuario
# Carga el archivo .env (SEED_* no pasan por la configuracion de la app, asi que se leen aqui).
load_dotenv()

PROVEEDORES = [
    (1, "900000001", "Proveedor Demo A", "contacto.a@demo.com", "proveedor.a@demo.com", "Usuario Demo A"),
    (2, "900000002", "Proveedor Demo B", "contacto.b@demo.com", "proveedor.b@demo.com", "Usuario Demo B"),
    (3, "900000003", "Proveedor Demo C", "contacto.c@demo.com", "proveedor.c@demo.com", "Usuario Demo C"),
]

# (nombre, unidad, {proveedor_id: valor})
INDICADORES = [
    ("Cumplimiento de entregas", "%", {1: 95.5, 2: 88.0, 3: 92.3}),
    ("Calidad de productos", "%", {1: 98.0, 2: 91.5, 3: 96.1}),
    ("Tiempo promedio de entrega", "días", {1: 3.0, 2: 5.5, 3: 4.2}),
]


def requerir(nombre: str) -> str:
    valor = os.getenv(nombre)
    if not valor:
        sys.exit(f"Falta la variable de entorno {nombre}. Revisa tu archivo .env (ver .env.example).")
    return valor


def main() -> None:
    admin_correo = requerir("SEED_ADMIN_EMAIL").strip().lower()
    admin_password = requerir("SEED_ADMIN_PASSWORD")
    demo_password = requerir("SEED_DEMO_PASSWORD")

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if not db.scalar(select(Usuario).where(Usuario.correo == admin_correo)):
            db.add(Usuario(nombre="Administrador Haceb", correo=admin_correo,
                           password_hash=hash_password(admin_password), rol="ADMIN"))
            db.flush()

        for pid, nit, nombre, correo_prov, correo_user, nombre_user in PROVEEDORES:
            if not db.scalar(select(Proveedor).where(Proveedor.nit == nit)):
                db.add(Proveedor(nit=nit, nombre=nombre, correo=correo_prov, activo=True))
                db.flush()
            proveedor = db.scalar(select(Proveedor).where(Proveedor.nit == nit))
            if not db.scalar(select(Usuario).where(Usuario.correo == correo_user)):
                db.add(Usuario(nombre=nombre_user, correo=correo_user,
                               password_hash=hash_password(demo_password), rol="PROVEEDOR",
                               proveedor_id=proveedor.id))

        # 2026-09 ya PUBLICADO (historial) y 2026-10 en BORRADOR (para probar que no se ve).
        for periodo, estado, fecha in (
            ("2026-09", "PUBLICADO", datetime(2026, 10, 21, 14, 30, tzinfo=timezone.utc)),
            ("2026-10", "BORRADOR", None),
        ):
            if not db.scalar(select(Publicacion).where(Publicacion.periodo == periodo)):
                pub = Publicacion(periodo=periodo, estado=estado, fecha_publicacion=fecha)
                db.add(pub)
                db.flush()
                for nombre_ind, unidad, valores in INDICADORES:
                    for prov_nit_idx, valor in valores.items():
                        proveedor = db.scalar(select(Proveedor).where(Proveedor.nit == PROVEEDORES[prov_nit_idx - 1][1]))
                        db.add(Indicador(proveedor_id=proveedor.id, publicacion_id=pub.id,
                                         nombre=nombre_ind, valor=valor, unidad=unidad))
        db.commit()
    print("Datos de prueba cargados correctamente.")


if __name__ == "__main__":
    main()
