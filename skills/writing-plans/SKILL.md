---
name: writing-plans
description: Use when design is complete, ready to implement, and need task breakdown with exact file paths - creates TDD-focused implementation plans with verification steps. Mechanically enforced via wrapper script (invokes wrapper and writes file, never describes in chat). Writes plans only, never executes them. Lock file enforcement prevents unauthorized writes.
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**FIRST ACTION (mandatory):** Invoke wrapper script - DO NOT describe plan in chat first:

**Step 1: Locate the script**
```bash
find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/write_plan.py" 2>/dev/null | head -1
```

**Step 2: Invoke with the path from Step 1**
```bash
python3 <path-from-step-1> \
  --working-dir <working-directory> \
  --plan-name <descriptive-name> \
  --artifact-root <working-directory>/llm
```

**Note:** Command substitution `$(...)` doesn't work in Bash tool execution environment, so use two-step approach.

## When NOT to Use

**Don't use writing-plans for:**
- Executing existing plans → Use `superpowers-fork:executing-plans`
- Quick prototypes/exploration → No plan needed, just implement
- Project conventions → Use CLAUDE.md instead
- One-off solutions → Implement directly

**Common mistake:** "I see a plan file, I should execute it"

**Reality:** writing-plans writes, executing-plans executes. Never cross boundaries.

## Quick Reference

### Invoke Wrapper (FIRST ACTION)

**❌ DANGEROUS: Do NOT use non-deterministic find pattern**

```bash
# DON'T: Can select stale cache when multiple versions exist
SCRIPT=$(find ~/.claude/plugins/cache -path "*/scripts/write_plan.py" 2>/dev/null | head -1)
python3 $SCRIPT --args
```

**✅ SAFE: Two-step manual approach**

```bash
# Step 1: Find script path
find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/write_plan.py" 2>/dev/null | head -1

# Step 2: Invoke with path from step 1
python3 <path-from-step-1> \
  --working-dir <working-directory> \
  --plan-name <descriptive-name> \
  --artifact-root <working-directory>/llm
```

**Note:** Command substitution `$(...)` doesn't work in Bash tool execution environment, so use two-step approach.

**Why two-step is safe:** User manually copies correct path between steps, verifying the selected version before execution.

**Best practice (if available):** Use `${CLAUDE_PLUGIN_ROOT}/skills/writing-plans/scripts/write_plan.py` when environment variable is available.

### Post-Write Workflow

| Step | Action | Script | Required |
|------|--------|--------|----------|
| 0 | Copy from staging (if plan mode) | `cp ~/.claude/plans/<name>.md <working-dir>/llm/...` | Conditional |
| 1 | Validate frontmatter | `validate-frontmatter.py` | Yes |
| 2 | Rename with sequence | `rename_jot.py` | Yes |
| 3 | ~~Generate acceptance~~ DEPRECATED | ~~generate_acceptance.py~~ | No |
| 4 | Initialize progress | `initialize_progress.py` | Optional |

### Then STOP

writing-plans writes plans only. Never executes them.

## Mechanical Enforcement

**This is NOT optional. This is NOT guidance. This is MANDATORY.**

**Production incident (2025-12-18):** Agent received explicit instruction "Use the writing-plans skill exactly as written" but skipped wrapper script entirely.

**Lock file enforcement:**
1. Wrapper creates `.writing-plans-active` lock file in artifact_root (llm/)
2. Write tool can ONLY create plan if lock exists
3. Attempting Write without lock will FAIL
4. Lock is removed from artifact_root after rename script completes

**You cannot write the plan without invoking wrapper first. The system prevents it.**

**Previous incident (2025-12-13):** Agent skipped wrapper despite warnings. File never registered with file-track. Now mechanically enforced via lock file pattern.

**DO NOT before invoking wrapper:**
- Describe plan content in chat
- "Show" the plan structure
- Output plan deliverables/tasks
- List what the plan will contain

**"Create a plan" = invoke wrapper script immediately. Nothing else.**

**Execution Mode:** This skill has an executable wrapper that FORCES file writing.

**How it works:**
1. You invoke the wrapper script: `write_plan.py` (auto-located in plugin cache)
2. The wrapper prints directives: "USE WRITE TOOL to create file at X"
3. You MUST follow the directives - no describing, only executing
4. The wrapper guides you through post-write workflow

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:**
- **In plan mode:** Write to `~/.claude/plans/<plan-name>.md` (staging area, as specified by plan mode system prompt)
- **In regular mode:** Write to `<working-directory>/<target-dir>/<plan-name>.md`
  - Default: `<working-directory>/llm/implementation-plans/<plan-name>.md`
  - Configurable via `--target-dir` parameter

