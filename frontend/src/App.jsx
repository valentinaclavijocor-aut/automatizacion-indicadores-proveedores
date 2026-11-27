import { useCallback, useEffect, useState } from 'react';
import LoginPage from './components/LoginPage.jsx';
import ProviderDashboard from './pages/ProviderDashboard.jsx';
import {
  clearSession,
  getAccessToken,
  getCurrentUser,
  isDemoMode,
  login,
  saveAccessToken,
} from './services/api.js';

export default function App() {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [isRestoring, setIsRestoring] = useState(true);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [loginError, setLoginError] = useState('');

  useEffect(() => {
    let active = true;
    const savedToken = getAccessToken();
    if (!savedToken) {
      setIsRestoring(false);
      return () => { active = false; };
    }

    getCurrentUser(savedToken)
      .then((currentUser) => {
        if (!active) return;
        if (!currentUser || currentUser.rol !== 'PROVEEDOR') {
          throw new Error('Esta cuenta no tiene acceso al portal de proveedores.');
        }
        setToken(savedToken);
        setUser(currentUser);
      })
      .catch(() => {
        if (active) clearSession();
      })
      .finally(() => {
        if (active) setIsRestoring(false);
      });

    return () => { active = false; };
  }, []);

  const handleLogout = useCallback(() => {
    clearSession();
    setToken(null);
    setUser(null);
    setLoginError('');
  }, []);

  async function handleLogin(correo, password) {
    setIsLoggingIn(true);
    setLoginError('');
    try {
      const result = await login(correo, password);
      if (!result?.access_token || !result?.usuario) {
        throw new Error('La respuesta de autenticación no tiene el formato esperado.');
      }
      if (result.usuario.rol !== 'PROVEEDOR') {
        throw new Error('Esta cuenta no tiene acceso al portal de proveedores.');
      }
      saveAccessToken(result.access_token);
      setToken(result.access_token);
      setUser(result.usuario);
    } catch (error) {
      setLoginError(error.message || 'No fue posible iniciar sesión. Intenta de nuevo.');
    } finally {
      setIsLoggingIn(false);
    }
  }

  if (isRestoring) {
    return (
      <main className="app-loading" role="status">
        <span className="loading-spinner" />
        <span>Preparando tu espacio…</span>
      </main>
    );
  }

  if (!token || !user) {
    return (
      <LoginPage
        onLogin={handleLogin}
        isLoading={isLoggingIn}
        error={loginError}
        isDemo={isDemoMode()}
      />
    );
  }

  return (
    <ProviderDashboard
      user={user}
      token={token}
      isDemo={isDemoMode()}
      onLogout={handleLogout}
    />
  );
}