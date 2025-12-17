#!/usr/bin/env python3
"""Read superpowers user configuration."""
import json
import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "superpowers" / "config.json"

DEFAULTS = {
    "artifacts": {
        "plans": "llm/implementation-plans",
        "designs": "llm/designs",
        "progress": "llm"
    }
}

def get_config():
    """Return merged config (user + defaults)."""
    config = DEFAULTS.copy()
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            user_config = json.load(f)
        # Deep merge artifacts section
        if "artifacts" in user_config:
            config["artifacts"].update(user_config["artifacts"])
    return config

def get_artifact_path(artifact_type: str) -> str:
    """Get path for artifact type (plans, designs, progress)."""
    config = get_config()
    return config["artifacts"].get(artifact_type, DEFAULTS["artifacts"].get(artifact_type))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(get_artifact_path(sys.argv[1]))
    else:
        print(json.dumps(get_config(), indent=2))
