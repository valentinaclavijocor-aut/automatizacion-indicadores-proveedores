# Portal de proveedores

## Iniciar en modo de demostración

Requiere Node.js y npm. Desde esta carpeta ejecuta:

```sh
npm install
npm run dev
```

El portal usa datos ficticios de forma predeterminada. En el formulario de acceso puedes escribir cualquier correo y contraseña no vacíos; no hay credenciales de demostración predefinidas.

## Conectar con el backend

Crea un archivo `.env.local` a partir de `.env.example`, establece `VITE_USE_MOCK_API=false` y configura `VITE_API_BASE_URL` con la URL del backend (por ejemplo, `http://localhost:8000`). Reinicia Vite después de cambiar variables de entorno. El cliente consume `/api/v1/auth/login`, `/api/v1/auth/me`, `/api/v1/mis-periodos` y `/api/v1/mis-indicadores`; envía el token JWT como Bearer y no envía un identificador de proveedor.

## Estructura

- `src/components/`: formulario de acceso, cabecera, selector, tarjetas de indicadores y estados de interfaz.
- `src/pages/ProviderDashboard.jsx`: carga los períodos y resultados del usuario autenticado.
- `src/services/`: cliente HTTP y datos ficticios sustituibles por la API.
- `src/App.jsx`: restaura la sesión y presenta el acceso o el portal según el estado de autenticación.