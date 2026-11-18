
# Modelo de datos - MVP Haceb

## 1. Objetivo

Definir las entidades, campos y relaciones de la plataforma de indicadores para proveedores nacionales de Haceb.

Este documento será la referencia para desarrollar la base de datos, el backend y las interfaces.

Para el MVP utilizaremos información ficticia.

## 2. Entidades

### 2.1. Proveedores

Tabla: `proveedores`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador único |
| nit | VARCHAR(20) | NIT del proveedor, único |
| nombre | VARCHAR(150) | Razón social |
| correo | VARCHAR(150) | Correo de notificación |
| activo | BOOLEAN | Estado del proveedor |

### 2.2. Usuarios

Tabla: `usuarios`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador único |
| nombre | VARCHAR(150) | Nombre del usuario |
| correo | VARCHAR(150) | Correo único |
| password_hash | VARCHAR(255) | Contraseña almacenada como hash |
| rol | VARCHAR(20) | ADMIN o PROVEEDOR |
| proveedor_id | INTEGER | Proveedor asociado, si aplica |
| activo | BOOLEAN | Estado del usuario |

Reglas:
- Un ADMIN no necesita proveedor asociado.
- Un usuario PROVEEDOR debe tener proveedor asociado.
- No se almacenan contraseñas en texto plano.
- Cada proveedor solo puede consultar su información.

### 2.3. Publicaciones

Tabla: `publicaciones`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador único |
| periodo | VARCHAR(7) | Mes en formato YYYY-MM |
| fecha_publicacion | TIMESTAMP | Fecha de publicación |
| estado | VARCHAR(20) | BORRADOR o PUBLICADO |

Reglas:
- Cada período tiene una publicación única.
- Los indicadores en BORRADOR no son visibles para proveedores.
- Al publicar un período se habilita su consulta.

### 2.4. Indicadores

Tabla: `indicadores`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador único |
| proveedor_id | INTEGER | Proveedor al que pertenece |
| publicacion_id | INTEGER | Publicación asociada |
| nombre | VARCHAR(150) | Nombre del indicador |
| valor | NUMERIC(12,2) | Resultado del indicador |
| unidad | VARCHAR(30) | %, días, unidades, etc. |

Reglas:
- Cada indicador pertenece a un proveedor.
- Cada indicador pertenece a una publicación mensual.
- Un proveedor puede tener varios indicadores por período.
- Solo se muestran indicadores de publicaciones PUBLICADO.

### 2.5. Notificaciones

Tabla: `notificaciones`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador único |
| proveedor_id | INTEGER | Proveedor destinatario |
| publicacion_id | INTEGER | Publicación notificada |
| correo_destino | VARCHAR(150) | Correo utilizado |
| fecha_envio | TIMESTAMP | Fecha del intento |
| estado | VARCHAR(20) | PENDIENTE, ENVIADO o FALLIDO |
| error | TEXT | Detalle del error, si existe |

Reglas:
- Se registra el resultado de cada intento de envío.
- Un envío fallido no elimina los indicadores.
- Los correos notifican la disponibilidad de información.
- Los indicadores se consultan dentro del portal.

## 3. Relaciones

- Un proveedor puede tener varios usuarios.
- Un proveedor puede tener muchos indicadores.
- Una publicación puede contener muchos indicadores.
- Un proveedor puede tener varias notificaciones.
- Una publicación puede generar varias notificaciones.

## 4. Flujo de información

1. Haceb registra o consulta proveedores.
2. Un administrador crea una publicación mensual.
3. Se cargan indicadores asociados a proveedores.
4. Los indicadores se almacenan en PostgreSQL.
5. Haceb cambia la publicación a PUBLICADO.
6. El backend habilita la consulta de indicadores.
7. Se generan las notificaciones correspondientes.
8. Cada proveedor accede al portal y consulta sus indicadores.
9. Los resultados históricos permanecen disponibles.

## 5. Seguridad

- El frontend nunca accede directamente a PostgreSQL.
- FastAPI valida la identidad y el rol del usuario.
- El proveedor_id autorizado se obtiene de la sesión autenticada.
- No se permite consultar indicadores de otro proveedor.
- Los datos en BORRADOR no son visibles para proveedores.
- Las contraseñas se almacenan mediante hashes seguros.
- No se incluyen credenciales reales en GitHub.

## 6. Datos de prueba

Se utilizarán al menos tres proveedores ficticios:

| ID | NIT | Nombre |
|---|---|---|
| 1 | 900000001 | Proveedor Demo A |
| 2 | 900000002 | Proveedor Demo B |
| 3 | 900000003 | Proveedor Demo C |

Períodos de prueba:
- 2026-09
- 2026-10

Indicadores de ejemplo:
- Cumplimiento de entregas (%)
- Calidad de productos (%)
- Tiempo promedio de entrega (días)

Los valores serán ficticios y no representarán información real de Haceb.

## 7. Restricciones del MVP

- PostgreSQL será la base de datos principal.
- FastAPI gestionará las operaciones y permisos.
- React consumirá los endpoints de FastAPI.
- No se conectará directamente con Power BI en esta primera versión.
- Los correos se probarán en un entorno controlado.
- No se utilizarán datos confidenciales de Haceb.

## 8. Criterios de aceptación

- [ ] Las cinco tablas están definidas.
- [ ] Las relaciones entre entidades son coherentes.
- [ ] Cada indicador pertenece a un proveedor y una publicación.
- [ ] Los proveedores no pueden consultar datos ajenos.
- [ ] Los indicadores en borrador permanecen ocultos.
- [ ] Las notificaciones permiten registrar errores.
- [ ] Existen datos ficticios para realizar pruebas.

## 9. Consideraciones de implementación

- Utilizar claves primarias para los identificadores.
- Utilizar claves foráneas para las relaciones.
- Establecer restricciones de unicidad para NIT, correo y período.
- Validar los valores permitidos de roles y estados.
- Crear índices para las consultas por proveedor y período.
- Definir las reglas de actualización y eliminación sin perder el historial.
