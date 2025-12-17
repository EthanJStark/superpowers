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
  "artifacts": {
    "plans": "relative/path/to/plans",
    "designs": "relative/path/to/designs",
    "progress": "relative/path/to/progress"
  }
}
```

Paths are relative to working directory. Skills append filename patterns.

### Defaults

```json
{
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
