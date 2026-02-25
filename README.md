# AI-CYBERSSIT — LLM-Driven Autonomous SOC Orchestration Prototype

Production-style SOC automation platform with FastAPI backend, React dashboard, Redis orchestration, Docker sandbox execution, Ollama (Mistral 7B), threat intelligence enrichment, and multi-agent response workflow.

## Architecture

- **Backend (FastAPI):** incident ingestion, detection, risk scoring, MITRE mapping, LLM explainability, command safety validation, ATAVE checks, sandbox execution, audit logging.
- **Agents:** Planner → Executor → Auditor connected by Redis streams.
- **Threat Intel:** VirusTotal + AbuseIPDB connectors (mock fallback when keys absent) and CVE mapping.
- **Playbooks:** LLM-generated adaptive response playbooks, repository, and execution pipeline.
- **Frontend (React):** SOC control center with metrics bar, incident feed, risk gauge/progress, AI explainability, mitigation HITL controls, timeline, audit logs.

## Backend Modules

1. detector.py
2. redis_client.py
3. llm_engine.py
4. mitigation_generator.py
5. command_verifier.py
6. atave_validator.py
7. sandbox_executor.py
8. audit_logger.py
9. pipeline_orchestrator.py
10. main_api.py

Additional modules included for requested extensions:

- agent_planner.py
- agent_executor.py
- agent_auditor.py
- agent_orchestrator.py
- playbook_generator.py
- playbook_executor.py
- playbook_repository.py
- threat_intel_fetcher.py
- vt_connector.py
- abuseipdb_connector.py
- cve_mapper.py
- intel_correlator.py

## Frontend Modules

1. AnalystDashboard.jsx
2. IncidentPanel.jsx
3. ExplainabilityPanel.jsx
4. MitigationPanel.jsx
5. RiskScoreChart.jsx
6. AuditLogsViewer.jsx

## Security Controls

- Command whitelist enforcement (`command_verifier.py`)
- Unsafe command rejection (`command_verifier.py`)
- ATAVE policy validation (`atave_validator.py`)
- Docker sandbox isolation logging (`sandbox_executor.py`)

## Installation (Local)

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main_api:app --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

## Redis Setup

- Docker: `docker run -p 6379:6379 redis:7-alpine`
- Env: `REDIS_URL=redis://localhost:6379/0`

## Ollama Setup (Mistral 7B)

```bash
ollama serve
ollama pull mistral:7b
```

Set backend env:

```bash
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=mistral:7b
```

## Threat Intelligence Keys

```bash
export VT_API_KEY=your_virustotal_key
export ABUSEIPDB_API_KEY=your_abuseipdb_key
```

When unavailable, connectors automatically use safe mocked outputs.

## Docker Compose Deployment

```bash
docker-compose up --build
```

Services:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Redis: localhost:6379
- Ollama: localhost:11434

## Run Instructions

1. Open frontend dashboard.
2. Demo incident auto-runs from `/api/demo/incidents`.
3. Review risk score, MITRE mapping, threat intel enrichment, timeline, and audit logs.
4. Use **Approve / Reject / Modify** in Mitigation Queue for human-in-the-loop operations.

## Data Ingestion Process

- Incident posted to `/api/incidents/process`
- Stored in Redis ingestion queue and cache
- Enriched with threat intelligence and CVE mapping
- Compared with historical incidents from audit memory
- Processed by multi-agent flow and response pipeline

## API Endpoints

- `POST /api/incidents/process`
- `POST /api/mitigation/review`
- `GET /api/audit/logs`
- `GET /api/demo/incidents`
- `GET /api/agent/{planner|executor|auditor}`
- `GET /health`
