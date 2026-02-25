from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


class PlaybookRepository:
    def __init__(self) -> None:
        self.base = Path("playbooks")
        self.base.mkdir(parents=True, exist_ok=True)

    def save(self, attack_type: str, playbook: Dict) -> Path:
        path = self.base / f"{attack_type.replace(' ', '_')}.json"
        path.write_text(json.dumps(playbook, indent=2), encoding="utf-8")
        return path

    def load(self, attack_type: str) -> Dict | None:
        path = self.base / f"{attack_type.replace(' ', '_')}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))


playbook_repository = PlaybookRepository()
