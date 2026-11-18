
# Contrato de API - MVP Haceb

## 1. Objetivo

Definir los endpoints, formatos JSON y permisos de la API que conectará los portales React con el backend FastAPI.

Este documento es el contrato compartido entre los integrantes del equipo.

## 2. Configuración general

- Framework: FastAPI.
- Formato de intercambio: JSON.
- Prefijo de rutas: `/api/v1`.
- Documentación interactiva: `/docs`.
- Identificadores: números enteros.
- Fechas: formato ISO 8601.
- Períodos: formato `YYYY-MM`.
- Autenticación: token Bearer JWT para el MVP.

El frontend enviará el token mediante:

`Authorization: Bearer <token>`

El backend validará la identidad, el rol y el estado activo del usuario.

## 3. Roles

### ADMIN
Puede:
- Consultar proveedores.
- Crear publicaciones mensuales.
- Registrar indicadores.
- Publicar períodos.
- Consultar indicadores de cualquier proveedor.
- Consultar el estado de las notificaciones.

### PROVEEDOR
Puede:
- Iniciar sesión.
- Consultar su perfil.
- Consultar exclusivamente sus indicadores publicados.
- Consultar sus períodos históricos.

No puede modificar indicadores ni consultar información de otros proveedores.

## 4. Autenticación

### POST /api/v1/auth/login

Acceso público.

Solicitud:

```json
{
  "correo": "proveedor.a@demo.com",
  "password": "Demo123!"
}
```

Respuesta 200:

```json
{
  "access_token": "token_jwt_de_ejemplo",
  "token_type": "bearer",
  "usuario": {
    "id": 2,
    "nombre": "Usuario Demo A",
    "correo": "proveedor.a@demo.com",
    "rol": "PROVEEDOR",
    "proveedor_id": 1
  }
}
```

Credenciales inválidas: HTTP 401.

### GET /api/v1/auth/me

Requiere autenticación.

Respuesta 200:

```json
{
  "id": 2,
  "nombre": "Usuario Demo A",
  "correo": "proveedor.a@demo.com",
  "rol": "PROVEEDOR",
  "proveedor_id": 1
}
```

## 5. Proveedores

### GET /api/v1/proveedores

Permiso: ADMIN.

Respuesta 200:

```json
[
  {
    "id": 1,
    "nit": "900000001",
    "nombre": "Proveedor Demo A",
    "correo": "contacto.a@demo.com",
    "activo": true
  }
]
```

### GET /api/v1/proveedores/{proveedor_id}

Permiso: ADMIN.

Devuelve el proveedor solicitado.

Si no existe: HTTP 404.

## 6. Publicaciones

### GET /api/v1/publicaciones

Permiso: ADMIN.

Respuesta 200:

```json
[
  {
    "id": 1,
    "periodo": "2026-10",
    "fecha_publicacion": null,
    "estado": "BORRADOR"
  }
]
```

### POST /api/v1/publicaciones

Permiso: ADMIN.

Solicitud:

```json
{
  "periodo": "2026-10"
}
```

Respuesta 201:

```json
{
  "id": 1,
  "periodo": "2026-10",
  "fecha_publicacion": null,
  "estado": "BORRADOR"
}
```

Un período duplicado devuelve HTTP 409.

### POST /api/v1/publicaciones/{publicacion_id}/publicar

Permiso: ADMIN.

Cambia el estado de BORRADOR a PUBLICADO.

Respuesta 200:

```json
{
  "id": 1,
  "periodo": "2026-10",
  "fecha_publicacion": "2026-11-21T14:30:00Z",
  "estado": "PUBLICADO"
}
```

Reglas:
- La publicación debe existir.
- Debe estar en estado BORRADOR.
- Debe tener al menos un indicador.
- Publicar dos veces devuelve HTTP 409.
- Al publicarse, se generan registros de notificación PENDIENTE para los proveedores incluidos.

## 7. Indicadores administrativos

### POST /api/v1/indicadores

Permiso: ADMIN.

Solicitud:

```json
{
  "proveedor_id": 1,
  "publicacion_id": 1,
  "nombre": "Cumplimiento de entregas",
  "valor": 95.5,
  "unidad": "%"
}
```

Respuesta 201:

```json
{
  "id": 1,
  "proveedor_id": 1,
  "publicacion_id": 1,
  "nombre": "Cumplimiento de entregas",
  "valor": 95.5,
  "unidad": "%"
}
```

Reglas:
- El proveedor y la publicación deben existir.
- Solo se agregan indicadores a publicaciones BORRADOR.
- Los datos inválidos devuelven HTTP 422.

### GET /api/v1/indicadores?proveedor_id=1&publicacion_id=1

Permiso: ADMIN.

Devuelve los indicadores que coincidan con los filtros.

Ambos filtros son opcionales.

Respuesta 200:

