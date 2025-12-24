# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin** that provides a core skills library. Unlike traditional Node.js projects, this repository contains **no build system, no package.json, and no traditional test suite**. Skills are markdown documentation files that are loaded directly by Claude Code.

**Key Architecture:**

- `skills/` - 14 skills organized by category (testing, debugging, collaboration, meta) - consolidated from 21 in v4.0.0
- `commands/` - Slash commands that activate corresponding skills
- `agents/` - Agent definitions (e.g., code-reviewer)
- `hooks/` - Session lifecycle hooks (auto-loads skills system)
- `.claude-plugin/` - Plugin manifest and marketplace configuration
- `llm/` - Local-only planning documents (NOT tracked by git)

## Branch Strategy

**Main branch serves as source of truth:**
- Contains company marketplace configuration (marketplace.json)
- Includes fork-specific plugin identity
- Company Claude Code marketplace points to this branch
- Stable and ready for production use

**For upstream contributions:**
- Create feature branches from main: `pr/NUMBER-cleanup` or `feature/upstream-NAME`
- Add cleanup commits to remove fork-specific config
- Submit PR from cleanup branch to obra/superpowers
- Main branch retains fork identity

**For local development:**
- Use git worktrees (see Local Development Workflow below)
- Keeps main stable for marketplace while testing changes

## Development Workflow

### Creating New Skills

**Don't improvise.** Use the meta-skills that define the process:

1. **Read `skills/writing-skills/SKILL.md` first** - Complete TDD methodology for documentation
2. **Test with `skills/testing-skills-with-subagents/SKILL.md`** - Run baseline tests, verify skill fixes violations
3. **Contribute with `skills/sharing-skills/SKILL.md`** - Fork, branch, test, PR workflow

**TDD for Documentation Approach:**

- RED: Run baseline with subagent (without skill) - observe failures
- GREEN: Write skill that addresses violations - verify compliance
- REFACTOR: Close loopholes, tighten language against rationalization

### Local Plugin Development

#### Initial Setup (One-Time)

**First time setting up local development? Follow these steps:**

1. **Add the local marketplace wrapper:**
   ```bash
   # From parent directory (claude-code-resources/):
   /plugin marketplace add ./superpowers-local-dev

   # OR from main repo directory (superpowers/):
   /plugin marketplace add ../superpowers-local-dev
   ```

   **Important:**
   - The **command path** (what you type) should be **relative** starting with `./` or `../`
   - The **source field** in `marketplace.json` should use an **absolute path** to avoid path traversal security errors

   This registers a marketplace wrapper. The marketplace definition at `superpowers-local-dev/.claude-plugin/marketplace.json`
   contains an absolute path to the plugin directory: `/Users/ethan.stark/dev/claude-code-resources/superpowers`.

2. **Verify marketplace added:**
   ```bash
   /plugin marketplace list
   # Should show: superpowers-local-dev (no errors)
   ```

3. **Install the plugin from your local marketplace:**
   ```bash
   /plugin install superpowers-fork@superpowers-local-dev
   ```

**Why a wrapper directory?** The main repo's `.claude-plugin/marketplace.json` contains plugin publish metadata (for renaissance-marketplace), not marketplace definition. Claude Code requires marketplace definition at `.claude-plugin/marketplace.json`, so we use a separate wrapper directory to avoid conflicts.

#### Quick Start (Daily Workflow)

When developing superpowers locally and testing changes in Claude Code:

1. **Edit skills** in your local superpowers clone (e.g., `~/dev/claude-code-resources/superpowers/skills/`)
2. **Commit changes** to your branch (e.g., `integration/v4-consolidated`)
3. **Reload plugin** to reflect changes in Claude Code (paste both lines):
   ```bash
   /plugin uninstall superpowers-fork@superpowers-local-dev
   /plugin install superpowers-fork@superpowers-local-dev
   ```
4. **Test changes** in a new Claude Code session

**Important:** Plugin changes only take effect after reload. Skills are loaded at session start, so existing sessions won't see updates.

