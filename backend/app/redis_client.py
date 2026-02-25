import json
import os
from typing import Any, Dict, List

import redis


class RedisClient:
    def __init__(self) -> None:
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        self.client = redis.Redis.from_url(self.redis_url, decode_responses=True)

    def enqueue(self, queue: str, payload: Dict[str, Any]) -> None:
        self.client.rpush(queue, json.dumps(payload))

    def read_stream(self, stream: str, count: int = 50) -> List[Dict[str, Any]]:
        entries = self.client.xrevrange(stream, count=count)
        return [{"id": entry_id, **data} for entry_id, data in entries]

    def publish_agent_event(self, stream: str, payload: Dict[str, Any]) -> str:
        normalized = {k: json.dumps(v) if not isinstance(v, str) else v for k, v in payload.items()}
        return self.client.xadd(stream, normalized)

    def cache_incident(self, key: str, payload: Dict[str, Any]) -> None:
        self.client.set(key, json.dumps(payload), ex=86400)

    def get_json(self, key: str) -> Dict[str, Any] | None:
        value = self.client.get(key)
        if not value:
            return None
        return json.loads(value)

    def append_audit_log(self, payload: Dict[str, Any]) -> None:
        self.client.lpush("audit_logs", json.dumps(payload))

    def get_audit_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        logs = self.client.lrange("audit_logs", 0, limit - 1)
        return [json.loads(item) for item in logs]


redis_client = RedisClient()
