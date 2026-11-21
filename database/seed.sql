-- ============================================================================
-- HACEB DB-01 | SEED CON DATOS FICTICIOS EXTRAÍDOS DE LOS CSV DEL EQUIPO
-- Fuentes: proveedores.csv, indicadores_mensuales.csv y ordenes.csv (2026).
-- SQL autoconenido, no requiere archivos externos al ejecutarse.
-- Respeta exactamente las cinco tablas definidas en docs/modelo-datos.md.
-- ADMIN incluye las funciones de administrador/ingeniero (sin rol adicional).
-- Los correos .example se conservaron literalmente; NO son direcciones reales.
-- P011 y P012 NO se insertan: sus correos de origen están vacío o mal formado.
-- Sus valores originales permanecen intactos en data_fuente/proveedores.csv.
-- Usuarios de laboratorio: contraseña ficticia Demo123! (no se almacena).
-- Solo contiene hashes Argon2id independientes con sal propia.
-- Orden: schema.sql -> seed.sql -> pruebas.sql. No toca frontend/backend.
-- ============================================================================
BEGIN;
-- Proveedores: ID entero 1..10 correspondiente a P001..P010 del CSV.
INSERT INTO proveedores (id, nit, nombre, correo, activo) VALUES
    (1, '900123137-7', 'Industrias Metálicas Antioquia S.A.S.', 'compras@metalicasantioquia.example', TRUE),
    (2, '900123274-1', 'Inyectora del Valle Ltda.', 'compras@inyectoravalle.example', TRUE),
    (3, '900123411-7', 'Empacadora Cartón Andino S.A.', 'compras@cartonandino.example', TRUE),
    (4, '900123548-0', 'Tornillería Norte de Santander SAS', 'compras@tornillerianorte.example', TRUE),
    (5, '900123685-0', 'Resortes Industriales Oriente Colombia S.A.', 'compras@resortesoriente.example', TRUE),
    (6, '900123822-6', 'Vidrios Templados Medellín Ltda.', 'compras@vidriostemplados.example', TRUE),
    (7, '900123959-0', 'Motores Pequeños Antioquia S.A.S.', 'compras@motoresantioquia.example', TRUE),
    (8, '900124096-1', 'Fundición de Caldas S.A.', 'compras@fundicioncaldas.example', TRUE),
    (9, '900124233-5', 'Plásticos EcoPaisa S.A.S.', 'compras@plasticosecopaisa.example', TRUE),
    (10, '900124370-3', 'Acero Refractario Antioquia Ltda.', 'compras@acerorefractario.example', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Usuarios: se reutiliza el correo ficticio EXISTENTE de cada proveedor.
-- El administrador es una cuenta de laboratorio adicional con dominio .example.
INSERT INTO usuarios (id, nombre, correo, password_hash, rol, proveedor_id, activo) VALUES
    (1, 'Administrador e Ingeniero Demo', 'admin@portal-haceb.example', '$argon2id$v=19$m=65536,t=3,p=2$F+xEl+ahXneWWIg485j/ng$MKHdPW00WUIyAFZ5qDF+ltqO0oeI+ov9M8oU+k5vUVg', 'ADMIN', NULL, TRUE),
    (2, 'Carolina Restrepo', 'compras@metalicasantioquia.example', '$argon2id$v=19$m=65536,t=3,p=2$3CkYZ78uM7qzN0845uxMfQ$gPa12MJQHY7EIXBUsDXSuOf9TG0n9gA9PRDP9GSh8Eg', 'PROVEEDOR', 1, TRUE),
    (3, 'Andrés Muñoz', 'compras@inyectoravalle.example', '$argon2id$v=19$m=65536,t=3,p=2$588SIlBWiBVXFC5z5mQb+A$AmCKxYuOkLCIGFkknRqX0lv+BwW9AiDPKqbxFYHzu9E', 'PROVEEDOR', 2, TRUE),
    (4, 'Diana Castaño', 'compras@cartonandino.example', '$argon2id$v=19$m=65536,t=3,p=2$0ANfLjMA501bjKrz8GasXg$8uBVOI4RpRMUY6v0E1MpeuVKbMk+BI+wYQh9b+7iD00', 'PROVEEDOR', 3, TRUE),
    (5, 'Juan Ospina', 'compras@tornillerianorte.example', '$argon2id$v=19$m=65536,t=3,p=2$8c9gpOhAPvpJg8TgTYnhUg$GqQyt2JkodIjlOyxBaEMq4Chc0Qp7bFcXYHtRzanVi4', 'PROVEEDOR', 4, TRUE),
    (6, 'Luisa Henao', 'compras@resortesoriente.example', '$argon2id$v=19$m=65536,t=3,p=2$j9BP62ACb78KcW1Ned6n8A$0Jq0xDbXNaMul8gu9iTqu8SNoq9PxW5nm3F91g4dYdI', 'PROVEEDOR', 5, TRUE),
    (7, 'Felipe Giraldo', 'compras@vidriostemplados.example', '$argon2id$v=19$m=65536,t=3,p=2$B0eWwji+zVJtRM9UIGFcew$+a1Op4SglOLekPwoe80yYD5M7bf2Z/RuSQfyrLlJBjo', 'PROVEEDOR', 6, TRUE),
    (8, 'Natalia Arango', 'compras@motoresantioquia.example', '$argon2id$v=19$m=65536,t=3,p=2$HhkT0/QYC1AbqvagOy2JXQ$t89spsgfRB5zb7RQEMkEzfrLDXPrVQmxW6Sn9C/B0DU', 'PROVEEDOR', 7, TRUE),
    (9, 'Santiago Mejía', 'compras@fundicioncaldas.example', '$argon2id$v=19$m=65536,t=3,p=2$fGQ0kNF+NB1SqFl2lX2DBg$gr8jGnVBvWDK6x/g/mGT8tQYa8OkHf8ojZljPi6kQ/M', 'PROVEEDOR', 8, TRUE),
    (10, 'Paula Ríos', 'compras@plasticosecopaisa.example', '$argon2id$v=19$m=65536,t=3,p=2$FHGFsTohHT8+1jyXKOElxQ$gnXgyQwmXLC5EBf+7/KAgLWbl8UwVsuJHSPJ8e6uw0w', 'PROVEEDOR', 9, TRUE),
    (11, 'Camilo Vélez', 'compras@acerorefractario.example', '$argon2id$v=19$m=65536,t=3,p=2$kOqXnpYUr+/fzPAdmFhWrA$hTpBuYL8QPRytxFfE2mrrmrnnkLPo2DWH2zcBywb444', 'PROVEEDOR', 10, TRUE)
ON CONFLICT (id) DO NOTHING;

-- Publicaciones. Septiembre: PUBLICADO, octubre: BORRADOR para probar permisos.
INSERT INTO publicaciones (id, periodo, fecha_publicacion, estado) VALUES
    (1, '2026-09', NULL, 'BORRADOR'),
    (2, '2026-10', NULL, 'BORRADOR')
ON CONFLICT (id) DO NOTHING;

-- Los tres primeros indicadores provienen de indicadores_mensuales.csv.
-- Los otros tres se calculan de ordenes.csv (filtrado por fecha_orden).
-- Unidades requeridas/entregadas = suma de cantidades por proveedor y mes.
-- Entregas puntuales = 100 * líneas entregadas antes/en fecha / líneas totales.
-- No se guardan pedidos ni columnas que no estén en el modelo del MVP.
-- No se usa ON CONFLICT en indicadores para no ejecutar triggers en publicados.
INSERT INTO indicadores (id, proveedor_id, publicacion_id, nombre, valor, unidad)
SELECT datos.*
FROM (VALUES
    (  1,  1, 1, 'Cumplimiento OTIF', 100.00, '%'),
    (  2,  1, 1, 'Nivel de inventario', 95.40, '%'),
    (  3,  1, 1, 'Nivel de servicio integral', 97.70, '%'),
    (  4,  1, 1, 'Unidades requeridas', 4780.00, 'unidades'),
    (  5,  1, 1, 'Unidades entregadas', 4780.00, 'unidades'),
    (  6,  1, 1, 'Entregas puntuales', 100.00, '%'),
    (  7,  2, 1, 'Cumplimiento OTIF', 100.00, '%'),
    (  8,  2, 1, 'Nivel de inventario', 99.60, '%'),
    (  9,  2, 1, 'Nivel de servicio integral', 99.80, '%'),
    ( 10,  2, 1, 'Unidades requeridas', 5300.00, 'unidades'),
    ( 11,  2, 1, 'Unidades entregadas', 5300.00, 'unidades'),
    ( 12,  2, 1, 'Entregas puntuales', 100.00, '%'),
    ( 13,  3, 1, 'Cumplimiento OTIF', 100.00, '%'),
    ( 14,  3, 1, 'Nivel de inventario', 94.70, '%'),
    ( 15,  3, 1, 'Nivel de servicio integral', 97.40, '%'),
    ( 16,  3, 1, 'Unidades requeridas', 5320.00, 'unidades'),
    ( 17,  3, 1, 'Unidades entregadas', 5320.00, 'unidades'),
    ( 18,  3, 1, 'Entregas puntuales', 100.00, '%'),
    ( 19,  4, 1, 'Cumplimiento OTIF', 100.00, '%'),
    ( 20,  4, 1, 'Nivel de inventario', 97.10, '%'),
    ( 21,  4, 1, 'Nivel de servicio integral', 98.60, '%'),
    ( 22,  4, 1, 'Unidades requeridas', 5900.00, 'unidades'),
    ( 23,  4, 1, 'Unidades entregadas', 5900.00, 'unidades'),
    ( 24,  4, 1, 'Entregas puntuales', 100.00, '%'),
    ( 25,  5, 1, 'Cumplimiento OTIF', 85.70, '%'),
    ( 26,  5, 1, 'Nivel de inventario', 80.10, '%'),
    ( 27,  5, 1, 'Nivel de servicio integral', 82.90, '%'),
    ( 28,  5, 1, 'Unidades requeridas', 6390.00, 'unidades'),
    ( 29,  5, 1, 'Unidades entregadas', 6231.00, 'unidades'),
    ( 30,  5, 1, 'Entregas puntuales', 92.86, '%'),
    ( 31,  6, 1, 'Cumplimiento OTIF', 85.70, '%'),
    ( 32,  6, 1, 'Nivel de inventario', 93.40, '%'),
    ( 33,  6, 1, 'Nivel de servicio integral', 89.60, '%'),
    ( 34,  6, 1, 'Unidades requeridas', 6940.00, 'unidades'),
    ( 35,  6, 1, 'Unidades entregadas', 6770.00, 'unidades'),
    ( 36,  6, 1, 'Entregas puntuales', 92.86, '%'),
    ( 37,  7, 1, 'Cumplimiento OTIF', 80.00, '%'),
    ( 38,  7, 1, 'Nivel de inventario', 85.20, '%'),
    ( 39,  7, 1, 'Nivel de servicio integral', 82.60, '%'),
    ( 40,  7, 1, 'Unidades requeridas', 4400.00, 'unidades'),
    ( 41,  7, 1, 'Unidades entregadas', 4148.00, 'unidades'),
    ( 42,  7, 1, 'Entregas puntuales', 90.00, '%'),
    ( 43,  8, 1, 'Cumplimiento OTIF', 83.30, '%'),
    ( 44,  8, 1, 'Nivel de inventario', 82.00, '%'),
    ( 45,  8, 1, 'Nivel de servicio integral', 82.70, '%'),
    ( 46,  8, 1, 'Unidades requeridas', 5010.00, 'unidades'),
    ( 47,  8, 1, 'Unidades entregadas', 4845.00, 'unidades'),
    ( 48,  8, 1, 'Entregas puntuales', 91.67, '%'),
    ( 49,  9, 1, 'Cumplimiento OTIF', 83.30, '%'),
    ( 50,  9, 1, 'Nivel de inventario', 88.30, '%'),
    ( 51,  9, 1, 'Nivel de servicio integral', 85.80, '%'),
    ( 52,  9, 1, 'Unidades requeridas', 5190.00, 'unidades'),
    ( 53,  9, 1, 'Unidades entregadas', 4962.00, 'unidades'),
    ( 54,  9, 1, 'Entregas puntuales', 91.67, '%'),
    ( 55, 10, 1, 'Cumplimiento OTIF', 85.70, '%'),
    ( 56, 10, 1, 'Nivel de inventario', 80.70, '%'),
    ( 57, 10, 1, 'Nivel de servicio integral', 83.20, '%'),
    ( 58, 10, 1, 'Unidades requeridas', 6070.00, 'unidades'),
    ( 59, 10, 1, 'Unidades entregadas', 5900.00, 'unidades'),
    ( 60, 10, 1, 'Entregas puntuales', 92.86, '%'),
    ( 61,  1, 2, 'Cumplimiento OTIF', 100.00, '%'),
    ( 62,  1, 2, 'Nivel de inventario', 94.90, '%'),
    ( 63,  1, 2, 'Nivel de servicio integral', 97.50, '%'),
    ( 64,  1, 2, 'Unidades requeridas', 6360.00, 'unidades'),
    ( 65,  1, 2, 'Unidades entregadas', 6360.00, 'unidades'),
    ( 66,  1, 2, 'Entregas puntuales', 100.00, '%'),
    ( 67,  2, 2, 'Cumplimiento OTIF', 100.00, '%'),
    ( 68,  2, 2, 'Nivel de inventario', 95.40, '%'),
    ( 69,  2, 2, 'Nivel de servicio integral', 97.70, '%'),
    ( 70,  2, 2, 'Unidades requeridas', 5990.00, 'unidades'),
    ( 71,  2, 2, 'Unidades entregadas', 5990.00, 'unidades'),
    ( 72,  2, 2, 'Entregas puntuales', 100.00, '%'),
    ( 73,  3, 2, 'Cumplimiento OTIF', 100.00, '%'),
    ( 74,  3, 2, 'Nivel de inventario', 94.50, '%'),
    ( 75,  3, 2, 'Nivel de servicio integral', 97.30, '%'),
    ( 76,  3, 2, 'Unidades requeridas', 3520.00, 'unidades'),
    ( 77,  3, 2, 'Unidades entregadas', 3520.00, 'unidades'),
    ( 78,  3, 2, 'Entregas puntuales', 100.00, '%'),
    ( 79,  4, 2, 'Cumplimiento OTIF', 100.00, '%'),
    ( 80,  4, 2, 'Nivel de inventario', 97.10, '%'),
    ( 81,  4, 2, 'Nivel de servicio integral', 98.60, '%'),
    ( 82,  4, 2, 'Unidades requeridas', 3550.00, 'unidades'),
    ( 83,  4, 2, 'Unidades entregadas', 3550.00, 'unidades'),
    ( 84,  4, 2, 'Entregas puntuales', 100.00, '%'),
    ( 85,  5, 2, 'Cumplimiento OTIF', 84.60, '%'),
    ( 86,  5, 2, 'Nivel de inventario', 84.90, '%'),
    ( 87,  5, 2, 'Nivel de servicio integral', 84.80, '%'),
    ( 88,  5, 2, 'Unidades requeridas', 5230.00, 'unidades'),
    ( 89,  5, 2, 'Unidades entregadas', 5165.00, 'unidades'),
    ( 90,  5, 2, 'Entregas puntuales', 92.31, '%'),
    ( 91,  6, 2, 'Cumplimiento OTIF', 80.00, '%'),
    ( 92,  6, 2, 'Nivel de inventario', 91.90, '%'),
    ( 93,  6, 2, 'Nivel de servicio integral', 86.00, '%'),
    ( 94,  6, 2, 'Unidades requeridas', 3350.00, 'unidades'),
    ( 95,  6, 2, 'Unidades entregadas', 3349.00, 'unidades'),
    ( 96,  6, 2, 'Entregas puntuales', 90.00, '%'),
    ( 97,  7, 2, 'Cumplimiento OTIF', 81.80, '%'),
    ( 98,  7, 2, 'Nivel de inventario', 84.10, '%'),
    ( 99,  7, 2, 'Nivel de servicio integral', 83.00, '%'),
    (100,  7, 2, 'Unidades requeridas', 5200.00, 'unidades'),
    (101,  7, 2, 'Unidades entregadas', 5014.00, 'unidades'),
    (102,  7, 2, 'Entregas puntuales', 90.91, '%'),
    (103,  8, 2, 'Cumplimiento OTIF', 84.60, '%'),
    (104,  8, 2, 'Nivel de inventario', 94.00, '%'),
    (105,  8, 2, 'Nivel de servicio integral', 89.30, '%'),
    (106,  8, 2, 'Unidades requeridas', 5250.00, 'unidades'),
    (107,  8, 2, 'Unidades entregadas', 5211.00, 'unidades'),
    (108,  8, 2, 'Entregas puntuales', 92.31, '%'),
    (109,  9, 2, 'Cumplimiento OTIF', 83.30, '%'),
    (110,  9, 2, 'Nivel de inventario', 95.60, '%'),
    (111,  9, 2, 'Nivel de servicio integral', 89.50, '%'),
    (112,  9, 2, 'Unidades requeridas', 5770.00, 'unidades'),
    (113,  9, 2, 'Unidades entregadas', 5643.00, 'unidades'),
    (114,  9, 2, 'Entregas puntuales', 91.67, '%'),
    (115, 10, 2, 'Cumplimiento OTIF', 83.30, '%'),
    (116, 10, 2, 'Nivel de inventario', 86.70, '%'),
    (117, 10, 2, 'Nivel de servicio integral', 85.00, '%'),
    (118, 10, 2, 'Unidades requeridas', 5220.00, 'unidades'),
    (119, 10, 2, 'Unidades entregadas', 5033.00, 'unidades'),
    (120, 10, 2, 'Entregas puntuales', 91.67, '%')
) AS datos(id, proveedor_id, publicacion_id, nombre, valor, unidad)
WHERE NOT EXISTS (SELECT 1 FROM indicadores i WHERE i.id = datos.id);

-- El cambio a PUBLICADO crea los avisos PENDIENTES usando el correo ficticio
-- tal como se cargó en proveedores. No envía mensajes reales.
UPDATE publicaciones
   SET estado = 'PUBLICADO', fecha_publicacion = '2026-10-02 08:00:00'
 WHERE id = 1 AND estado = 'BORRADOR';

-- Simulamos dos resultados de notificación; las otras ocho siguen PENDIENTE.
UPDATE notificaciones
   SET estado = 'ENVIADO', fecha_envio = '2026-10-02 08:05:00', error = NULL
 WHERE proveedor_id = 1 AND publicacion_id = 1 AND estado = 'PENDIENTE';

UPDATE notificaciones
   SET estado = 'FALLIDO', fecha_envio = '2026-10-02 08:05:00',
       error = 'Error simulado: dirección .example no admite entrega real'
 WHERE proveedor_id = 2 AND publicacion_id = 1 AND estado = 'PENDIENTE';

-- Ajustar las secuencias por haber usado IDs explícitos en el seed.
SELECT setval(pg_get_serial_sequence('proveedores', 'id'), (SELECT MAX(id) FROM proveedores), TRUE);
SELECT setval(pg_get_serial_sequence('usuarios', 'id'), (SELECT MAX(id) FROM usuarios), TRUE);
SELECT setval(pg_get_serial_sequence('publicaciones', 'id'), (SELECT MAX(id) FROM publicaciones), TRUE);
SELECT setval(pg_get_serial_sequence('indicadores', 'id'), (SELECT MAX(id) FROM indicadores), TRUE);
SELECT setval(pg_get_serial_sequence('notificaciones', 'id'), (SELECT MAX(id) FROM notificaciones), TRUE);
COMMIT;
