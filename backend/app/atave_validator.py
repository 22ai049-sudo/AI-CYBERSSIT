from __future__ import annotations

from typing import Dict, List


class AtaveValidator:
    """ATAVE: Action Trust and Attack Vector Evaluation."""

    def validate(self, commands: List[str], threat_level: str) -> Dict[str, object]:
        risk_flags = []
        for command in commands:
            if "pkill" in command and threat_level in {"Low", "Medium"}:
                risk_flags.append({"command": command, "warning": "aggressive response for lower risk"})
        return {
            "policy": "ATAVE-v1",
            "approved": len(risk_flags) == 0,
            "flags": risk_flags,
        }


atave_validator = AtaveValidator()
