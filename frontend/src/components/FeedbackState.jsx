export default function FeedbackState({ variant = 'empty', title, message, actionLabel, onAction }) {
  return (
    <section className={`feedback-state feedback-state--${variant}`} role={variant === 'error' ? 'alert' : 'status'}>
      <span className="feedback-state__icon" aria-hidden="true">
        {variant === 'error' ? '!' : variant === 'loading' ? <span className="loading-spinner" /> : '↗'}
      </span>
      <h3>{title}</h3>
      <p>{message}</p>
      {actionLabel && onAction && (
        <button className="button button--outline" type="button" onClick={onAction}>{actionLabel}</button>
      )}
    </section>
  );
}