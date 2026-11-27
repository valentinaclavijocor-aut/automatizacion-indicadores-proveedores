const DEMO_TOKEN = 'mock-provider-session';
const MOCK_USER_KEY = 'provider-portal-mock-user';

const periods = [
  { periodo: '2026-10', fecha_publicacion: '2026-11-21T14:30:00Z' },
  { periodo: '2026-09', fecha_publicacion: '2026-10-21T14:30:00Z' },
  { periodo: '2026-08', fecha_publicacion: '2026-09-19T14:30:00Z' },
];

const indicatorsByPeriod = {
  '2026-10': [
    { id: 1, periodo: '2026-10', nombre: 'Cumplimiento de entregas', valor: 95.5, unidad: '%' },
    { id: 2, periodo: '2026-10', nombre: 'Calidad de producto', valor: 98, unidad: '%' },
    { id: 3, periodo: '2026-10', nombre: 'Nivel de servicio', valor: 92.4, unidad: '%' },
    { id: 4, periodo: '2026-10', nombre: 'Documentación entregada', valor: 100, unidad: '%' },
  ],
  '2026-09': [
    { id: 5, periodo: '2026-09', nombre: 'Cumplimiento de entregas', valor: 93.8, unidad: '%' },
    { id: 6, periodo: '2026-09', nombre: 'Calidad de producto', valor: 97.2, unidad: '%' },
    { id: 7, periodo: '2026-09', nombre: 'Nivel de servicio', valor: 91, unidad: '%' },
  ],
  '2026-08': [],
};

const wait = (duration = 320) => new Promise((resolve) => setTimeout(resolve, duration));

export async function loginWithMock(correo) {
  await wait();
  const usuario = {
    id: 0,
    nombre: 'Proveedor de demostración',
    correo,
    rol: 'PROVEEDOR',
    proveedor_id: 0,
  };
  sessionStorage.setItem(MOCK_USER_KEY, JSON.stringify(usuario));

  return {
    access_token: DEMO_TOKEN,
    token_type: 'bearer',
    usuario,
  };
}

export async function getMockCurrentUser(token) {
  await wait();
  if (token !== DEMO_TOKEN) {
    throw new Error('La sesión de demostración ya no está disponible.');
  }

  const savedUser = sessionStorage.getItem(MOCK_USER_KEY);
  return savedUser ? JSON.parse(savedUser) : null;
}

export async function getMockPeriods() {
  await wait();
  return periods;
}

export async function getMockIndicators(period) {
  await wait();
  return indicatorsByPeriod[period] ?? [];
}

export function isMockToken(token) {
  return token === DEMO_TOKEN;
}