**Note:** The target directory structure is workflow-specific. The default assumes an `llm/` directory pattern, but this can be customized for projects with different conventions.

**Config:** Default target directory can be customized in `~/.config/superpowers/config.json`:
```json
{
  "artifacts": {
    "plans": "your/preferred/path"
  }
}
```

**Note:** After writing, the file will be renamed to `YYMMDD-XX-<slug>.md` format by the rename script (where YYMMDD is year/month/day, XX is auto-sequenced). If written to staging area, it must be copied to the working directory's target directory before rename.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers-fork:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

**IMPORTANT:** The "For Claude" instruction above is FOR THE EXECUTOR (future session using executing-plans), NOT for writing-plans. When you write this header, you are creating instructions for a future Claude - not instructions for yourself.

## File Requirements

**Every plan file MUST include these elements:**

1. **First line:** `<!-- jot:md-rename -->` (required for rename script detection)

2. **YAML frontmatter** (required for metadata and indexing):
   ```yaml
   ---
   title: Clear, descriptive title
   date: YYYY-MM-DD  # Current date
   type: implementation-plan
   status: draft      # Or: active, completed, archived
   tags: [relevant, tags, here]
   project: PROJECT-KEY  # Optional: e.g., NPCP-2495
   phase: ep001          # Optional: project phase
   acceptance:
     - id: criterion-id
       category: functional
       description: What to verify
       steps:
         - "Step 1: Action"
         - "Step 2: Verification"
       passes: false
       notes: ""
   ---
   ```

3. **H1 heading:** Feature name

4. **Header section:** Goal, Architecture, Tech Stack (as shown above)

**If a Jira ticket is referenced** (e.g., NPCP-1234), it will be included at the beginning of the final filename: `YYMMDD-XX-NPCP-1234-<slug>.md`

## File Naming Convention

**All plan artifacts use the same YYMMDD-XX prefix:**

```
llm/implementation-plans/
  251217-01-auth-implementation.md          # Plan with acceptance in frontmatter
  251217-01-auth-implementation-progress.md  # Optional progress log
```

**Why:** Prevents overwrites when creating multiple plans. Acceptance criteria are in frontmatter, no separate JSON needed.

## Path Requirements

- ✅ **ALWAYS use absolute paths**: `<working-directory>/<target-dir>/file.md`
- ❌ **NEVER use relative paths**: `llm/implementation-plans/file.md`
- **Default target directory**: `llm/implementation-plans/` (can be overridden with `--target-dir`)
- **Git repository awareness**: Files are tracked relative to repository root, handling nested git repos correctly

The working directory is shown as "Working directory" in the environment context at the start of each conversation.

**Workflow flexibility:** Use `--target-dir` to override per-invocation, or set your preferred default in `~/.config/superpowers/config.json`. The default supports an `llm/` subdirectory pattern, but can be customized to match any project convention (e.g., `docs/plans/`, `planning/implementation/`).

**Nested git repositories:** If llm/ is its own git repository (has llm/.git), the tooling automatically finds the parent repository to ensure correct path tracking.

## Repository Detection

The writing-plans scripts automatically detect the git repository root and handle nested git repositories:

**Nested llm/ repositories:** If your llm/ directory is its own git repository (common pattern for keeping ephemeral docs separate), the scripts automatically skip past it to find the parent repository. This ensures file paths are tracked relative to the main project repository, not the nested llm/ repo.

**Example:**
- Working in `/Users/name/project/.claude/llm/plans/`
- llm/ has its own `.git` directory (nested repo)
- Scripts find parent `/Users/name/project/.claude/` (main repo)
- Paths reported as `llm/plans/file.md` (relative to main repo)

**Custom usage:**
```bash
# Step 1: Find script path
find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/write_plan.py" 2>/dev/null | head -1

# Step 2: Invoke with custom target directory
python3 <path-from-step-1> \
    --working-dir /path/to/repo \
    --plan-name my-feature \
    --target-dir docs/architecture \
    --artifact-root /path/to/repo/llm
```

This flexibility allows the writing-plans skill to work with different project organizational conventions while maintaining backward compatibility with existing "llm/" workflows.

## Enforcement Mechanism

