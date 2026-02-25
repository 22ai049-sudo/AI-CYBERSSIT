from __future__ import annotations

from typing import Dict, List

from .atave_validator import atave_validator
from .command_verifier import command_verifier
from .sandbox_executor import sandbox_executor


class PlaybookExecutor:
    def execute(self, commands: List[str], threat_level: str) -> Dict:
        verify = command_verifier.verify(commands)
        atave = atave_validator.validate(verify["accepted"], threat_level)
        sandbox = sandbox_executor.execute(verify["accepted"] if atave["approved"] else [])
        return {"verification": verify, "atave": atave, "sandbox": sandbox}


playbook_executor = PlaybookExecutor()
