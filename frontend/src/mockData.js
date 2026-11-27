// Datos completamente ficticios para demostración. Nunca son información real de HACEB.
export const initialData = {
  proveedores: [
    { id: 1, nit: '900000001', nombre: 'Proveedor Demo Andino', correo: 'andino@ejemplo.test', activo: true },
    { id: 2, nit: '900000002', nombre: 'Suministros Demo Norte', correo: 'norte@ejemplo.test', activo: true },
    { id: 3, nit: '900000003', nombre: 'Logística Demo Central', correo: 'central@ejemplo.test', activo: false },
    { id: 4, nit: '900000004', nombre: 'Insumos Demo del Valle', correo: 'valle@ejemplo.test', activo: true },
    { id: 5, nit: '900000005', nombre: 'Distribuidora Demo Sur', correo: 'sur@ejemplo.test', activo: true },
  ],
  publicaciones: [
    { id: 1, periodo: '2026-09', estado: 'PUBLICADO', fecha_publicacion: '2026-10-08T13:00:00Z' },
    { id: 2, periodo: '2026-10', estado: 'BORRADOR', fecha_publicacion: null },
  ],
  indicadores: [
    { id: 1, proveedor_id: 1, publicacion_id: 1, nombre: 'Cumplimiento de entregas', valor: 96.5, unidad: '%' },
    { id: 2, proveedor_id: 1, publicacion_id: 1, nombre: 'Calidad de productos', valor: 98.2, unidad: '%' },
    { id: 3, proveedor_id: 2, publicacion_id: 1, nombre: 'Cumplimiento de entregas', valor: 89.7, unidad: '%' },
    { id: 4, proveedor_id: 1, publicacion_id: 2, nombre: 'Cumplimiento de entregas', valor: 94.1, unidad: '%' },
    { id: 5, proveedor_id: 2, publicacion_id: 2, nombre: 'Calidad de productos', valor: 97.3, unidad: '%' },
  ],
  notificaciones: [
    { id: 1, proveedor_id: 1, publicacion_id: 1, correo_destino: 'andino@ejemplo.test', fecha_envio: '2026-10-08T13:03:00Z', estado: 'ENVIADO', error: null },
    { id: 2, proveedor_id: 2, publicacion_id: 1, correo_destino: 'norte@ejemplo.test', fecha_envio: '2026-10-08T13:03:00Z', estado: 'ENVIADO', error: null },
  ],
}
