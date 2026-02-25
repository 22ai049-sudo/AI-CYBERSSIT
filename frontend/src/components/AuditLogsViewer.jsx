export default function AuditLogsViewer({ logs }) {
  return (
    <div className="card">
      <h3>Audit Logs Viewer</h3>
      <div className="logs">
        {logs.map((log) => (
          <div key={log.audit_id} className="logItem">
            <strong>{log.incident_id}</strong> - {log.risk?.level} - {log.timestamp}
          </div>
        ))}
      </div>
    </div>
  );
}
