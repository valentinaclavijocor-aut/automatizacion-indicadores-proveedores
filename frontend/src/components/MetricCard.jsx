export default function MetricCard({ indicator, index }) {
  const value = typeof indicator.valor === 'number'
    ? new Intl.NumberFormat('es-CO', { maximumFractionDigits: 2 }).format(indicator.valor)
    : indicator.valor;

  return (
    <article className="metric-card" style={{ '--card-index': index }}>
      <div className="metric-card__topline">
        <span className={`metric-card__icon metric-card__icon--${index % 3}`} aria-hidden="true">
          {index % 3 === 0 ? (
            <svg viewBox="0 0 24 24"><path d="M5 17.5 9.5 13l3 3L20 8.5M14.5 8.5H20V14" /></svg>
          ) : index % 3 === 1 ? (
            <svg viewBox="0 0 24 24"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3Z" /></svg>
          ) : (
            <svg viewBox="0 0 24 24"><path d="M4 19V5m0 14h16M8 15l3-4 3 2 5-6" /></svg>
          )}
        </span>
        <span className="metric-card__index">{String(index + 1).padStart(2, '0')}</span>
      </div>
      <h3>{indicator.nombre}</h3>
      <div className="metric-card__value">
        <span>{value}</span>
        {indicator.unidad && <span className="metric-card__unit">{indicator.unidad}</span>}
      </div>
      <span className="metric-card__caption">Resultado del período</span>
    </article>
  );
}