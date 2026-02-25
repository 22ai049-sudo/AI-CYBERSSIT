from __future__ import annotations

from .llm_engine import llm_engine
from .models import AgentDecision


class ExecutorAgent:
    def run(self, command_count: int, strategy: str) -> AgentDecision:
        reasoning = llm_engine.ask(
            f"Explain execution approach for {command_count} commands with strategy {strategy}",
            system="You are Executor Agent for SOC response.",
        )
        decision = {"playbook_execution": "triggered", "strategy": strategy, "commands_prepared": command_count}
        return AgentDecision(agent="executor", reasoning=reasoning, decision=decision)


executor_agent = ExecutorAgent()