#### Switching Between Local and Marketplace Versions

**Your plugin identifiers:**
- `superpowers-fork@renaissance-marketplace` - Company marketplace version (published)
- `superpowers-fork@superpowers-local-dev` - Local development version (wrapper pointing to this repo)

**Switch TO local development:**
```bash
/plugin uninstall superpowers-fork@renaissance-marketplace
/plugin install superpowers-fork@superpowers-local-dev
# Then start new session
```

**Switch BACK to marketplace:**
```bash
/plugin uninstall superpowers-fork@superpowers-local-dev
/plugin install superpowers-fork@renaissance-marketplace
# Then start new session
```

**After editing local skills:**
```bash
# Commit changes (optional but recommended)
git add -A && git commit -m "your changes"

# Reload plugin (paste both lines together):
/plugin uninstall superpowers-fork@superpowers-local-dev
/plugin install superpowers-fork@superpowers-local-dev

# Start new Claude Code session to see changes
```

#### When to Uninstall/Reinstall vs Restart

**How plugin caching works:**
- Plugin code is cached when installed - changes to source files don't automatically reflect
- **Session binding:** Each session locks to specific cache directory on startup
- Skills are loaded at session start - they need a new session to reload
- Uninstall/reinstall forces cache refresh and reloads components
- **Restart alone is NOT sufficient** - must have new cache to bind to

**⚠️ CRITICAL: Restart is ALWAYS required after plugin changes**

"Restart alone is NOT sufficient - you need uninstall/reinstall"

**Why:** Claude Code sessions bind to plugin cache on startup. Even after cache updates:
- Running sessions remain bound to old cache
- New files/changes won't appear until restart
- `${CLAUDE_PLUGIN_ROOT}` continues pointing to old location

**Workflow:** Uninstall → Reinstall → Restart → Verify

**Decision matrix:**

| Scenario | Action | Why |
|----------|--------|-----|
| Changed skill content in source directory | Uninstall → Reinstall → Restart mandatory | Source changes don't affect cache; must propagate to cache and rebind session |
| Plugin update from marketplace | Uninstall → Reinstall → Restart mandatory | New cache created; must bind new session to it |
| Testing same skill twice | Restart (new session) | Rebind to ensure clean state |
| Switching between marketplace and local | Uninstall old → Install new → Restart mandatory | Different plugin identities require cache invalidation |
| Plugin not appearing in `/help` | Uninstall → Reinstall → Restart mandatory | Metadata not loaded; must clear and rebind |
| Script path not found error | Check ${CLAUDE_PLUGIN_ROOT}, then Uninstall → Reinstall → Restart | May be bound to stale cache |

**Always paste both commands together:**
```bash
/plugin uninstall superpowers@superpowers-dev
/plugin install superpowers@superpowers-dev
```

### Path Resolution Anti-Patterns

**❌ NEVER use `find ... | head -1` to locate plugin scripts:**

```bash
# DON'T: Non-deterministic when multiple cache versions exist
find ~/.claude/plugins/cache -path "*/scripts/*.py" 2>/dev/null | head -1
```

**Problem:** When multiple plugin cache versions exist (e.g., after updates), `find | head -1` can select a stale version instead of the active session's version.

**✅ ALWAYS use `${CLAUDE_PLUGIN_ROOT}` for script paths:**

```bash
# DO: Deterministic - uses active session's plugin version
${CLAUDE_PLUGIN_ROOT}/skills/skill-name/scripts/script-name.py
```

**✅ Alternative: Two-step manual pattern (safe):**

```bash
# Step 1: User locates and copies path
find ~/.claude/plugins/cache -path "*/skills/skill-name/scripts/script.py" 2>/dev/null | head -1

# Step 2: User pastes path from step 1
python3 <path-from-step-1> --args
```

**Why two-step is safe:** User manually verifies and copies the correct path between steps, preventing automated selection of wrong version.

**See also:** `llm/pattern-replacement-guide.md` for complete examples.

### Using ${CLAUDE_PLUGIN_ROOT}

