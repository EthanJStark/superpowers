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

## Worktree-Safe Setup

**For users working with git worktrees:** Artifact-bridge provides a centralized storage system that makes artifacts resilient to worktree operations.

### The Problem

When using git worktrees, each worktree has its own working directory. If artifacts are stored directly in `<worktree>/llm/`, you face two issues:

1. **Duplication:** Each worktree has separate `llm/` directories with potentially different content
2. **Loss on deletion:** Deleting a worktree removes its `llm/` directory and all artifacts

### The Solution: Centralized Artifacts

Artifact-bridge's `repo link` command creates a stable canonical store at `~/.artifacts/repos/<repo_id>/llm` and symlinks each worktree to it:

```bash
# In your main worktree
cd ~/dev/my-project
artifact-bridge repo link

# Link all existing worktrees
artifact-bridge repo link --all-worktrees
```

**What happens:**
1. Generates stable repo ID (survives remote URL changes)
2. Creates `~/.artifacts/repos/<repo_id>/llm/` (canonical store)
3. Moves existing `llm/` contents to canonical store
4. Creates symlink: `<repo>/llm` → `~/.artifacts/repos/<repo_id>/llm`

**Benefits:**
- **Worktree-safe:** All worktrees share the same artifacts via symlinks
- **Deletion-safe:** Artifacts survive worktree deletion
- **Move-safe:** Repo ID persists even if repository moves or remote changes

### Integration with Superpowers Config

Artifact-bridge respects the `artifact_root` field from superpowers config:

```bash
# If your superpowers config uses artifact_root: "docs"
# artifact-bridge will use "docs" instead of "llm"
artifact-bridge repo link  # Creates ~/. artifacts/repos/<repo_id>/docs
```

**Override if needed:**
```bash
artifact-bridge repo link --artifact-root custom
```

### Checking Link Status

```bash
# Show current repository's link status
artifact-bridge repo status

# Example output:
# Repo ID: github-acme-widgets__a1b2c3
# Canonical store: ~/.artifacts/repos/github-acme-widgets__a1b2c3/llm
# Status: ✅ Linked (symlink intact)
```

### Healing Broken Links

If symlinks break (e.g., after manual directory operations):

```bash
# Heal current repository
artifact-bridge repo heal

# Heal all repositories under a directory
artifact-bridge repo heal --search-root ~/dev
```

### Recommended Workflow

1. **First-time setup:** Run `artifact-bridge repo link` in your main worktree
2. **New worktrees:** Run `artifact-bridge repo link` after creating each worktree (or use `--all-worktrees` once)
3. **Periodic health check:** Run `artifact-bridge repo heal --search-root ~/dev` to catch any issues

This setup ensures your artifacts remain safe and accessible regardless of worktree operations.
