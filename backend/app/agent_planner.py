from __future__ import annotations

from .llm_engine import llm_engine
from .models import AgentDecision, Incident


class PlannerAgent:
    def run(self, incident: Incident, risk_level: str) -> AgentDecision:
        reasoning = llm_engine.ask(
            f"Prioritize SOC response urgency for {incident.title} with risk {risk_level}",
            system="You are Planner Agent for SOC triage.",
        )
        decision = {
            "urgency": "immediate" if risk_level in {"High", "Critical"} else "monitor",
            "strategy": "containment" if risk_level in {"High", "Critical"} else "enhanced-monitoring",
        }
        return AgentDecision(agent="planner", reasoning=reasoning, decision=decision)


planner_agent = PlannerAgent()
