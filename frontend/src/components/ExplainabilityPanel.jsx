export default function ExplainabilityPanel({ result }) {
  if (!result) return <div className="card">AI reasoning will appear here.</div>;
  return (
    <div className="card">
      <h3>AI Analysis Panel</h3>
      <p><strong>MITRE ATT&CK:</strong> {result.mitre_tactic}</p>
      <p><strong>Confidence:</strong> {(result.incident.confidence * 100).toFixed(0)}%</p>
      <p><strong>Reasoning:</strong> {result.llm_reasoning}</p>
    </div>
  );
}
