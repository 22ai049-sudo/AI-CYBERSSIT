const severityColor = { Low: 'green', Medium: 'gold', High: 'orange', Critical: 'red' };

export default function IncidentPanel({ incident, risk }) {
  if (!incident) return <div className="card">No incident selected.</div>;
  return (
    <div className="card pulse">
      <h3>Live Incident Feed</h3>
      <p><strong>{incident.title}</strong></p>
      <p>Source IP: {incident.source_ip || 'N/A'}</p>
      <p>Time: {new Date(incident.timestamp || Date.now()).toLocaleString()}</p>
      <span className="badge" style={{ background: severityColor[risk?.level] || '#444' }}>
        {risk?.level || 'Unknown'}
      </span>
    </div>
  );
}