**Lock file pattern:**
1. Wrapper creates `.writing-plans-active` in artifact_root (e.g., llm/)
2. Lock file contains authorized file path
3. Write tool can only create plan if lock exists (future: full integration)
4. Rename script removes lock from artifact_root after complete workflow

**Location:** Lock files are created in artifact_root directory to avoid cluttering repo root and to keep them hidden from git status (llm/ is typically in .gitignore).

**Current enforcement layers:**
- Lock file created by wrapper (implemented)
- Git pre-commit hook catches format violations (implemented)
- Future: Write tool gating for complete prevention

**Manual check (optional):**
```bash
# Step 1: Find script
find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/check_lock.py" 2>/dev/null | head -1

# Step 2: Run check
python3 <path-from-step-1> <working-dir> <file-path>
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Acceptance Criteria Generation

**When planning, generate detailed acceptance criteria in frontmatter:**

```yaml
---
acceptance:
  - id: derived-from-task-name
    category: functional  # or style, performance, security
    description: What this criterion verifies
    steps:
      - "Step 1: Specific action to perform"
      - "Step 2: What to verify"
      - "Step 3: Expected outcome"
      - "Step 4: Additional verification"
      - "Step 5: Final check"
    passes: false
    notes: ""
```

**Generating criteria from tasks:**

For each task in the plan, create 1-2 acceptance criteria:

1. **Functional criterion**: Verifies the feature works end-to-end
   - Test the happy path
   - Test error cases
   - Verify integration points

2. **Quality criterion** (if applicable): Verifies non-functional requirements
   - Performance benchmarks
   - Code quality standards
   - Security requirements

**Step granularity (5-10 steps per criterion):**
- Each step is one concrete action or verification
- Include setup steps (start service, navigate to URL)
- Include positive and negative test cases
- Include cleanup/verification steps

**Category guidelines:**
- `functional`: Feature works as specified
- `style`: UI/UX matches design
- `performance`: Meets performance requirements
- `security`: Passes security checks

**Example task → acceptance mapping:**

Task: "Implement JWT authentication endpoint"

Acceptance criteria:
```yaml
- id: jwt-auth-endpoint-validation
  category: functional
  description: JWT authentication endpoint validates tokens and handles errors
  steps:
    - "Step 1: Start server with 'npm run dev'"
    - "Step 2: Send POST /api/auth/login with missing token"
    - "Step 3: Verify 400 Bad Request response"
    - "Step 4: Send request with malformed token"
    - "Step 5: Verify 401 Unauthorized response"
    - "Step 6: Send request with expired token"
    - "Step 7: Verify 401 Unauthorized with 'Token expired' message"
    - "Step 8: Send request with valid token"
    - "Step 9: Verify 200 OK with user data"
    - "Step 10: Verify response includes userId and email"
  passes: false
  notes: ""

- id: jwt-auth-security-checks
  category: security
  description: JWT endpoint implements security best practices
  steps:
    - "Step 1: Attempt request without HTTPS (if enforced)"
    - "Step 2: Verify appropriate error or redirect"
    - "Step 3: Send request with injection attempt in token"
    - "Step 4: Verify token is sanitized/rejected"
    - "Step 5: Verify rate limiting works (send 100 requests)"
    - "Step 6: Verify later requests are rate-limited"
  passes: false
  notes: ""
