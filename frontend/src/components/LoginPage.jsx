import { useState } from 'react';
import BrandMark from './BrandMark.jsx';

export default function LoginPage({ onLogin, isLoading, error, isDemo }) {
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');

  function handleSubmit(event) {
    event.preventDefault();
    onLogin(correo.trim(), password);
  }

  return (
    <main className="login-layout">
      <div className="login-card">
        <section className="login-story" aria-label="Portal de proveedores Haceb">
          <div className="login-story__top">
            <BrandMark />
            <span className="login-story__tag">RELACIONES QUE AVANZAN</span>
          </div>
          <div className="login-story__content">
            <span className="eyebrow eyebrow--light">PORTAL DE PROVEEDORES</span>
            <h1>Tu desempeño,<br />siempre a la vista.</h1>
            <p>Un espacio para consultar tus resultados y seguir construyendo juntos.</p>
          </div>
          <div className="login-story__footer">
            <span className="story-orbit story-orbit--one" />
            <span className="story-orbit story-orbit--two" />
            <span className="story-orbit story-orbit--three" />
            <span>Conectamos para crecer.</span>
            <span className="login-story__year">HACEB · 2026</span>
          </div>
        </section>

        <section className="login-panel">
          <div className="login-panel__mobile-brand"><BrandMark /></div>
          <div className="login-form-wrap">
            <span className="eyebrow">ACCESO SEGURO</span>
            <h2>Qué bueno tenerte<br />por aquí.</h2>
            <p className="login-intro">Ingresa con la cuenta asociada a tu empresa.</p>

            <form className="login-form" onSubmit={handleSubmit}>
              <label htmlFor="correo">Correo electrónico</label>
              <input
                id="correo"
                name="correo"
                type="email"
                autoComplete="username"
                placeholder="nombre@empresa.com"
                value={correo}
                onChange={(event) => setCorreo(event.target.value)}
                required
              />

              <label htmlFor="password">Contraseña</label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                placeholder="Ingresa tu contraseña"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />

              {error && <p className="form-error" role="alert">{error}</p>}

              <button className="button button--primary login-submit" type="submit" disabled={isLoading}>
                {isLoading ? 'Ingresando…' : 'Iniciar sesión'}
                {!isLoading && <span aria-hidden="true">→</span>}
              </button>
            </form>

            {isDemo && (
              <p className="demo-note">
                <span className="demo-note__dot" />
                Demostración activa: usa cualquier correo y contraseña no vacíos.
              </p>
            )}
            <p className="login-help">¿Necesitas ayuda para ingresar? Contacta a tu referente de HACEB.</p>
          </div>
          <span className="login-panel__copyright">© Haceb · Portal de proveedores</span>
        </section>
      </div>
    </main>
  );
}