from __future__ import annotations

from .agent_auditor import auditor_agent
from .agent_executor import executor_agent
from .agent_planner import planner_agent
from .models import Incident
from .redis_client import redis_client


class AgentOrchestrator:
    def execute(self, incident: Incident, risk_level: str, command_count: int, pipeline_ok: bool, rejected_count: int):
        planner = planner_agent.run(incident, risk_level)
        redis_client.publish_agent_event("agent:planner", planner.model_dump())

        executor = executor_agent.run(command_count, planner.decision.get("strategy", "containment"))
        redis_client.publish_agent_event("agent:executor", executor.model_dump())

        auditor = auditor_agent.run(pipeline_ok, rejected_count)
        redis_client.publish_agent_event("agent:auditor", auditor.model_dump())
        return planner, executor, auditor


agent_orchestrator = AgentOrchestrator()