```

## Remember

- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Red Flags - You're About to Violate the Skill

**Why you're reading this section:** You already rationalized around skill boundaries.

**Two violation types:**

### Violation 1: Not writing the plan file

**Stop. Delete any plan content you wrote. Go back and invoke wrapper script.**

If you caught yourself thinking:
- "I'll describe the plan structure first" → You're already violating. Stop now.
- "Let me show the plan content" → You're already violating. Stop now.
- "The wrapper is just guidance" → WRONG. The wrapper is mandatory.
- "I can write without invoking wrapper" → WRONG. Wrapper ensures correct workflow.
- "Plan is simple, skip wrapper" → WRONG. Wrapper prevents the bug this plan fixes.
- "Create a plan" means output in chat → WRONG. "Create" means invoke wrapper.
- "I remember how to write plans" → WRONG. Skills evolve. Always read current version.
- "Wrapper is optional guidance" → WRONG. Wrapper is mandatory. Creates lock file.
- "Too simple to need wrapper" → WRONG. Wrapper prevents the exact bug this incident shows.
- "I'll write first, adapt later" → WRONG. Write without lock = violation. Wrapper first, always.
- "Describing plan is helpful" → WRONG. Describing without writing = incomplete work. Invoke wrapper immediately.

**Production incident (2025-12-18):** Agent received explicit instruction "Use the writing-plans skill exactly as written" via `/superpowers-fork:write-plan` command, but completely ignored the skill and wrote the plan directly without invoking the wrapper script.

**Production incident (2025-12-13):** Agent described entire plan in chat instead of writing file. User had to explicitly correct: "You need to write that plan file."

**All of these mean: Delete any plan content. Invoke wrapper script. Follow its directives exactly.**

| Excuse | Reality |
|--------|---------|
| "I remember how to write plans" | Skills evolve. Always read current version. |
| "Wrapper is optional guidance" | Wrapper is mandatory. Creates lock file. |
| "Too simple to need wrapper" | Wrapper prevents the exact bug this incident shows. |
| "I'll write first, adapt later" | Write without lock = violation. Wrapper first, always. |
| "Describing plan is helpful" | Describing without writing = incomplete work. Invoke wrapper immediately. |

### Violation 2: Executing the plan after writing

**Stop. writing-plans does NOT execute plans.**

If you caught yourself thinking:
- "Plan header says use executing-plans, so I should execute" → WRONG. That's for the EXECUTOR, not writing-plans.
- "User asked to create plan for task 2, so I should do task 2" → WRONG. Create = write plan only.
- "Plan already exists, let me execute it" → WRONG. writing-plans writes, never executes.
- "I'll just start the first task" → WRONG. STOP after writing.

**Production incident:** 2025-12-13 - Agent saw existing plan, decided to execute using superpowers-fork:execute-plan. User had to interrupt: "This is a bug... writing-plans should write and STOP."

**Scope boundaries:**
- writing-plans = WRITE plans only
- executing-plans = EXECUTE plans only
- These are separate skills. Never cross boundaries.

### Violation 3: Reverting to generic file names

**Stop. Use prefixed names derived from plan filename.**

If you caught yourself thinking:
- "Just use acceptance.json, it's simpler" → WRONG. Overwrites previous work.
- "User can rename later" → WRONG. Files must be correctly named from creation.
- "Prefixing is optional" → WRONG. Prefixing is required (prevents overwrites).
- "Only prefix acceptance, not progress" → WRONG. All artifacts share prefix.

| Excuse | Reality |
|--------|---------|
| "Generic names are simpler" | Generic names overwrite. Always prefix. |
| "User didn't ask for prefixing" | Prefixing prevents data loss. Always use. |
| "Template references target.txt" | Legacy pattern. Ignore - use prefixed names. |
| "This plan won't have multiple" | Can't predict future. Always prefix. |

**All of these mean: Use derived paths from plan filename. No exceptions.**

## Post-Write Workflow

After writing the plan file, MUST complete these steps:

### Step 0: Copy from Staging (if in plan mode)

**How to know if you're in plan mode:** Check the system prompt at conversation start. If it specifies a path like `~/.claude/plans/<name>.md`, you're in plan mode.

**If file was written to `~/.claude/plans/`** (plan mode staging area), copy it to the working directory:

```bash
# Ensure target directory exists
mkdir -p <working-directory>/llm/implementation-plans

# Copy from staging to final location
cp ~/.claude/plans/<plan-name>.md <working-directory>/llm/implementation-plans/<plan-name>.md
```

**All subsequent steps operate on the file in `<working-directory>/llm/implementation-plans/`**, not the staging copy.

**If file was written directly to `<working-directory>/llm/implementation-plans/`**, skip this step.

**Note:** The staging copy in `~/.claude/plans/` can remain (user may want it for reference), or be deleted with `rm ~/.claude/plans/<plan-name>.md` if preferred.

### Step 0.5: Initialize Progress Log (Optional)

**Check if user wants per-plan progress tracking:**

Ask: "Would you like to initialize a progress log for this plan? (tracks cross-session state)"

**If YES:**

```bash
python3 ~/.claude/skills/writing-plans/scripts/initialize_progress.py \
    --plan-file <working-directory>/llm/implementation-plans/<renamed-file>.md
```

Output: `<renamed-file>-progress.md` (same directory as plan)

**If NO:** Skip this step.

**Why optional:** Not all plans need progress tracking. Use for:
- Multi-session feature work
- Complex implementations
- When resuming work across sessions

### Step 1: Validate Frontmatter

```bash
# Find script
find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/validate-frontmatter.py" 2>/dev/null | head -1

