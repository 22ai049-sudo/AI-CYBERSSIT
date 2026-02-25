import { useState } from 'react';
import axios from 'axios';

export default function MitigationPanel({ result }) {
  const [message, setMessage] = useState('');
  if (!result) return <div className="card">Mitigation queue empty.</div>;

  const review = async (action) => {
    const res = await axios.post('/api/mitigation/review', {
      incident_id: result.incident.incident_id,
      action
    });
    setMessage(res.data.message);
  };

  return (
    <div className="card">
      <h3>Mitigation Queue</h3>
      <ul>{result.mitigation_commands.map((cmd) => <li key={cmd}>{cmd}</li>)}</ul>
      <div className="buttonRow">
        <button onClick={() => review('approve')}>Approve</button>
        <button onClick={() => review('reject')}>Reject</button>
        <button onClick={() => review('modify')}>Modify</button>
      </div>
      {message && <p>{message}</p>}
    </div>
  );
}
