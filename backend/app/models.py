from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Incident(BaseModel):
    incident_id: str
    title: str
    description: str
    source_ip: Optional[str] = None
    file_hash: Optional[str] = None
    severity: int = Field(ge=1, le=10)
    confidence: float = Field(ge=0, le=1)
    asset_criticality: int = Field(ge=1, le=10)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    raw_event: Dict[str, Any] = Field(default_factory=dict)


class ThreatIntel(BaseModel):
    ip_reputation_score: int = 0
    ip_reputation_label: str = "unknown"
    malware_detection_ratio: str = "0/0"
    cves: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class RiskAssessment(BaseModel):
    score: float
    level: str
    severity_indicator: str


class AgentDecision(BaseModel):
    agent: str
    reasoning: str
    decision: Dict[str, Any]


class PipelineResult(BaseModel):
    incident: Incident
    risk: RiskAssessment
    mitre_tactic: str
    llm_reasoning: str
    mitigation_commands: List[str]
    command_validation: Dict[str, Any]
    atave_validation: Dict[str, Any]
    sandbox_result: Dict[str, Any]
    threat_intel: ThreatIntel
    historical_similarity: List[Dict[str, Any]]
    planner_decision: AgentDecision
    executor_decision: AgentDecision
    auditor_decision: AgentDecision
    playbook: Dict[str, Any]
    timeline: List[Dict[str, Any]]
    audit_id: str


class MitigationReviewRequest(BaseModel):
    incident_id: str
    action: str
    modified_commands: Optional[List[str]] = None
