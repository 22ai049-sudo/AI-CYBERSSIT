from __future__ import annotations

from typing import Dict, List

SAFE_PREFIXES = [
    "iptables -A INPUT -s",
    "ufw deny from",
    "pkill -f",
    "systemctl restart",
    "echo",
]

UNSAFE_TERMS = ["rm -rf", "mkfs", "shutdown", "reboot", "dd if="]


class CommandVerifier:
    def verify(self, commands: List[str]) -> Dict[str, object]:
        rejected = []
        accepted = []
        for cmd in commands:
            if any(term in cmd for term in UNSAFE_TERMS):
                rejected.append({"command": cmd, "reason": "unsafe term detected"})
                continue
            if not any(cmd.startswith(prefix) for prefix in SAFE_PREFIXES):
                rejected.append({"command": cmd, "reason": "not in whitelist"})
                continue
            accepted.append(cmd)
        return {
            "accepted": accepted,
            "rejected": rejected,
            "is_safe": len(rejected) == 0,
        }


command_verifier = CommandVerifier()