# Run validation
python3 <path-from-above> <absolute-path-to-written-file>
```

Expected output: `✓ Frontmatter validation passed`

If validation fails:
- Fix the reported errors in the frontmatter
- Re-run validation until it passes

### Step 2: Invoke Rename Script

```bash
# Find script
find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/rename_jot.py" 2>/dev/null | head -1

# Run rename
python3 <path-from-above> <absolute-path-to-written-file>
```

The script will:
- Rename file to `YYMMDD-XX-slug.md` format (where YYMMDD is year/month/day, XX is sequence number)
- Automatically track with file-track if available (silent fallback if not installed)

Expected output:
```
✓ Renamed plan-name.md → 251213-01-plan-name.md
```

**Note:** File tracking is automatic. Use `file-track` (TUI) or `file-track list` to browse created files.

### Step 3: Generate Acceptance Criteria (Optional)

**⚠️  DEPRECATED:** Acceptance criteria are now generated in frontmatter during plan creation.

~~**Check if user wants acceptance tracking:**~~

~~Ask: "Would you like to generate acceptance criteria for this plan?"~~

**Note:** This step is no longer needed. Acceptance criteria are included in plan frontmatter.

## Common Mistakes

### Mistake 1: Operating on staging file after copy
**Problem:** Running validation/rename on `~/.claude/plans/<name>.md` instead of `<working-directory>/llm/implementation-plans/<name>.md`

**Fix:** After Step 0 copy, ALL subsequent steps use the file in `llm/implementation-plans/`, not the staging copy

### Mistake 2: Forgetting to copy in plan mode
**Problem:** Validating/renaming staging file, then wondering why it's not in the correct location

**Fix:** Always check system prompt at conversation start. If in plan mode, Step 0 is mandatory

### Mistake 3: Using relative paths
**Problem:** Writing to `llm/implementation-plans/file.md` instead of absolute path

**Fix:** Always use `<working-directory>/llm/implementation-plans/file.md` where `<working-directory>` is from environment context

### Mistake 4: Skipping frontmatter validation
**Problem:** Rename script fails with cryptic errors due to invalid frontmatter

**Fix:** ALWAYS run validation (Step 1) before rename (Step 2). Fix all errors before proceeding

### Mistake 5: Trying to use command substitution in one line
**Problem:** Getting parse errors like `(eval):1: parse error near '('` when trying to use `SCRIPT_PATH=$(find...)` pattern

**Root cause:** The Bash tool passes commands through shell evaluation that doesn't support command substitution `$(...)` syntax

**Fix:** Use the two-step approach documented throughout this skill:
1. Run `find` command to get the path
2. Copy the path and use it in the next command

**Alternative (if desperate):** Wrap in bash: `bash -c 'SCRIPT_PATH=$(find...); python3 "$SCRIPT_PATH" ...'`

## Troubleshooting

### Script Path Issues

**Symptom:** Error like "can't open file '/skills/writing-plans/scripts/write_plan.py'"

**Cause:** Script path variable is empty or malformed, OR selected stale cache version

**Solution:**
1. Verify script exists: `find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/write_plan.py"`
2. Check output - should show one absolute path
3. **If multiple paths found:** You have multiple cache versions - use `${CLAUDE_PLUGIN_ROOT}` or manually select latest
4. If no path found: plugin not installed correctly - reinstall from marketplace
5. If path found but wrong version: Check `${CLAUDE_PLUGIN_ROOT}`, may need to restart session

**Prevention:** Use `${CLAUDE_PLUGIN_ROOT}/skills/writing-plans/scripts/write_plan.py` instead of `find` when available.

**Symptom:** Parse error with parentheses: `parse error near '('`

**Cause:** Shell evaluation doesn't support `$(...)` command substitution

**Solution:** Use two-step approach (documented throughout skill)

### Lock File Issues

**Symptom:** "Lock file not found" or permission errors

**Solution:**
1. Verify wrapper script was invoked first (creates lock file)
2. Check `.writing-plans-active` exists in artifact_root (e.g., llm/)
3. If missing: must invoke wrapper before Write tool

**Symptom:** Lock file left behind after rename script completes

**Cause:** Nested git repositories (e.g., `llm/.git`) can confuse git root detection

**Solution (v4.1.1+):** Fixed - rename script now finds outermost git repository, skipping nested repos

**Workaround (older versions):** Manually remove: `rm .writing-plans-active` from main repo root

**Symptom:** Lock file found in repo root instead of llm/

**Cause:** Old version of script or missing --artifact-root parameter

**Solution:**
1. Upgrade to latest plugin version (v5.0.2+)
2. Manually remove old lock: `rm .writing-plans-active`
3. Re-run wrapper with --artifact-root parameter (auto-included in v5.0.2+)