**Environment variable set by Claude Code:** Points to the active plugin's cache directory for the current session.

**Value example:**
```bash
~/.claude/plugins/cache/temp_local_1234567890/
```

**Why it's important:**
- Session-bound: Always references the plugin version loaded when session started
- Portable: Works across different installations and users
- Safe: Immune to cache version conflicts

**Usage in skills:**

```bash
# Invoke Python script
python3 ${CLAUDE_PLUGIN_ROOT}/skills/writing-plans/scripts/write_plan.py --args

# Source bash functions
source ${CLAUDE_PLUGIN_ROOT}/skills/skill-name/helpers.sh

# Reference documentation
cat ${CLAUDE_PLUGIN_ROOT}/skills/skill-name/reference.md
```

**Usage in commands:**

Slash commands (e.g., `/superpowers-fork:brainstorm`) automatically have `${CLAUDE_PLUGIN_ROOT}` available when they spawn subagents or run scripts.

**Verification:**

```bash
# Check variable is set
echo $CLAUDE_PLUGIN_ROOT

# Check it points to superpowers plugin
ls ${CLAUDE_PLUGIN_ROOT}/skills/
```

Expected: Should list all skills directories

### Understanding Plugin Cache

**How plugin caching works:**

1. **Installation:** Plugin files copied from source to `~/.claude/plugins/cache/<directory>/`
2. **Session start:** Claude Code binds to specific cache directory, sets `${CLAUDE_PLUGIN_ROOT}`
3. **Session lifetime:** Same cache version used throughout session (no dynamic reload)
4. **Updates:** New version creates new cache directory (e.g., `temp_local_1234567891/`)

**Multi-version cache directories:**

After multiple plugin updates, you may see:
```bash
~/.claude/plugins/cache/
  temp_local_1766188090207/  # Old version (may still be in use by running session)
  temp_local_1766199234567/  # Newer version
  temp_local_1766201234567/  # Latest version
```

**Session binding (critical concept):**
- Each Claude Code session binds to ONE cache directory on startup
- Running sessions continue using their bound cache even after plugin updates
- New sessions use the latest cache directory
- **This is why restart is required after updates**

**Cache invalidation:**
- ✅ Happens on: Uninstall → Reinstall (removes old cache, creates new)
- ✅ Happens on: Plugin update (creates new cache directory)
- ❌ Doesn't happen on: Session restart without reinstall
- ❌ Doesn't happen on: File edits in source directory

**Common misconception:** "I edited the plugin source, so changes should appear"

**Reality:** Changes in source directory don't affect cache. Must uninstall → reinstall to propagate changes to cache, then restart to bind new session to updated cache.

#### Troubleshooting

**Issue:** Plugin error in `/doctor` output
- **Cause:** Stale plugin reference in `~/.claude/settings.json`
- **Fix:** Edit settings.json and remove the stale `enabledPlugins` entry

**Issue:** Script path not found (e.g., `write_plan.py`)
- **Cause:** Plugin not installed or cache cleared
- **Fix:** Reinstall plugin from marketplace

**Issue:** Skills don't update after editing
- **Cause:** Didn't reload plugin or start new session
- **Fix:** Uninstall → Reinstall → New session

#### Stale Plugin Cache Detection

**Symptoms:**
- Script not found errors despite plugin being installed
- Script exists but doesn't have expected feature/fix
- Different behavior between sessions

**Diagnostic procedure:**

```bash
# 1. Check all cached versions
find ~/.claude/plugins/cache -type d -name "superpowers-fork"

# 2. Check which version has the script/feature you need
find ~/.claude/plugins/cache -path "*/scripts/your-script.py" -exec ls -lh {} \;

# 3. Verify CLAUDE_PLUGIN_ROOT points to expected version
echo $CLAUDE_PLUGIN_ROOT
# Compare with versions from step 1

# 4. Check which version has recent changes
find ~/.claude/plugins/cache -type d -name "superpowers-fork" -exec stat -f "%Sm %N" -t "%Y-%m-%d %H:%M:%S" {} \;
```

