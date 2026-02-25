from __future__ import annotations

from typing import Dict

from .abuseipdb_connector import abuseipdb_connector
from .vt_connector import vt_connector


class ThreatIntelFetcher:
    def fetch(self, source_ip: str | None) -> Dict[str, object]:
        if not source_ip:
            return {"ip_reputation_score": 0, "ip_reputation_label": "unknown", "tags": []}
        vt = vt_connector.check_ip(source_ip)
        abuse = abuseipdb_connector.check_ip(source_ip)
        score = int((vt.get("score", 0) + abuse.get("abuse_confidence", 0)) / 2)
        label = "malicious" if score > 70 else "suspicious" if score > 35 else "benign"
        return {
            "ip_reputation_score": score,
            "ip_reputation_label": label,
            "malware_detection_ratio": f"{vt.get('score', 0)}/100",
            "tags": [vt.get("source", "unknown"), abuse.get("source", "unknown")],
        }


threat_intel_fetcher = ThreatIntelFetcher()
