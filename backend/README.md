# Backend – API de Indicadores de Proveedores (Haceb MVP)

API REST con **FastAPI + SQLAlchemy + PostgreSQL** y autenticación **JWT**.
Implementa el contrato definido en [`docs/contrato-api.md`](../docs/contrato-api.md).

## Estructura

```
backend/
├── app/
│   ├── main.py            # Arranque de FastAPI, CORS y registro de rutas (/api/v1)
│   ├── deps.py            # Autenticación (JWT) y autorización por rol (ADMIN / PROVEEDOR)
│   ├── core/              # config.py (variables de entorno) y security.py (bcrypt + JWT)
│   ├── db/session.py      # Conexión a PostgreSQL y sesión por solicitud
│   ├── models/            # Tablas SQLAlchemy (docs/modelo-datos.md)
│   ├── schemas/           # Esquemas Pydantic de entrada/salida (JSON del contrato)
│   ├── routes/            # auth, proveedores, publicaciones, indicadores, portal, notificaciones
│   └── services/notificaciones.py   # Punto de integración con el módulo de Andrés
├── scripts/seed.py        # Datos ficticios de prueba
├── tests/                 # Pruebas con pytest (SQLite en memoria)
├── .env.example           # Plantilla de variables de entorno
└── docker-compose.yml     # PostgreSQL local opcional
```

## 1. Instalación

Requisitos: Python 3.11 o superior.

```bash
cd backend
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Windows (cmd):         .venv\Scripts\activate.bat
# macOS / Linux:         source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 2. Configuración

1. Copia la plantilla: `cp .env.example .env` (en Windows: `copy .env.example .env`).
2. Edita `.env` y reemplaza **todos** los valores `cambia_...` por los tuyos.
   - `SECRET_KEY`: genera una con `python -c "import secrets; print(secrets.token_hex(32))"`.
   - `DATABASE_URL`: usuario, clave y base de tu PostgreSQL.
3. **Nunca subas `.env` a GitHub** (ya está en `.gitignore`).

### PostgreSQL

**Opción A – Docker** (si lo tienes instalado): con `POSTGRES_PASSWORD` definido en tu `.env`:

```bash
docker compose up -d
```

**Opción B – PostgreSQL instalado en tu equipo**: crea un usuario y una base y ponlos en `DATABASE_URL`:

```sql
CREATE USER haceb_user WITH PASSWORD 'tu_clave';
CREATE DATABASE haceb_indicadores OWNER haceb_user;
```

Las tablas se crean automáticamente al iniciar la API.

## 3. Datos de prueba (ficticios)

```bash
python -m scripts.seed
```

Crea 3 proveedores demo, 1 ADMIN, 1 usuario por proveedor, el período `2026-09` (PUBLICADO)
y `2026-10` (BORRADOR). Las contraseñas salen de `SEED_ADMIN_PASSWORD` y `SEED_DEMO_PASSWORD`
de tu `.env`. Es seguro ejecutarlo varias veces.

| Usuario | Correo | Rol |
|---|---|---|
| Administrador Haceb | el de `SEED_ADMIN_EMAIL` (por defecto `admin@demo.com`) | ADMIN |
| Usuario Demo A / B / C | `proveedor.a@demo.com`, `proveedor.b@demo.com`, `proveedor.c@demo.com` | PROVEEDOR |

## 4. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000/api/v1
- **Swagger (documentación interactiva): http://localhost:8000/docs**
- En Swagger: `POST /auth/login` → copia el `access_token` → botón **Authorize** → pega el token.

## 5. Pruebas

```bash
python -m pytest
```

No necesitan PostgreSQL ni `.env`: usan SQLite en memoria y una clave de prueba propia.
Cubren: login, 401 sin token, 403 por rol, aislamiento entre proveedores, borradores ocultos,
publicación (409 al duplicar, notificaciones PENDIENTE) y validaciones (404/409/422).

## Decisiones técnicas

- **Autorización siempre en el backend.** `proveedor_id`, rol y estado activo se leen de la base
  de datos en cada solicitud (no se confía en el token), así que desactivar un usuario o cambiarle el rol
  surte efecto de inmediato.
- **Aislamiento entre proveedores.** `/mis-indicadores` y `/mis-periodos` filtran por el `proveedor_id`
  del usuario autenticado; ningún parámetro del cliente puede cambiarlo. Solo se leen publicaciones `PUBLICADO`.
- **401 vs 403.** Sin token o token inválido → 401. Token válido pero rol incorrecto → 403.
- **Contraseñas** con bcrypt; el login tarda lo mismo si el correo no existe (no revela qué correos están registrados).
- **Sin secretos en el código.** `SECRET_KEY` y `DATABASE_URL` no tienen valor por defecto: sin `.env` la app no arranca.
- **Tablas con `create_all`** (suficiente para el MVP). Si el esquema cambia en el futuro, conviene migrar a Alembic.
- **Publicar** bloquea la fila de la publicación (`FOR UPDATE`) para evitar doble publicación simultánea y crea una
  notificación `PENDIENTE` por cada proveedor con indicadores en ese período.

## Integración con notificaciones (Andrés)

El backend **no envía correos**. El archivo `app/services/notificaciones.py` define dos funciones:

| Función | Cuándo se llama | Estado |
|---|---|---|
| `notificar_publicacion(db, publicacion_id)` | Justo después de publicar (las notificaciones PENDIENTE ya existen) | Vacía; Andrés decide si la usa |
| `enviar_notificacion(db, notificacion)` | Desde `POST /api/v1/notificaciones/{id}/enviar` | **Pendiente (Andrés)**: enviar o simular el correo y actualizar `estado`, `fecha_envio` y `error` |

Mientras no se implemente `enviar_notificacion`, ese endpoint responde **HTTP 501**. El contrato exige
que el correo no incluya valores de indicadores y que los fallos se registren como `FALLIDO`.

## Decisiones pendientes de confirmar con el equipo

1. **Publicar sin indicadores** devuelve **409** (el contrato exige "al menos un indicador" pero no indica el código).
2. `GET /mis-indicadores` ignora un `proveedor_id` enviado por el cliente (el contrato dice que no debe usarse).
3. Un ADMIN que llame a `/mis-indicadores` o `/mis-periodos` recibe **403** (son endpoints exclusivos de PROVEEDOR).
