# Superpowers Configuration

## Overview

Superpowers supports user-level configuration via `~/.config/superpowers/config.json` following XDG Base Directory conventions.

## Configuration File Location

**Path:** `~/.config/superpowers/config.json`

**Format:** JSON

**Scope:** User-level (applies to all projects)

## Artifact Destinations

Control where skills write plans, designs, and progress files.

### Schema

```json
{
  "artifact_root": "llm",
  "artifacts": {
    "plans": "relative/path/to/plans",
    "designs": "relative/path/to/designs",
    "progress": "relative/path/to/progress"
  }
}
```

**Fields:**
- `artifact_root` (optional): Root directory for artifact storage. If omitted, computed from common prefix of artifact paths. Used for communicating with users and for artifact-bridge integration.
- `artifacts`: Specific paths for different artifact types

Paths are relative to working directory. Skills append filename patterns.

### Defaults

```json
{
  "artifact_root": "llm",
  "artifacts": {
    "plans": "llm/implementation-plans",
    "designs": "llm/designs",
    "progress": "llm"
  }
}
```

### Example Configurations

**llm-preferred (fork default):**
```json
{
  "artifact_root": "llm",
  "artifacts": {
    "plans": "llm/implementation-plans",
    "designs": "llm/designs",
    "progress": "llm"
  }
}
```

**docs-preferred (upstream style):**
```json
{
  "artifact_root": "docs",
  "artifacts": {
    "plans": "docs/plans",
    "designs": "docs/designs",
    "progress": "docs"
  }
}
```

**Custom structure:**
```json
{
  "artifact_root": ".claude",
  "artifacts": {
    "plans": ".claude/plans",
    "designs": "architecture/designs",
    "progress": ".claude"
  }
}
```

## Skills That Use Config

- **writing-plans:** Reads `artifacts.plans` for default `--target-dir`
- **brainstorming:** Uses `artifacts.designs` for design document output
- **executing-plans:** (future) Will use `artifacts.progress` for progress tracking

## Creating Initial Config

```bash
mkdir -p ~/.config/superpowers
cat > ~/.config/superpowers/config.json <<'EOF'
{
  "artifact_root": "llm",
  "artifacts": {
    "plans": "llm/implementation-plans",
    "designs": "llm/designs",
    "progress": "llm"
  }
}
EOF
```

## Fallback Behavior

If `~/.config/superpowers/config.json` does not exist, skills use built-in defaults (shown above).

## Per-Invocation Overrides

Config sets defaults. Most skills support per-invocation overrides:

```bash
# Override plans directory for one invocation
write_plan.py --target-dir docs/architecture
```

Config file + override flags provide flexibility without rigidity.

## Artifact-Bridge Integration

The `artifact_root` field enables integration with [artifact-bridge](https://github.com/your-org/artifact-bridge) for automatic artifact watching and browser synchronization.

### How artifact-bridge Discovers Watch Paths

Artifact-bridge can read superpowers config to discover watch paths:

```python
# In artifact-bridge discover_watch_paths():
from pathlib import Path
import json

superpowers_config = Path.home() / ".config" / "superpowers" / "config.json"
if superpowers_config.exists():
    data = json.loads(superpowers_config.read_text())
    artifact_root = data.get("artifact_root", "llm")
    # Add to watch paths discovery
    watch_paths.append(artifact_root)
```

### Auto-Computation

If `artifact_root` is not explicitly set, it's computed from the common prefix of artifact paths:

**Examples:**
- `["llm/plans", "llm/designs", "llm"]` → `artifact_root: "llm"`
- `["docs/plans", "docs/designs"]` → `artifact_root: "docs"`
- `[".claude/plans", "architecture/designs"]` → `artifact_root: "."` (no common prefix)

### Future Integration

This integration is currently documentation-only. Full artifact-bridge integration is planned for a future release. The config schema is ready to support it.
