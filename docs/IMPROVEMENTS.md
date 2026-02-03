# Production-Tested Improvements

This fork of [obra/superpowers](https://github.com/obra/superpowers) adds mechanical enforcement and safety gates developed through real-world usage.

## Compatibility

All existing Superpowers workflows, commands, and skills work unchanged. Users familiar with the original can maintain their existing workflows.

## Key Improvements

### 1. Writing-Plans Automation Framework

Enhances the existing `writing-plans` skill with executable wrapper scripts that enforce plan creation through lock files and git pre-commit hooks.

- **Lock file mechanism** ensures plans exist before coding begins
- **Git pre-commit hooks** prevent commits without corresponding implementation plans

### 2. PR Creation Safety Gate

Adds mandatory user preview and approval before pull request creation in the `finishing-a-development-branch` skill.

- **Defense-in-depth approach**: skill-level approval gate + permission rules + system prompts
- **Preview-then-confirm pattern** prevents bypassing approval workflows through rationalization
- **Follows pattern from `jira-publisher` skill** - proven safety-critical workflow

### 3. Continuous Execution Pattern

Removes artificial 3-task batching checkpoints from `executing-plans`, allowing uninterrupted workflow through multiple tasks.

- **Improved development velocity** - no artificial pauses
- **Only genuine blockers cause pauses** - maintains quality gates
- **Preserves all safety checks** - verification still runs at appropriate times

### 4. Writing-Skills Governance

Strengthens skill modification governance with enhanced discoverability and rationalization counters.

- **Enhanced discoverability** of the writing-skills meta-skill
- **Rationalization counters** against "just adding a section" shortcuts
- **Clear guidance on TDD treatment vs. quick updates** - when skills need full testing methodology

### 5. Graceful Pause/Resume for Plan Execution

Adds `/pause` command for graceful interruption during plan execution with easy continuation in fresh sessions.

- **Structured pause workflow** - completes current task, updates acceptance criteria, commits progress
- **Resume instructions** - outputs copy-paste command referencing plan and acceptance criteria
- **Session continuity** - acceptance criteria (passes: true/false) enable skipping completed tasks
- **Quality preservation** - ensures clean handoff between sessions without losing progress

**Use case:** Long-running implementation plans that span multiple sessions, context management, or when switching focus mid-execution.

### 6. Version Consistency Automation

Adds pre-commit hook validation to prevent version drift between `.cz.toml` and `plugin.json`.

- **Automated validation** - runs on every commit to catch mismatches early
- **Clear error messages** - provides instructions for resolution when versions diverge
- **Prevention over correction** - blocks commits rather than fixing drift after deployment
- **Complements release automation** - ensures version bumps propagate correctly

**Problem solved:** Manual version management led to inconsistencies between commitizen configuration and plugin manifest, causing marketplace version mismatches.

**Impact:** Zero-tolerance enforcement prevents version drift at commit time rather than discovering issues during release.

### 7. Test Infrastructure Documentation

Establishes three-tier test artifact pattern with clear separation of concerns.

- **Personal TDD artifacts** (`llm/skill-tests/`) - RED-GREEN-REFACTOR iterations, git-ignored
- **Reusable test scenarios** (`skills/*/test-*.md`) - Clean test cases, committed for validation
- **Executable test infrastructure** (`tests/`) - Shared automation frameworks for CI/CD
- **Zero context cost** - Test files don't load until explicitly read, no performance impact
- **Upstream alignment** - Matches obra/superpowers test pattern while maintaining fork-specific structure

**Rationale:** Separates messy TDD development artifacts from clean, reusable test scenarios. Personal iteration stays local (no git noise), while committed test scenarios prove skills were tested and enable regression protection.

### 8. Git Worktrees Enhancements

Extends the `using-git-worktrees` skill with robust pre-flight checks and integration with plan execution.

- **Nested worktree detection** - Compares `git-dir` vs `git-common-dir` to detect if already in a worktree (works from any subdirectory)
- **Bare repository support** - Detects bare repos and guides all work to worktrees
- **Absolute path enforcement** - Prevents nested worktree creation from wrong paths
- **Executing-plans integration** - Post-execution checklist verifies work happened in worktree context

**Problem solved:** Agents creating worktrees from within existing worktrees, causing nested creation at wrong paths. Old `.git` file check only worked at repo root.

### 9. Acceptance Criteria Frontmatter System

Replaces separate JSON files with YAML frontmatter in plan files for acceptance criteria tracking.

- **Single source of truth** - Criteria live in plan file frontmatter, not separate files
- **Progress tracking** - `passes: true/false` and `notes` fields updated during execution
- **Session continuity** - Completed tasks (passes: true) skipped in fresh sessions
- **Validation script** - `validate-frontmatter.py` ensures schema compliance

**Deprecated:** `acceptance.json` files and `generate_acceptance.py` script.

### 10. Configuration System

Adds user-configurable artifact paths with smart defaults.

- **User config** - `~/.config/superpowers/config.json` for artifact path overrides
- **Smart defaults** - Merges user config with built-in defaults
- **Session injection** - `config.py --inject` embeds config in session start hook
- **Artifact root computation** - Auto-computes common prefix from artifact paths

**Use case:** Users with different project structures can customize where plans, designs, and progress files are stored.

### 11. Release Automation

Adds Commitizen-based release workflow with marketplace synchronization.

- **Conventional commits** - Version determined from commit types (feat→minor, fix→patch)
- **Automated bumping** - `release.sh` handles version bump, changelog, and git tag
- **Marketplace sync** - Updates local marketplace manifest with new version
- **Multi-repo coordination** - Provides instructions for syncing both repositories

**Problem solved:** Manual version management led to inconsistencies between plugin and marketplace versions.

## Philosophy

**Mechanical constraints belong in code, not documentation.** When requirements are 100% objective and programmatically detectable (format, structure, regex-enforceable rules), automate them. Save documentation for judgment calls where human-like reasoning matters.

**Skills are TDD for documentation**—we test first, then write documentation that makes tests pass, iterating to close loopholes where agents rationalize around requirements.

---

[View upstream project](https://github.com/obra/superpowers)
