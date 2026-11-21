-- Origen CSV: 10 proveedores con correo .example sintácticamente válido.
-- Dos filas del CSV original con correo vacío/malformado están preservadas
-- en data_fuente pero excluidas de las tablas del MVP por integridad.

-- Haceb - Pruebas de lectura e integridad. Ejecución SIN efectos permanentes.
-- Requiere ejecutar schema.sql y seed.sql previamente.
-- DB-01: ingeniero + administrador => rol ADMIN. No existe rol INGENIERO.
-- SOLO SELECT y bloques que capturan fallos esperados; no quedan datos de prueba nuevos.

-- 1) Deben existir las cinco tablas del contrato.
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public' AND table_type='BASE TABLE'
  AND table_name IN ('proveedores','usuarios','publicaciones','indicadores','notificaciones')
ORDER BY table_name;

-- 2) Los registros de demostración deben sumar 10, 11, 2, 120 y 10.
SELECT 'proveedores' AS tabla, COUNT(*) AS total FROM proveedores
UNION ALL SELECT 'usuarios', COUNT(*) FROM usuarios
UNION ALL SELECT 'publicaciones', COUNT(*) FROM publicaciones
UNION ALL SELECT 'indicadores', COUNT(*) FROM indicadores
UNION ALL SELECT 'notificaciones', COUNT(*) FROM notificaciones;

-- 3) El PROVEEDOR A solo puede ver SUS indicadores PUBLICADOS.
-- En producción FastAPI debe obtener proveedor_id del JWT; jamás del navegador.
SELECT i.id, p.periodo, i.nombre, i.valor, i.unidad
FROM indicadores i
JOIN publicaciones p ON p.id = i.publicacion_id
WHERE i.proveedor_id = 1 AND p.estado = 'PUBLICADO'
ORDER BY p.periodo DESC, i.id;

-- 4) Un período en BORRADOR no debe aparecer en el resultado anterior.
SELECT p.periodo, p.estado, COUNT(i.id) AS indicadores_registrados
FROM publicaciones p LEFT JOIN indicadores i ON i.publicacion_id = p.id
GROUP BY p.id, p.periodo, p.estado ORDER BY p.periodo;

-- 5) Se deben ver ENVIADO, FALLIDO y PENDIENTE.
SELECT n.id, pr.nombre AS proveedor, n.estado, n.fecha_envio, n.error
FROM notificaciones n JOIN proveedores pr ON pr.id=n.proveedor_id
ORDER BY n.id;

-- 6) Verificadores automáticos, fallan si el seed no quedó coherente.
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM proveedores) <> 10
      OR (SELECT COUNT(*) FROM usuarios) <> 11
      OR (SELECT COUNT(*) FROM publicaciones) <> 2
      OR (SELECT COUNT(*) FROM indicadores) <> 120
      OR (SELECT COUNT(*) FROM notificaciones) <> 10 THEN
        RAISE EXCEPTION 'Falló el número esperado de registros demo';
    END IF;

    IF (SELECT COUNT(*) FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name IN ('proveedores', 'usuarios', 'publicaciones', 'indicadores', 'notificaciones')) <> 29 THEN
        RAISE EXCEPTION 'Las cinco tablas deben tener exactamente 29 columnas';
    END IF;

    IF EXISTS (SELECT 1 FROM usuarios WHERE rol NOT IN ('ADMIN', 'PROVEEDOR')) THEN
        RAISE EXCEPTION 'Hay roles no autorizados; ingeniero pertenece a ADMIN';
    END IF;

    IF EXISTS (
        SELECT 1 FROM usuarios u WHERE
            (u.rol='ADMIN' AND u.proveedor_id IS NOT NULL)
            OR (u.rol='PROVEEDOR' AND u.proveedor_id IS NULL)
    ) THEN
        RAISE EXCEPTION 'Hay usuarios con rol/proveedor incoherente';
    END IF;

    IF (SELECT COUNT(*) FROM indicadores i
        JOIN publicaciones p ON p.id = i.publicacion_id
        WHERE i.proveedor_id=1 AND p.estado='PUBLICADO') <> 6 THEN
        RAISE EXCEPTION 'El filtro por proveedor/publicación no es coherente';
    END IF;

    IF (SELECT COUNT(*) FROM notificaciones WHERE estado='ENVIADO') <> 1
      OR (SELECT COUNT(*) FROM notificaciones WHERE estado='FALLIDO') <> 1
      OR (SELECT COUNT(*) FROM notificaciones WHERE estado='PENDIENTE') <> 8 THEN
        RAISE EXCEPTION 'Los estados de notificaciones no coinciden';
    END IF;

    IF EXISTS (SELECT 1 FROM usuarios WHERE password_hash NOT LIKE '$argon2id$%') THEN
        RAISE EXCEPTION 'Hay un hash de demo que no usa Argon2id';
    END IF;

    RAISE NOTICE 'OK: las verificaciones de datos demo pasaron';
END;
$$;

-- 7) Verificar restricciones sin alterar datos: las excepciones se capturan.
DO $$
DECLARE
    rechazo BOOLEAN;
