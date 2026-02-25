from __future__ import annotations

from typing import Dict, List

from .llm_engine import llm_engine


class MitigationGenerator:
    def generate(self, incident_summary: Dict[str, str]) -> Dict[str, object]:
        prompt = (
            "Generate short SOC mitigation steps for incident: "
            f"{incident_summary}. Include host containment and monitoring notes."
        )
        reasoning = llm_engine.ask(prompt)

        source_ip = incident_summary.get("source_ip")
        commands: List[str] = []
        if source_ip:
            commands.append(f"iptables -A INPUT -s {source_ip} -j DROP")
            commands.append(f"ufw deny from {source_ip}")
        commands.append("systemctl restart ssh")
        commands.append("echo 'incident isolated'")

        return {"reasoning": reasoning, "commands": commands}


mitigation_generator = MitigationGenerator()