**Resolution:**

If `${CLAUDE_PLUGIN_ROOT}` points to stale version:
1. Uninstall plugin: `/plugin uninstall superpowers-fork@superpowers-local-dev`
2. Reinstall plugin: `/plugin install superpowers-fork@superpowers-local-dev`
3. Start new session (existing session still bound to old cache)
4. Verify: `echo $CLAUDE_PLUGIN_ROOT` should show new directory

**Prevention:**

- Always use `${CLAUDE_PLUGIN_ROOT}/path/to/script` instead of `find ... | head -1`
- Follow uninstall → reinstall → restart cycle for all updates
- Paste both uninstall and install commands together to prevent partial updates

#### Cache Version Mismatch Detection

**Quick check for multiple versions:**

```bash
find ~/.claude/plugins/cache -type d -name "superpowers-fork" | wc -l
```

Expected: 1 (single version)
Concerning: 2+ (multiple versions - potential for confusion)

**If multiple versions found:**

```bash
# Check timestamps to identify latest
find ~/.claude/plugins/cache -type d -name "superpowers-fork" -exec ls -ld {} \;

# Check plugin.json versions
find ~/.claude/plugins/cache -path "*superpowers-fork*/.claude-plugin/plugin.json" -exec jq -r '.version' {} \; 2>/dev/null

# Compare with settings.json to see which is "installed"
grep -A 5 "superpowers-fork" ~/.claude/settings.json
```

**Clean up old versions (optional):**

Old cache directories can be manually removed if no sessions are using them:

```bash
# DANGER: Only do this with Claude Code fully quit
rm -rf ~/.claude/plugins/cache/temp_local_OLD_TIMESTAMP/
```

**Safer approach:** Uninstall → reinstall clears cache automatically.

### PR Creation Safety

**Approval pattern:** finishing-a-development-branch skill enforces preview-then-confirm for PR creation.

**Expected flow:**
1. User selects option 2 (Push and create PR)
2. Claude pushes branch
3. Claude shows PR title/body preview
4. Claude asks: "Create this PR? (yes/no)"
5. User must type "yes" to proceed

**Defense-in-depth:**
- Skill-level approval gate (primary)
- Permission rules in ~/.claude/settings.json (secondary)
- Permission system prompts on first use (tertiary)

**Similar patterns:**
- jira-publisher skill (safety-critical approval gates)
- Option 4 discard confirmation (typed "discard" required)

### Local Development with Worktrees

**Use git worktrees to test changes in isolation while keeping main stable for the company marketplace.**

**Creating a worktree for experiments:**

```bash
# From main repository (adjust path to your local clone)
cd ~/dev/superpowers  # or wherever you cloned this repo

# Create worktree with new branch
git worktree add .worktrees/feature-name -b feature/my-experiment

# Work in worktree
cd .worktrees/feature-name
# Edit skills, commit changes, then reload plugin:
/plugin uninstall superpowers-fork
/plugin install superpowers-fork
# (Paste both lines together)
```

**When satisfied with changes:**

```bash
# Return to main repository
cd ~/dev/superpowers  # or wherever you cloned this repo

# Merge feature branch
git merge feature/my-experiment

# Remove worktree
git worktree remove .worktrees/feature-name

# Delete feature branch (optional)
git branch -d feature/my-experiment
```

**Benefits:**
- Main directory always stable for marketplace
- Test changes in isolation without affecting running Claude sessions
- Run multiple worktrees for parallel experiments
- Easy cleanup when done

### Skill Structure Requirements

**Directory and Naming:**

```plaintext
skills/
  skill-name/           # lowercase-with-hyphens only (no special chars)
    SKILL.md            # Required: main skill content
    example.ts          # Optional: reusable tool/example code
    scripts/            # Optional: supporting utilities
    reference-docs.md   # Optional: heavy reference material
```

**Frontmatter (required in SKILL.md):**

