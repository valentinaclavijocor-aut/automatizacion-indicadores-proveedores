import hacebLogo from '../assets/haceb-logo.png';

export default function BrandMark({ compact = false }) {
  return (
    <div
      className={`brand-mark${compact ? ' brand-mark--compact' : ''}`}
      role="img"
      aria-label="Haceb"
    >
      <img className="brand-mark__logo" src={hacebLogo} alt="" />
    </div>
  );
}