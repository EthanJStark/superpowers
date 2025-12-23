#!/usr/bin/env python3
"""Read superpowers user configuration."""
import json
import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "superpowers" / "config.json"

DEFAULTS = {
    "artifact_root": "llm",
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
        # Merge artifact_root if present
        if "artifact_root" in user_config:
            config["artifact_root"] = user_config["artifact_root"]
        # Deep merge artifacts section
        if "artifacts" in user_config:
            config["artifacts"].update(user_config["artifacts"])
    return config

def get_artifact_path(artifact_type: str) -> str:
    """Get path for artifact type (plans, designs, progress)."""
    config = get_config()
    return config["artifacts"].get(artifact_type, DEFAULTS["artifacts"].get(artifact_type))

def compute_artifact_root(artifact_paths: dict) -> str:
    """Compute common prefix from artifact paths."""
    if not artifact_paths:
        return "llm"

    paths = list(artifact_paths.values())
    if len(paths) == 1:
        parent = os.path.dirname(paths[0])
        return parent if parent else "."

    # Find common prefix
    try:
        common = os.path.commonpath(paths)
        # Return llm if no meaningful common prefix
        return common if (common and common != ".") else "llm"
    except ValueError:
        # No common path (different drives on Windows, etc.)
        return "llm"

def get_config_for_injection() -> str:
    """Get config formatted for session hook injection."""
    # Read user config directly to check if artifact_root is user-provided
    user_config = {}
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            user_config = json.load(f)

    config = get_config()

    # Compute artifact_root if not explicitly set by user
    if "artifact_root" in user_config:
        artifact_root = user_config["artifact_root"]
    else:
        # Compute from user-provided artifact paths only (not merged with defaults)
        user_artifacts = user_config.get("artifacts", {})
        if user_artifacts:
            artifact_root = compute_artifact_root(user_artifacts)
        else:
            # No user config, use default
            artifact_root = DEFAULTS["artifact_root"]

    # Format for injection
    lines = [
        "<superpowers-config>",
        f"artifact_root: {artifact_root}",
        "artifact_paths:"
    ]

    for key, path in config.get("artifacts", {}).items():
        lines.append(f"  {key}: {path}")

    lines.append("</superpowers-config>")

    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--inject":
            print(get_config_for_injection())
        else:
            print(get_artifact_path(sys.argv[1]))
    else:
        print(json.dumps(get_config(), indent=2))
