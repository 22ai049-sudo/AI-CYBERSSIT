export default function RiskScoreChart({ risk }) {
  if (!risk) return <div className="card">Risk score unavailable.</div>;
  const pct = Math.min((risk.score / 12) * 100, 100);

  return (
    <div className="card">
      <h3>Risk Score Engine</h3>
      <div className="gauge"><div className="gauge-fill" style={{ width: `${pct}%` }} /></div>
      <p>Score: {risk.score} ({risk.level})</p>
      <progress value={pct} max="100" />
      <span className={`badge ${risk.severity_indicator}`}>{risk.level}</span>
    </div>
  );
}
