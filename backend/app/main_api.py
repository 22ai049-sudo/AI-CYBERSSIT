from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import Incident, MitigationReviewRequest
from .pipeline_orchestrator import pipeline_orchestrator
from .redis_client import redis_client

app = FastAPI(title="LLM-Driven Autonomous SOC Orchestration Prototype", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/incidents/process")
def process_incident(incident: Incident):
    return pipeline_orchestrator.process_incident(incident)


@app.post("/api/mitigation/review")
def review_mitigation(payload: MitigationReviewRequest):
    if payload.action not in {"approve", "reject", "modify"}:
        raise HTTPException(status_code=400, detail="Invalid action")
    return {
        "incident_id": payload.incident_id,
        "action": payload.action,
        "commands": payload.modified_commands or [],
        "message": "Human-in-the-loop review registered",
    }


@app.get("/api/audit/logs")
def get_audit_logs(limit: int = 50):
    return redis_client.get_audit_logs(limit)


@app.get("/api/agent/{agent_name}")
def get_agent_stream(agent_name: str):
    if agent_name not in {"planner", "executor", "auditor"}:
        raise HTTPException(status_code=404, detail="Unknown agent")
    return redis_client.read_stream(f"agent:{agent_name}")


@app.get("/api/demo/incidents")
def demo_incidents():
    return [
        {
            "incident_id": "demo-001",
            "title": "Brute force attack detected",
            "description": "Multiple failed login attempts from one IP against admin account",
            "source_ip": "185.220.101.1",
            "severity": 8,
            "confidence": 0.92,
            "asset_criticality": 9,
        },
        {
            "incident_id": "demo-002",
            "title": "Malware download attempt",
            "description": "Endpoint downloaded suspicious executable from known malware host",
            "source_ip": "45.9.148.12",
            "file_hash": "a7f5f35426b927411fc9231b56382173",
            "severity": 9,
            "confidence": 0.88,
            "asset_criticality": 8,
        },
        {
            "incident_id": "demo-003",
            "title": "Suspicious admin login",
            "description": "Admin login from unusual geo location followed by sudo commands",
            "source_ip": "91.121.88.33",
            "severity": 7,
            "confidence": 0.8,
            "asset_criticality": 10,
        },
    ]