```yaml
---
name: skill-name # Must match directory name exactly
description: Use when [trigger] - [what it does] # Appears in skill list
---
```

**Supporting Files Patterns:**

- Self-contained skill → Only `SKILL.md`
- Skill with reusable tool → `SKILL.md` + `example.ts` (see `condition-based-waiting`)
- Skill with heavy reference → `SKILL.md` + reference docs + `scripts/` (see `root-cause-tracing`)

### Skill Types and Treatment

1. **Discipline-Enforcing Skills** (e.g., `test-driven-development`, `verification-before-completion`)

   - Contain rigid rules tested against pressure scenarios
   - Follow exactly - don't adapt away the discipline

2. **Technique Skills** (e.g., `condition-based-waiting`, `root-cause-tracing`)

   - How-to guides with concrete steps

3. **Pattern Skills** (e.g., `brainstorming`, `systematic-debugging`)

   - Mental models and flexible patterns - adapt to context

4. **Reference Skills**
   - Heavy documentation, APIs, guides

The skill itself indicates which type it is.

## Testing Skills

**No traditional test suite exists.** Skills are tested using:

1. **Subagent Testing** - Spawn subagents with/without skill, compare behavior
2. **Pressure Scenarios** - Test if agents comply when tempted to skip steps
3. **Baseline Testing** - Run without skill to demonstrate violations
4. **TDD Cycle** - Iteratively tighten language to close loopholes

See `skills/testing-skills-with-subagents/SKILL.md` for complete methodology.

## Contributing Workflow

**Standard fork-based workflow:**

1. Fork repository (if you have `gh` CLI configured)
2. Create feature branch: `add-skillname-skill` or `improve-skillname-skill`
3. Create/edit skill following `writing-skills` guidelines
4. Test with subagents to verify behavior changes
5. Commit with clear message (avoid mentioning "Claude" in commits)
6. Push to your fork
7. Create PR to upstream

**Branch off `main`** - this is the primary branch.

## Version Management

Update plugin version in `.claude-plugin/plugin.json`:

```json
{
  "name": "superpowers",
  "version": "X.Y.Z",
  ...
}
```

Follow semantic versioning:

- MAJOR: Breaking changes to skill interfaces
- MINOR: New skills, backward-compatible improvements
- PATCH: Bug fixes, documentation improvements

## Important Notes

**llm/ Directory:**

- Contains local-only planning documents
- NOT tracked by git (per `.gitignore`)
- Safe for scratch notes, implementation plans
- Do NOT reference these files in skills or commits

**Skill References:**

- Skills are namespace-qualified: `superpowers-fork:skill-name`
- Use slash commands to activate: `/superpowers-fork:brainstorm`
- Session hook auto-loads `using-superpowers` at startup

**No Legacy Systems:**

- Skills overlay system removed in v2.0
- First-party skills system adopted in v3.0
- No backward compatibility with old skill formats

## Key Reference Files

**Essential reading for contributors:**

- `skills/writing-skills/SKILL.md` - How to create effective skills
- `skills/using-superpowers/SKILL.md` - How the skills system works
- `skills/testing-skills-with-subagents/SKILL.md` - Testing methodology
- `skills/sharing-skills/SKILL.md` - Contributing workflow
- `README.md` - Installation, quick start, skills overview

**Example skills demonstrating patterns:**

- `skills/systematic-debugging/SKILL.md` - Complex skill with flowchart (Graphviz DOT notation)
- `skills/condition-based-waiting/` - Skill with supporting TypeScript example
- `skills/brainstorming/SKILL.md` - Command-activated skill with clear triggers

**Supporting documentation in writing-skills:**

- `anthropic-best-practices.md` - Official Anthropic skill authoring guide
- `graphviz-conventions.dot` - Flowchart style rules
- `persuasion-principles.md` - Psychology of effective documentation

## Philosophy

Skills are TDD for documentation. Write tests (baseline runs) first, then write documentation that makes tests pass. Iterate to close loopholes where agents rationalize around requirements. The result: battle-tested process documentation that actually changes agent behavior.
