import { useEffect, useState } from 'react';
import axios from 'axios';
import IncidentPanel from './IncidentPanel';
import ExplainabilityPanel from './ExplainabilityPanel';
import MitigationPanel from './MitigationPanel';
import RiskScoreChart from './RiskScoreChart';
import AuditLogsViewer from './AuditLogsViewer';

axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function AnalystDashboard() {
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);

  const runDemo = async () => {
    const demos = await axios.get('/api/demo/incidents');
    const response = await axios.post('/api/incidents/process', demos.data[0]);
    setResult(response.data);
    const audit = await axios.get('/api/audit/logs');
    setLogs(audit.data);
  };

  useEffect(() => { runDemo(); }, []);

  const topMetrics = [
    ['Total Incidents Today', logs.length],
    ['High Severity Alerts', logs.filter((l) => ['High', 'Critical'].includes(l.risk?.level)).length],
    ['Mitigations Executed', logs.length],
    ['False Positives', 0],
    ['Mean Response Time', '1.2m']
  ];

  return (
    <div className="dashboard">
      <h1>LLM-Driven Autonomous SOC Orchestration Prototype</h1>
      <div className="metrics">{topMetrics.map(([k, v]) => <div className="metric" key={k}><span>{k}</span><strong>{v}</strong></div>)}</div>
      <div className="grid">
        <IncidentPanel incident={result?.incident} risk={result?.risk} />
        <RiskScoreChart risk={result?.risk} />
        <ExplainabilityPanel result={result} />
        <MitigationPanel result={result} />
        <AuditLogsViewer logs={logs} />
        <div className="card">
          <h3>Incident Timeline</h3>
          {(result?.timeline || []).map((s) => <p key={s.stage}>{s.stage} → {s.status}</p>)}
        </div>
      </div>
    </div>
  );
}
