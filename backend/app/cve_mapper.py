from __future__ import annotations

from typing import List


KEYWORD_TO_CVE = {
    "openssl": ["CVE-2023-0286"],
    "log4j": ["CVE-2021-44228"],
    "kernel": ["CVE-2024-1086"],
}


class CveMapper:
    def map_from_text(self, text: str) -> List[str]:
        text_l = text.lower()
        cves: List[str] = []
        for key, values in KEYWORD_TO_CVE.items():
            if key in text_l:
                cves.extend(values)
        return sorted(set(cves))


cve_mapper = CveMapper()
