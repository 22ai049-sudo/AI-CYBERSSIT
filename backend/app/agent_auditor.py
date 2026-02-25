from __future__ import annotations

from .llm_engine import llm_engine
from .models import AgentDecision


class AuditorAgent:
    def run(self, passed: bool, rejected_count: int) -> AgentDecision:
        reasoning = llm_engine.ask(
            f"Validate SOC actions passed={passed} rejected={rejected_count}",
            system="You are Auditor Agent for SOC compliance.",
        )
        decision = {
            "compliance_status": "pass" if passed else "review-required",
            "rejected_commands": rejected_count,
        }
        return AgentDecision(agent="auditor", reasoning=reasoning, decision=decision)


auditor_agent = AuditorAgent()
