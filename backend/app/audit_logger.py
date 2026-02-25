from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from typing import Dict

from .redis_client import redis_client


class AuditLogger:
    def __init__(self) -> None:
        self.log_dir = Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, payload: Dict) -> str:
        audit_id = str(uuid4())
        record = {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat(),
            **payload,
        }
        file_path = self.log_dir / f"audit-{datetime.utcnow().date().isoformat()}.jsonl"
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        redis_client.append_audit_log(record)
        return audit_id


audit_logger = AuditLogger()
