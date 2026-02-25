import os
from textwrap import dedent

import httpx


class LLMEngine:
    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
        self.model = os.getenv("OLLAMA_MODEL", "mistral:7b")

    def ask(self, prompt: str, system: str = "You are a SOC analyst assistant.") -> str:
        payload = {
            "model": self.model,
            "prompt": dedent(f"System: {system}\nUser: {prompt}\nAssistant:"),
            "stream": False,
        }
        try:
            response = httpx.post(f"{self.base_url}/api/generate", json=payload, timeout=20)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception:
            return "Fallback reasoning: suspicious behavior detected; apply safe containment and monitor further telemetry."


llm_engine = LLMEngine()
