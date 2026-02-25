from __future__ import annotations

from typing import Dict, List

from .agent_orchestrator import agent_orchestrator
from .audit_logger import audit_logger
from .atave_validator import atave_validator
from .command_verifier import command_verifier
from .detector import Detector, compute_risk_score
from .intel_correlator import intel_correlator
from .mitigation_generator import mitigation_generator
from .models import Incident, PipelineResult, RiskAssessment
from .playbook_executor import playbook_executor
from .playbook_generator import playbook_generator
from .redis_client import redis_client
from .sandbox_executor import sandbox_executor


detector = Detector()


class PipelineOrchestrator:
    def ingest_data(self, incident: Incident) -> None:
        redis_client.enqueue("incident_ingestion", incident.model_dump(mode="json"))
        redis_client.cache_incident(f"incident:{incident.incident_id}", incident.model_dump(mode="json"))

    def _historical_similarity(self, incident: Incident) -> List[Dict]:
        logs = redis_client.get_audit_logs(limit=20)
        current_tokens = set(f"{incident.title} {incident.description}".lower().split())
        scored = []
        for item in logs:
            text = f"{item.get('title', '')} {item.get('description', '')}".lower()
            tokens = set(text.split())
            overlap = len(current_tokens.intersection(tokens))
            if overlap:
                scored.append({"audit_id": item.get("audit_id"), "similarity": overlap, "mitigation": item.get("mitigation_commands", [])})
        return sorted(scored, key=lambda x: x["similarity"], reverse=True)[:3]

    def process_incident(self, incident: Incident) -> PipelineResult:
        self.ingest_data(incident)
        classification = detector.classify(incident)
        risk = RiskAssessment(**compute_risk_score(incident.severity, incident.confidence, incident.asset_criticality))
        threat_intel = intel_correlator.correlate(incident)

        mitigation = mitigation_generator.generate({
            "title": incident.title,
            "description": incident.description,
            "source_ip": incident.source_ip or "",
            "risk_level": risk.level,
        })
        verification = command_verifier.verify(mitigation["commands"])
        atave = atave_validator.validate(verification["accepted"], risk.level)
        sandbox = sandbox_executor.execute(verification["accepted"] if atave["approved"] else [])

        playbook = playbook_generator.generate(classification["threat_type"], incident.severity, "production asset")
        playbook_state = playbook_executor.execute(verification["accepted"], risk.level)

        planner, executor, auditor = agent_orchestrator.execute(
            incident,
            risk.level,
            len(verification["accepted"]),
            atave["approved"],
            len(verification["rejected"]),
        )

        timeline = [
            {"stage": "Detection", "status": "done"},
            {"stage": "Analysis", "status": "done"},
            {"stage": "Risk Score", "status": risk.level},
            {"stage": "Mitigation", "status": "generated"},
            {"stage": "Execution", "status": sandbox["status"]},
            {"stage": "Audit", "status": "logged"},
        ]

        historical = self._historical_similarity(incident)

        audit_id = audit_logger.log({
            "incident_id": incident.incident_id,
            "title": incident.title,
            "description": incident.description,
            "risk": risk.model_dump(),
            "mitigation_commands": verification["accepted"],
            "timeline": timeline,
        })

        return PipelineResult(
            incident=incident,
            risk=risk,
            mitre_tactic=classification["mitre_tactic"],
            llm_reasoning=mitigation["reasoning"],
            mitigation_commands=mitigation["commands"],
            command_validation=verification,
            atave_validation=atave,
            sandbox_result=sandbox,
            threat_intel=threat_intel,
            historical_similarity=historical,
            planner_decision=planner,
            executor_decision=executor,
            auditor_decision=auditor,
            playbook={**playbook, "execution": playbook_state},
            timeline=timeline,
            audit_id=audit_id,
        )


pipeline_orchestrator = PipelineOrchestrator()
