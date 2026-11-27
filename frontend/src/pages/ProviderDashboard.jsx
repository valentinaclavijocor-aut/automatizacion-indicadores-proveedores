import { useEffect, useState } from 'react';
import FeedbackState from '../components/FeedbackState.jsx';
import MetricCard from '../components/MetricCard.jsx';
import PeriodSelector, { formatPeriod } from '../components/PeriodSelector.jsx';
import PortalHeader from '../components/PortalHeader.jsx';
import { ApiError, getIndicators, getPeriods } from '../services/api.js';

function formatPublicationDate(value) {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return new Intl.DateTimeFormat('es-CO', { day: 'numeric', month: 'long', year: 'numeric' }).format(date);
}

export default function ProviderDashboard({ user, token, isDemo, onLogout }) {
  const [periods, setPeriods] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState('');
  const [periodsLoading, setPeriodsLoading] = useState(true);
  const [periodsError, setPeriodsError] = useState('');
  const [periodsAttempt, setPeriodsAttempt] = useState(0);
  const [indicators, setIndicators] = useState([]);
  const [indicatorsLoading, setIndicatorsLoading] = useState(false);
  const [indicatorsError, setIndicatorsError] = useState('');
  const [indicatorsAttempt, setIndicatorsAttempt] = useState(0);

  useEffect(() => {
    let active = true;
    setPeriodsLoading(true);
    setPeriodsError('');

    getPeriods(token)
      .then((result) => {
        if (!active) return;
        const availablePeriods = Array.isArray(result) ? result : [];
        setPeriods(availablePeriods);
        setSelectedPeriod((current) => (
          availablePeriods.some(({ periodo }) => periodo === current)
            ? current
            : availablePeriods[0]?.periodo ?? ''
        ));
      })
      .catch((error) => {
        if (!active) return;
        setPeriodsError(error.message || 'No pudimos cargar tus períodos.');
        if (error instanceof ApiError && error.status === 401) onLogout();
      })
      .finally(() => {
        if (active) setPeriodsLoading(false);
      });

    return () => { active = false; };
  }, [token, periodsAttempt, onLogout]);

  useEffect(() => {
    if (!selectedPeriod) {
      setIndicators([]);
      setIndicatorsLoading(false);
      setIndicatorsError('');
      return undefined;
    }

    let active = true;
    setIndicatorsLoading(true);
    setIndicatorsError('');

    getIndicators(token, selectedPeriod)
      .then((result) => {
        if (active) setIndicators(Array.isArray(result) ? result : []);
      })
      .catch((error) => {
        if (!active) return;
        setIndicatorsError(error.message || 'No pudimos cargar los indicadores.');
        if (error instanceof ApiError && error.status === 401) onLogout();
      })
      .finally(() => {
        if (active) setIndicatorsLoading(false);
      });

    return () => { active = false; };
  }, [token, selectedPeriod, indicatorsAttempt, onLogout]);

  const selectedPublication = periods.find(({ periodo }) => periodo === selectedPeriod);
  const publicationDate = formatPublicationDate(selectedPublication?.fecha_publicacion);

  return (
    <div className="portal-shell" id="inicio">
      <PortalHeader user={user} onLogout={onLogout} />
      <main className="dashboard-main">
        <section className="dashboard-welcome">
          <div className="dashboard-welcome__copy">
            <span className="eyebrow">TU ESPACIO DE DESEMPEÑO</span>
            <h1>Hola, {user.nombre.split(' ')[0]}<span className="welcome-period">.</span></h1>
            <p>Aquí puedes consultar tus resultados publicados y seguir tu evolución.</p>
          </div>
          {isDemo && <span className="demo-badge"><span />Datos ficticios · demostración</span>}
        </section>

        <section className="results-panel" aria-labelledby="results-title">
          <div className="results-panel__heading">
            <div>
              <span className="eyebrow">RESUMEN MENSUAL</span>
              <h2 id="results-title">Tus indicadores</h2>
            </div>
            <PeriodSelector
              periods={periods}
              selectedPeriod={selectedPeriod}
              onChange={setSelectedPeriod}
              isLoading={periodsLoading}
            />
          </div>

          {periodsLoading && (
            <FeedbackState variant="loading" title="Cargando períodos" message="Estamos consultando tus publicaciones." />
          )}
          {!periodsLoading && periodsError && (
            <FeedbackState
              variant="error"
              title="No pudimos cargar tus períodos"
              message={periodsError}
              actionLabel="Intentar de nuevo"
              onAction={() => setPeriodsAttempt((attempt) => attempt + 1)}
            />
          )}
          {!periodsLoading && !periodsError && periods.length === 0 && (
            <FeedbackState
              title="Aún no hay resultados publicados"
              message="Cuando se publique un período con tus indicadores, podrás consultarlo aquí."
            />
          )}

          {!periodsLoading && !periodsError && periods.length > 0 && (
            <>
              <div className="period-summary">
                <span className="period-summary__dot" />
                <span>{formatPeriod(selectedPeriod)}</span>
                {publicationDate && <span className="period-summary__date">Publicado el {publicationDate}</span>}
              </div>

              {indicatorsLoading && (
                <FeedbackState variant="loading" title="Cargando indicadores" message="Estamos preparando tus resultados." />
              )}
              {!indicatorsLoading && indicatorsError && (
                <FeedbackState
                  variant="error"
                  title="No pudimos cargar los indicadores"
                  message={indicatorsError}
                  actionLabel="Intentar de nuevo"
                  onAction={() => setIndicatorsAttempt((attempt) => attempt + 1)}
                />
              )}
              {!indicatorsLoading && !indicatorsError && indicators.length === 0 && (
                <FeedbackState
                  title="No hay indicadores en este período"
                  message="Todavía no hay resultados disponibles para el período seleccionado. Puedes consultar otro mes."
                />
              )}
              {!indicatorsLoading && !indicatorsError && indicators.length > 0 && (
                <div className="metrics-grid">
                  {indicators.map((indicator, index) => (
                    <MetricCard key={indicator.id ?? `${indicator.nombre}-${index}`} indicator={indicator} index={index} />
                  ))}
                </div>
              )}
            </>
          )}
        </section>

        <footer className="dashboard-footer">
          <span>Información privada de tu cuenta de proveedor.</span>
          <span>¿Necesitas ayuda? Contacta a tu referente de HACEB.</span>
        </footer>
      </main>
    </div>
  );
}