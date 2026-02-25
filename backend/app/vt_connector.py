import os
from typing import Dict

import httpx


class VirusTotalConnector:
    def __init__(self) -> None:
        self.api_key = os.getenv("VT_API_KEY", "")

    def check_ip(self, ip: str) -> Dict[str, object]:
        if not self.api_key:
            return {"score": 42, "label": "suspicious", "source": "mock"}
        headers = {"x-apikey": self.api_key}
        try:
            response = httpx.get(f"https://www.virustotal.com/api/v3/ip_addresses/{ip}", headers=headers, timeout=10)
            response.raise_for_status()
            stats = response.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            total = sum(stats.values()) or 1
            score = int((malicious / total) * 100)
            label = "malicious" if score > 70 else "suspicious" if score > 30 else "benign"
            return {"score": score, "label": label, "source": "virustotal"}
        except Exception:
            return {"score": 35, "label": "suspicious", "source": "fallback"}


vt_connector = VirusTotalConnector()
