from __future__ import annotations

import json
import subprocess
from typing import Dict, List


class SandboxExecutor:
    def execute(self, commands: List[str]) -> Dict[str, object]:
        if not commands:
            return {"status": "skipped", "results": [], "sandbox": "docker-dryrun"}
        results = []
        for command in commands:
            docker_cmd = [
                "docker",
                "run",
                "--rm",
                "alpine:3.20",
                "sh",
                "-c",
                f"echo '[SIMULATED] {command}'",
            ]
            try:
                output = subprocess.check_output(docker_cmd, stderr=subprocess.STDOUT, text=True, timeout=12)
                results.append({"command": command, "output": output.strip(), "status": "ok"})
            except Exception as exc:
                results.append({"command": command, "output": str(exc), "status": "error"})
        return {
            "status": "completed",
            "sandbox": "docker-alpine",
            "isolation_log": json.dumps({"commands_executed": len(commands)}),
            "results": results,
        }


sandbox_executor = SandboxExecutor()
