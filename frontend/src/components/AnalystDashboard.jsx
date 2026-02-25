import { useEffect, useState } from 'react';
import axios from 'axios';
import IncidentPanel from './IncidentPanel';
import ExplainabilityPanel from './ExplainabilityPanel';
import MitigationPanel from './MitigationPanel';
import RiskScoreChart from './RiskScoreChart';
import AuditLogsViewer from './AuditLogsViewer';

axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function AgentCard({ title, data }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {!data ? <p>No data yet.</p> : <>
        <p><strong>Decision:</strong> {JSON.stringify(data.decision)}</p>
        <p><strong>Reasoning:</strong> {data.reasoning}</p>
      </>}
    </div>
  );
}

function ThreatIntelPanel({ intel }) {
  return (
    <div className="card">
      <h3>Threat Intelligence</h3>
      {!intel ? <p>No enrichment data yet.</p> : <>
        <p><strong>IP Reputation:</strong> {intel.ip_reputation_label} ({intel.ip_reputation_score}/100)</p>
        <p><strong>Malware Detection:</strong> {intel.malware_detection_ratio}</p>
        <p><strong>CVEs:</strong> {(intel.cves || []).join(', ') || 'None mapped'}</p>
      </>}
    </div>
  );
}

function PlaybookPanel({ playbook }) {
  return (
    <div className="card">
      <h3>Playbook Viewer</h3>
      {!playbook ? <p>No playbook generated.</p> : <>
        <p><strong>Attack Type:</strong> {playbook.attack_type}</p>
        <ol>{(playbook.steps || []).map((step) => <li key={step}>{step}</li>)}</ol>
        <p><strong>Status:</strong> {playbook.status}</p>
      </>}
    </div>
  );
}

export default function AnalystDashboard() {
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const runDemo = async () => {
    setLoading(true);
    setError('');
    try {
      const demos = await axios.get('/api/demo/incidents');
      const response = await axios.post('/api/incidents/process', demos.data[0]);
      setResult(response.data);
      const audit = await axios.get('/api/audit/logs');
      setLogs(audit.data);
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || 'Failed to load SOC dashboard data');
    } finally {
      setLoading(false);
    }
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
      {error && <div className="card error">{error}</div>}
      {loading && <div className="card">Loading incidents...</div>}
      <div className="metrics">{topMetrics.map(([k, v]) => <div className="metric" key={k}><span>{k}</span><strong>{v}</strong></div>)}</div>
      <div className="grid">
        <IncidentPanel incident={result?.incident} risk={result?.risk} />
        <RiskScoreChart risk={result?.risk} />
        <ExplainabilityPanel result={result} />
        <MitigationPanel result={result} />
        <ThreatIntelPanel intel={result?.threat_intel} />
        <PlaybookPanel playbook={result?.playbook} />
        <AgentCard title="Planner Decision View" data={result?.planner_decision} />
        <AgentCard title="Executor Action Log" data={result?.executor_decision} />
        <AgentCard title="Auditor Compliance Report" data={result?.auditor_decision} />
        <AuditLogsViewer logs={logs} />
        <div className="card">
          <h3>Incident Timeline</h3>
          {(result?.timeline || []).map((s) => <p key={s.stage}>{s.stage} → {s.status}</p>)}
        </div>
      </div>
    </div>
  );
}