```json
[
  {
    "id": 1,
    "proveedor_id": 1,
    "publicacion_id": 1,
    "nombre": "Cumplimiento de entregas",
    "valor": 95.5,
    "unidad": "%"
  }
]
```

## 8. Portal de proveedores

Estos endpoints utilizan el proveedor_id del usuario autenticado.

El frontend no debe enviar un proveedor_id para determinar qué información puede consultar.

### GET /api/v1/mis-indicadores

Permiso: PROVEEDOR.

Parámetro opcional: `periodo=2026-10`.

Respuesta 200:

```json
[
  {
    "id": 1,
    "periodo": "2026-10",
    "nombre": "Cumplimiento de entregas",
    "valor": 95.5,
    "unidad": "%"
  },
  {
    "id": 2,
    "periodo": "2026-10",
    "nombre": "Calidad de productos",
    "valor": 98.0,
    "unidad": "%"
  }
]
```

Reglas:
- Solo devuelve indicadores del proveedor autenticado.
- Solo devuelve publicaciones PUBLICADO.
- Sin resultados devuelve una lista vacía.

### GET /api/v1/mis-periodos

Permiso: PROVEEDOR.

Respuesta 200:

```json
[
  {
    "periodo": "2026-10",
    "fecha_publicacion": "2026-11-21T14:30:00Z"
  },
  {
    "periodo": "2026-09",
    "fecha_publicacion": "2026-10-21T14:30:00Z"
  }
]
```

Solo devuelve períodos publicados que contengan indicadores del proveedor autenticado.

## 9. Notificaciones

### GET /api/v1/notificaciones

Permiso: ADMIN.

Respuesta 200:

```json
[
  {
    "id": 1,
    "proveedor_id": 1,
    "publicacion_id": 1,
    "correo_destino": "contacto.a@demo.com",
    "fecha_envio": null,
    "estado": "PENDIENTE",
    "error": null
  }
]
```

### POST /api/v1/notificaciones/{notificacion_id}/enviar

Permiso: ADMIN.

Intenta enviar una notificación pendiente o fallida.

Respuesta 200:

```json
{
  "id": 1,
  "estado": "ENVIADO",
  "fecha_envio": "2026-11-21T14:35:00Z",
  "error": null
}
```

Reglas:
- El correo no incluye valores de indicadores.
- El correo informa que hay nuevos resultados disponibles.
- Los errores se registran como FALLIDO.
- El envío se realizará inicialmente con un proveedor de correo de prueba o simulación.
- No se reenvían automáticamente notificaciones ya ENVIADO.

## 10. Errores HTTP

| Código | Significado |
|---|---|
| 200 | Consulta u operación exitosa |
| 201 | Registro creado |
| 401 | No autenticado o credenciales inválidas |
| 403 | Usuario sin permisos |
| 404 | Recurso inexistente |
| 409 | Conflicto con el estado o duplicado |
| 422 | Datos de entrada inválidos |
| 500 | Error inesperado del servidor |

Formato de error propio del negocio:

```json
{
  "detail": "La publicación ya está publicada"
}
```

Los errores de validación 422 pueden utilizar el formato estándar de FastAPI.

## 11. Reglas de integración

- Todos los endpoints se implementarán bajo `/api/v1`.
- Los nombres de campos JSON se escribirán en `snake_case`.
- Los roles serán exactamente `ADMIN` y `PROVEEDOR`.
- Los estados de publicación serán `BORRADOR` y `PUBLICADO`.
- Los estados de notificación serán `PENDIENTE`, `ENVIADO` y `FALLIDO`.
- React no accederá directamente a PostgreSQL.
- El backend verificará los permisos en cada endpoint.
- Las contraseñas y claves secretas no se subirán al repositorio.
- Las rutas protegidas devolverán 401 si no hay autenticación y 403 si el rol no tiene permiso.

## 12. Pruebas mínimas

- [ ] Un ADMIN puede consultar proveedores.
- [ ] Un ADMIN puede crear una publicación.
- [ ] Un ADMIN puede registrar indicadores.
- [ ] Un ADMIN puede publicar un período.
- [ ] Un PROVEEDOR puede iniciar sesión.
- [ ] Un PROVEEDOR puede consultar sus indicadores publicados.
- [ ] Un PROVEEDOR no puede consultar indicadores ajenos.
- [ ] Un PROVEEDOR no puede utilizar endpoints administrativos.
- [ ] Los indicadores en BORRADOR no aparecen en el portal.
- [ ] La publicación genera notificaciones pendientes.
- [ ] Los errores de envío quedan registrados.

## 13. Alcance

Este contrato define el comportamiento esperado del MVP.

No significa que los endpoints ya estén implementados.

Las funcionalidades se desarrollarán mediante Issues y Pull Requests durante las sesiones de trabajo del equipo.
