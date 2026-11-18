
# Arquitectura del MVP - EstudIA / Haceb

## 1. Objetivo

Desarrollar una plataforma web para que Haceb publique indicadores mensuales y cada proveedor consulte únicamente su información.

El sistema notificará por correo cuando existan nuevos indicadores disponibles.

## 2. Tecnologías

- Frontend: React + Vite.
- Backend: Python + FastAPI.
- Base de datos: PostgreSQL.
- Control de versiones: Git y GitHub.
- Pruebas: manuales y con datos ficticios.

## 3. Módulos del sistema

### Panel administrativo Haceb
- Consultar proveedores registrados.
- Cargar indicadores de un período.
- Publicar indicadores.
- Consultar el historial de publicaciones.

### Portal de proveedores
- Iniciar sesión.
- Consultar indicadores propios.
- Consultar períodos anteriores.
- Visualizar resultados en tablas o gráficas.

### Backend
- Recibir solicitudes del frontend.
- Validar información.
- Consultar y guardar datos.
- Controlar permisos de acceso.
- Gestionar la publicación de indicadores.

### Base de datos
Almacenará:
- Proveedores.
- Usuarios y roles.
- Indicadores.
- Períodos de publicación.
- Historial de notificaciones.

### Automatización
- Detectar nuevos indicadores publicados.
- Generar notificaciones por proveedor.
- Enviar correos electrónicos.
- Registrar resultados y errores.

## 4. Flujo general

1. Haceb ingresa al panel administrativo.
2. Carga los indicadores mensuales.
3. El backend valida y almacena la información.
4. Haceb publica los indicadores.
5. El sistema genera las notificaciones.
6. Cada proveedor recibe un correo.
7. El proveedor inicia sesión y consulta sus resultados.

## 5. Estructura del repositorio

- `frontend/`: interfaces React.
- `backend/`: API FastAPI y lógica de negocio.
- `database/`: scripts SQL y datos ficticios.
- `docs/`: documentación funcional y técnica.
- `.github/`: plantillas de Issues y Pull Requests.

## 6. Reglas técnicas

- El frontend se comunica con el backend mediante HTTP y JSON.
- Solo el backend puede acceder a PostgreSQL.
- Los proveedores no pueden consultar información de otros proveedores.
- La autorización debe verificarse en el backend.
- No almacenar contraseñas en texto plano.
- No subir credenciales ni información sensible al repositorio.
- Utilizar datos simulados durante el desarrollo.
- No modificar directamente la rama `main`.
- Cada funcionalidad se entrega mediante Pull Request.

## 7. Alcance y limitaciones

El MVP demostrará el flujo completo con proveedores e indicadores ficticios.

La integración con Power BI y el despliegue productivo quedan sujetos a la disponibilidad de accesos, infraestructura y autorizaciones de Haceb.

La autenticación, el almacenamiento y el envío de correos podrán implementarse inicialmente en un entorno de demostración.

## 8. Trabajo colaborativo con IA

Cada integrante recibirá un Issue con:
- Objetivo y requerimiento funcional.
- Herramientas y archivos involucrados.
- Instrucciones de implementación.
- Prompt para solicitar ayuda a una IA.
- Criterios de aceptación.
- Pruebas y evidencias esperadas.

El código generado con IA debe ser revisado, comprendido y probado antes de integrarse.
