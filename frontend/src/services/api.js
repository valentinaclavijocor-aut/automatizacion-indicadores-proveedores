import {
  getMockCurrentUser,
  getMockIndicators,
  getMockPeriods,
  isMockToken,
  loginWithMock,
} from './mockApi.js';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '');
const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API !== 'false';
const ACCESS_TOKEN_KEY = 'provider-portal-access-token';

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function request(path, { method = 'GET', token, body } = {}) {
  const headers = { Accept: 'application/json' };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiError('No fue posible conectar con el servicio. Intenta de nuevo.', 0);
  }

  const contentType = response.headers.get('content-type') ?? '';
  const data = contentType.includes('application/json')
    ? await response.json().catch(() => null)
    : null;

  if (!response.ok) {
    const message = typeof data?.detail === 'string'
      ? data.detail
      : 'Ocurrió un error al consultar la información.';
    throw new ApiError(message, response.status);
  }

  return data;
}

export function getAccessToken() {
  return sessionStorage.getItem(ACCESS_TOKEN_KEY);
}

export function saveAccessToken(token) {
  sessionStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function clearSession() {
  sessionStorage.removeItem(ACCESS_TOKEN_KEY);
  sessionStorage.removeItem('provider-portal-mock-user');
}

export function isDemoMode() {
  return USE_MOCK_API;
}

export async function login(correo, password) {
  if (USE_MOCK_API) return loginWithMock(correo);

  return request('/api/v1/auth/login', {
    method: 'POST',
    body: { correo, password },
  });
}

export async function getCurrentUser(token) {
  if (USE_MOCK_API && isMockToken(token)) return getMockCurrentUser(token);
  return request('/api/v1/auth/me', { token });
}

export async function getPeriods(token) {
  if (USE_MOCK_API && isMockToken(token)) return getMockPeriods();
  return request('/api/v1/mis-periodos', { token });
}

export async function getIndicators(token, period) {
  if (USE_MOCK_API && isMockToken(token)) return getMockIndicators(period);
  const query = new URLSearchParams({ periodo: period });
  return request(`/api/v1/mis-indicadores?${query.toString()}`, { token });
}