BEGIN
    rechazo := FALSE;
    BEGIN
        INSERT INTO usuarios (nombre, correo, password_hash, rol, proveedor_id)
        SELECT 'Prueba inválida', 'invalido@demo.com', password_hash, 'PROVEEDOR', NULL
        FROM usuarios WHERE id=2;
    EXCEPTION WHEN check_violation THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió PROVEEDOR sin empresa'; END IF;

    rechazo := FALSE;
    BEGIN
        UPDATE indicadores SET valor=70.00 WHERE id=1;
    EXCEPTION WHEN raise_exception THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió editar un indicador publicado'; END IF;

    rechazo := FALSE;
    BEGIN
        INSERT INTO publicaciones (periodo) VALUES ('2026-09');
    EXCEPTION WHEN unique_violation THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió un período duplicado'; END IF;

    rechazo := FALSE;
    BEGIN
        INSERT INTO indicadores (proveedor_id, publicacion_id, nombre, valor, unidad)
        VALUES (999, 2, 'Prueba FK', 90.00, '%');
    EXCEPTION WHEN foreign_key_violation THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió un proveedor inexistente'; END IF;

    -- Se impiden NIT duplicados entre proveedores.
    rechazo := FALSE;
    BEGIN
        INSERT INTO proveedores (nit, nombre, correo)
        VALUES ('900123137-7', 'Empresa duplicada', 'duplicado-nit@example.com');
    EXCEPTION WHEN unique_violation THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió NIT duplicado'; END IF;

    -- Se impiden correos duplicados aunque cambien las mayúsculas.
    rechazo := FALSE;
    BEGIN
        INSERT INTO proveedores (nit, nombre, correo)
        VALUES ('999900001', 'Empresa repetida', 'COMPRAS@METALICASANTIOQUIA.EXAMPLE');
    EXCEPTION WHEN unique_violation THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió correo de proveedor duplicado'; END IF;

    rechazo := FALSE;
    BEGIN
        INSERT INTO usuarios (nombre, correo, password_hash, rol, proveedor_id)
        SELECT 'Cuenta repetida', 'COMPRAS@METALICASANTIOQUIA.EXAMPLE', password_hash, 'PROVEEDOR', 1
        FROM usuarios WHERE id=2;
    EXCEPTION WHEN unique_violation THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió correo de usuario duplicado'; END IF;

    -- La ingeniería queda dentro de ADMIN: INGENIERO no es un rol SQL válido.
    rechazo := FALSE;
    BEGIN
        INSERT INTO usuarios (nombre, correo, password_hash, rol, proveedor_id)
        SELECT 'Rol no aprobado', 'rol-no-aprobado@demo.com', password_hash,
               'INGENIERO', NULL
        FROM usuarios WHERE id=1;
    EXCEPTION WHEN check_violation THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se permitió el rol INGENIERO'; END IF;

    -- Una publicación nueva debe comenzar en BORRADOR.
    rechazo := FALSE;
    BEGIN
        INSERT INTO publicaciones (periodo, fecha_publicacion, estado)
        VALUES ('2026-11', CURRENT_TIMESTAMP, 'PUBLICADO');
    EXCEPTION WHEN raise_exception THEN
        rechazo := TRUE;
    END;
    IF NOT rechazo THEN RAISE EXCEPTION 'ERROR: se creó una publicación como PUBLICADO'; END IF;

    RAISE NOTICE 'OK: rol ADMIN fusionado y restricciones de NIT, correos y publicación validadas';
    RAISE NOTICE 'OK: se bloquearon rol inválido, edición publicada, período duplicado y FK';
END;
$$;

-- 8) Comprobación puntual de valores del CSV (sin datos inventados).
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM proveedores WHERE id=1
          AND nit='900123137-7'
          AND correo='compras@metalicasantioquia.example'
    ) THEN RAISE EXCEPTION 'P001 no coincide con proveedores.csv'; END IF;

    IF NOT EXISTS (
        SELECT 1 FROM indicadores
        WHERE proveedor_id=1 AND publicacion_id=1
          AND nombre='Cumplimiento OTIF' AND valor=100.00
    ) THEN RAISE EXCEPTION 'OTIF de P001 septiembre no coincide con el CSV'; END IF;

    IF NOT EXISTS (
        SELECT 1 FROM indicadores
        WHERE proveedor_id=1 AND publicacion_id=1
          AND nombre='Unidades requeridas' AND valor=4780.00
    ) THEN RAISE EXCEPTION 'Cantidades de P001 no coinciden con ordenes.csv'; END IF;

    IF NOT EXISTS (
        SELECT 1 FROM indicadores
        WHERE proveedor_id=1 AND publicacion_id=2
          AND nombre='Unidades entregadas' AND valor=6360.00
    ) THEN RAISE EXCEPTION 'Cantidad de octubre no coincide con ordenes.csv'; END IF;

    IF EXISTS (SELECT 1 FROM proveedores WHERE correo NOT LIKE '%.example') THEN
        RAISE EXCEPTION 'Se alteró algún correo ficticio del conjunto de origen';
    END IF;

    RAISE NOTICE 'OK: CSV preservados, mapeo correcto e indicadores de septiembre/octubre';
END;
$$;
