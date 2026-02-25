from __future__ import annotations

from typing import Dict

from .models import Incident


MITRE_RULES = {
    "failed login": "Credential Access",
    "sudo": "Privilege Escalation",
    "psexec": "Lateral Movement",
    "c2": "Command and Control",
    "malware": "Execution",
}


class Detector:
    def classify(self, incident: Incident) -> Dict[str, str]:
        content = f"{incident.title} {incident.description}".lower()
        for key, tactic in MITRE_RULES.items():
            if key in content:
                return {"mitre_tactic": tactic, "threat_type": key}
        return {"mitre_tactic": "Discovery", "threat_type": "anomalous activity"}



def compute_risk_score(severity: int, confidence: float, asset_criticality: int) -> Dict[str, str | float]:
    score = round((severity * confidence * asset_criticality) / 10, 2)
    if score <= 3:
        level = "Low"
        indicator = "green"
    elif score <= 6:
        level = "Medium"
        indicator = "yellow"
    elif score <= 10:
        level = "High"
        indicator = "orange"
    else:
        level = "Critical"
        indicator = "red"
    return {"score": score, "level": level, "severity_indicator": indicator}
