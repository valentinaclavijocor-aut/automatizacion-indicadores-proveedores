# Base de datos Haceb | DB-01 con CSV ficticios

Esta entrega implementa únicamente **PostgreSQL**, sin modificar React, FastAPI ni el prototipo HTML. Respeta los 29 campos y las cinco tablas de `docs/modelo-datos.md` y las reglas de `docs/contrato-api.md`.

## Archivos

- `schema.sql`: copia sin cambios del esquema aprobado, con cinco tablas y sus restricciones.
- `seed.sql`: datos de prueba basados en los tres CSV reales del ejercicio (todos los datos son **ficticios**).
- `pruebas.sql`: consultas y verificaciones de integridad para las evidencias del PR.
- `ORIGEN_CSV.md`: explica qué datos se copiaron, cómo se relacionan y por qué se excluyeron dos filas.
- `data_fuente/`: copia **idéntica** de `proveedores.csv`, `ordenes.csv` e `indicadores_mensuales.csv` para trazabilidad (solo contienen datos ficticios).

## Requisitos

- PostgreSQL 14 o superior, `psql` o pgAdmin 4.
- Trabajar en una base local vacía, sin contraseñas ni información real de Haceb.

## Ejecutar desde la raíz del repositorio

```bash
psql -U postgres -d postgres -c "CREATE DATABASE haceb_mvp;"
psql -U postgres -d haceb_mvp -v ON_ERROR_STOP=1 -f database/schema.sql
psql -U postgres -d haceb_mvp -v ON_ERROR_STOP=1 -f database/seed.sql
psql -U postgres -d haceb_mvp -v ON_ERROR_STOP=1 -f database/pruebas.sql
```

En pgAdmin: crear la base `haceb_mvp`, abrir Query Tool y ejecutar los scripts en el mismo orden. **No volver a ejecutar `schema.sql` sobre una base que ya contiene tablas.**

El `seed.sql` es autónomo: no necesita leer archivos externos en tiempo de ejecución. Los archivos de origen se adjuntan como respaldo y evidencia.

## Resultados esperados

| Tabla | Filas |
|---|---:|
| proveedores | 10 |
| usuarios | 11 |
| publicaciones | 2 |
| indicadores | 120 |
| notificaciones | 10 |

Períodos: `2026-09` publicado; `2026-10` en borrador.

## Relación entre tablas

- `proveedores.id` se conecta con `usuarios.proveedor_id`, `indicadores.proveedor_id` y `notificaciones.proveedor_id`.
- `publicaciones.id` se conecta con `indicadores.publicacion_id` y `notificaciones.publicacion_id`.
- NIT y correos duplicados son rechazados, incluso con mayúsculas diferentes.
- El rol `ADMIN` reúne administrador e ingeniero; los proveedores usan `PROVEEDOR`.
- Las publicaciones en `BORRADOR` se mantienen ocultas para usuarios `PROVEEDOR` mediante filtros del backend.

## ¿Cómo se calcularon los indicadores?

Por proveedor y mes:

1. **Cumplimiento OTIF**: valor de `pct_otif` en `indicadores_mensuales.csv`.
2. **Nivel de inventario**: valor de `pct_nivel_inventario`.
3. **Nivel de servicio integral**: valor de `pct_ns_integral`.
4. **Unidades requeridas**: suma de `cantidad_requerida` en `ordenes.csv`.
5. **Unidades entregadas**: suma de `cantidad_entregada` en `ordenes.csv`.
6. **Entregas puntuales**: porcentaje de líneas con `fecha_entrega` anterior o igual a `fecha_requerida`.

El período de una orden se establece por `fecha_orden`, como está documentado en `ORIGEN_CSV.md`. Solo se usan septiembre y octubre de 2026. La estructura del esquema **no cambia**.

## Usuarios de laboratorio y seguridad

- Un usuario ficticio `ADMIN`: `admin@portal-haceb.example`.
- Cada proveedor importado tiene un usuario con el **mismo correo ficticio que aparece en el CSV**, sin reemplazarlo por correos reales.
- Clave compartida *solo para laboratorio*: `Demo123!`, pero se almacenan únicamente once hashes Argon2id con sales independientes.
- Los correos `.example` no se deben usar para envíos reales ni conectarse a un servidor de correo externo.
- FastAPI deberá verificar la contraseña contra el hash Argon2id, validar el JWT y obtener `proveedor_id` de la identidad autenticada, no de un parámetro del navegador.
- La base no habilita Row-Level Security en esta etapa; no se debe dar acceso SQL directo a proveedores.

## Prueba básica de consulta

```sql
SELECT p.nombre, pub.periodo, i.nombre AS indicador, i.valor, i.unidad
FROM indicadores i
JOIN proveedores p ON p.id = i.proveedor_id
JOIN publicaciones pub ON pub.id = i.publicacion_id
WHERE i.proveedor_id = 1 AND pub.estado = 'PUBLICADO'
ORDER BY pub.periodo, i.nombre;
```

Este SELECT debe mostrar **seis indicadores de septiembre** del proveedor `P001`, y no debe mostrar el borrador de octubre.

## Evidencia y GitHub

1. Ejecutar `schema.sql`, `seed.sql`, `pruebas.sql` en PostgreSQL local y verificar ausencia de errores.
2. Guardar captura de las cinco tablas, de los conteos `10/11/2/120/10` y de los mensajes `OK`.
3. Subir los archivos de `database/` en la rama `feat/DB-01-base-datos` y crear un PR hacia `main`.
4. Relacionar los sub-issues **DB-01.1 #12**, **DB-01.2 #13**, **DB-01.3 #14** y **DB-01.4 #15**. Pedir revisión antes de fusionar.

```bash
git switch main
git pull origin main
git switch -c feat/DB-01-base-datos
git add database/schema.sql database/seed.sql database/pruebas.sql database/README.md database/ORIGEN_CSV.md database/data_fuente/
git commit -m "feat(db): cargar CSV ficticios y validar indicadores Haceb"
git push -u origin feat/DB-01-base-datos
```

**Importante**: estos scripts no se han ejecutado sobre un servidor PostgreSQL real en este entorno. `pruebas.sql` está preparado para completar la validación en tu máquina.