### Path Resolution Issues (generate_acceptance.py)

**⚠️  OBSOLETE:** This script is deprecated as of 2025-12-26.

~~**Symptom:** ValueError: 'path' is not in the subpath of 'cwd'~~

Acceptance criteria are now in plan frontmatter. No separate generation needed.

## STOP: Plan Writing Complete

**After completing post-write workflow, STOP. Do NOT execute the plan.**

**This skill's scope:**
- ✅ Write implementation plans
- ✅ Complete post-write workflow (validate, rename, track)
- ❌ **NOT** execute plans
- ❌ **NOT** dispatch subagents to implement
- ❌ **NOT** use executing-plans or subagent-driven-development

**Execution Handoff:**

After saving the plan, offer execution choice:

**"Plan complete and saved to `<path>`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers-fork:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers-fork:executing-plans

**Common Rationalization:**

"The plan header says 'REQUIRED SUB-SKILL: Use executing-plans' - I should execute it now"

**Reality:** That instruction is FOR THE EXECUTOR (future Claude session), NOT for this skill. writing-plans ONLY writes, never executes.

**Production incident:** 2025-12-13 - Agent saw existing plan, decided to execute it instead of stopping. User had to interrupt: "This is a bug... writing-plans should write and STOP."

## Testing Verification

**Date:** 2025-12-13
**Approach:** Mechanical enforcement (automate objective constraints)
**Method:** Lock file pattern + git pre-commit hook

**Test results:**
- ✅ Normal flow (wrapper → write → rename): Lock created and removed correctly
- ✅ Violation attempt (skip wrapper): Git hook rejects commit with clear error
- ✅ Manual validation (check_lock.py): Correctly identifies missing lock
- ✅ Error messages: Clear guidance on correct usage

**Evidence for automation approach:**
- Previous violation (2025-12-13) despite strong documentation warnings
- Principle: Mechanical constraints belong in code, not documentation
- Cost-benefit: 30 min implementation vs 2-3 hours iterating documentation

**Enforcement layers:**
1. Lock file (primary - prevents unauthorized writes)
2. Validation script (agent self-check)
3. Git hook (catches violations at commit time)

## Version History

### v5.1.1 (2025-12-23)
- Fixed: Lock files (.writing-plans-active) now created in artifact_root (llm/) instead of repo root
- Fixed: Lock files properly cleaned up from artifact_root after workflow completes
- Added: --artifact-root parameter to write_plan.py for configurable lock location
- Updated: rename_jot.py searches artifact_root first for lock file cleanup
- Improved: Lock files no longer clutter git status (hidden in llm/ which is typically in .gitignore)

### v5.1.0 (2025-12-22)
- Added "When NOT to Use" section for ws compliance
- Optimized description for better CSO with implementation triggers
- Added Quick Reference section for improved scannability
- Enhanced keyword coverage: "ready to implement", "task breakdown", "TDD workflow"

### v5.0.0 (2025-12-19)
- Namespace migration: Updated all skill references from `superpowers:` to `superpowers-fork:`
- Merged with upstream v4.0.0 improvements (cleaner structure, better execution handoff)
- Preserved all fork enforcement mechanisms and documentation

### v4.1.1 (2025-12-18)
- Fixed: Lock file cleanup failing with nested git repositories
- rename_jot.py now finds outermost git root instead of stopping at first .git
- Added troubleshooting entry for lock file cleanup with nested repos
- Handles common pattern where llm/ is its own git repository

### v4.1.0 (2025-12-18)
- **CRITICAL FIX:** Added mechanical enforcement for wrapper script invocation
- Added Mechanical Enforcement section with explicit "MANDATORY" language
- Enhanced Red Flags section with production incident examples (2025-12-18)
- Added rationalization table mapping excuses to reality
- Updated using-superpowers skill with writing-plans rationalizations
- Created comprehensive test suite (baseline, enforcement, refactor, integration)
- Created INCIDENT-REPORTS.md tracking production violations
- Fixed: Agents skipping wrapper despite explicit instructions

### v4.0.0 (2025-12-17)
- Breaking: Namespace migration from `superpowers:` to `superpowers-fork:`
- Updated all skill references for fork identity

### v3.7.0 (2025-12-13)
- Added lock file enforcement mechanism
- Added git pre-commit hook for validation
- Fixed path resolution issues in generate_acceptance.py
- Enhanced testing verification section
