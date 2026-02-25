import os
from typing import Dict

import httpx


class AbuseIPDBConnector:
    def __init__(self) -> None:
        self.api_key = os.getenv("ABUSEIPDB_API_KEY", "")

    def check_ip(self, ip: str) -> Dict[str, object]:
        if not self.api_key:
            return {"abuse_confidence": 65, "reports": 3, "source": "mock"}
        headers = {"Key": self.api_key, "Accept": "application/json"}
        params = {"ipAddress": ip, "maxAgeInDays": 90}
        try:
            response = httpx.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", {})
            return {
                "abuse_confidence": data.get("abuseConfidenceScore", 0),
                "reports": data.get("totalReports", 0),
                "source": "abuseipdb",
            }
        except Exception:
            return {"abuse_confidence": 40, "reports": 1, "source": "fallback"}


abuseipdb_connector = AbuseIPDBConnector()
