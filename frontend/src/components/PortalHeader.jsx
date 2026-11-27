import BrandMark from './BrandMark.jsx';

export default function PortalHeader({ user, onLogout }) {
  return (
    <header className="portal-header">
      <a className="portal-header__brand" href="#inicio" aria-label="Inicio del portal">
        <BrandMark />
        <span className="portal-header__divider" />
        <span className="portal-header__section">Proveedores</span>
      </a>
      <div className="portal-header__account">
        <div className="account-avatar" aria-hidden="true">
          {(user.nombre || 'P').trim().charAt(0).toUpperCase()}
        </div>
        <div className="account-copy">
          <span className="account-copy__name">{user.nombre}</span>
          <span className="account-copy__email">{user.correo}</span>
        </div>
        <button className="button button--quiet logout-button" type="button" onClick={onLogout}>
          <svg viewBox="0 0 20 20" aria-hidden="true">
            <path d="M8 3H4.8A1.8 1.8 0 0 0 3 4.8v10.4A1.8 1.8 0 0 0 4.8 17H8M12.5 6.5 16 10l-3.5 3.5M7 10h9" />
          </svg>
          <span>Cerrar sesión</span>
        </button>
      </div>
    </header>
  );
}