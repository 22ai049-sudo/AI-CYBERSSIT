from __future__ import annotations

from typing import Dict

from .llm_engine import llm_engine
from .playbook_repository import playbook_repository


class PlaybookGenerator:
    def generate(self, attack_type: str, severity: int, affected_asset: str) -> Dict:
        prompt = (
            f"Generate SOC playbook for {attack_type} with severity {severity} on {affected_asset}. "
            "Include detection confirmation, containment, commands, host isolation, network blocks, recovery, forensics."
        )
        reasoning = llm_engine.ask(prompt, system="You are a SOAR playbook engineer.")
        playbook = {
            "attack_type": attack_type,
            "steps": [
                "Confirm detection with correlated telemetry",
                "Contain host and block malicious IOC",
                "Execute validated mitigation commands",
                "Collect volatile and disk forensic artifacts",
                "Recover service and apply hardening",
            ],
            "reasoning": reasoning,
            "status": "generated",
        }
        playbook_repository.save(attack_type, playbook)
        return playbook


playbook_generator = PlaybookGenerator()
