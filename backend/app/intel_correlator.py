from __future__ import annotations

from .cve_mapper import cve_mapper
from .models import Incident, ThreatIntel
from .threat_intel_fetcher import threat_intel_fetcher


class IntelCorrelator:
    def correlate(self, incident: Incident) -> ThreatIntel:
        ip_data = threat_intel_fetcher.fetch(incident.source_ip)
        cves = cve_mapper.map_from_text(f"{incident.title} {incident.description}")
        return ThreatIntel(**ip_data, cves=cves)


intel_correlator = IntelCorrelator()
