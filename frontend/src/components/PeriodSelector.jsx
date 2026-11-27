export function formatPeriod(period) {
  if (!/^\d{4}-\d{2}$/.test(period ?? '')) return period ?? '';
  const [year, month] = period.split('-').map(Number);
  const label = new Intl.DateTimeFormat('es-CO', {
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(Date.UTC(year, month - 1, 1)));
  return label.charAt(0).toUpperCase() + label.slice(1);
}

export default function PeriodSelector({ periods, selectedPeriod, onChange, isLoading }) {
  return (
    <div className="period-control">
      <label htmlFor="periodo">Período de consulta</label>
      <div className="period-control__select-wrap">
        <select
          id="periodo"
          value={selectedPeriod}
          onChange={(event) => onChange(event.target.value)}
          disabled={isLoading || periods.length === 0}
        >
          {periods.length === 0 && <option value="">Sin períodos disponibles</option>}
          {periods.map(({ periodo }) => (
            <option key={periodo} value={periodo}>{formatPeriod(periodo)}</option>
          ))}
        </select>
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path d="m4 6 4 4 4-4" />
        </svg>
      </div>
    </div>
  );
}