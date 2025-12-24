# Production-Tested Improvements

This fork of [obra/superpowers](https://github.com/obra/superpowers) adds mechanical enforcement and safety gates developed through real-world usage.

## Compatibility

All existing Superpowers workflows, commands, and skills work unchanged. Users familiar with the original can maintain their existing workflows.

## Key Improvements

### 1. Writing-Plans Automation Framework

Enhances the existing `writing-plans` skill with executable wrapper scripts that enforce plan creation through lock files and git pre-commit hooks.

- **Lock file mechanism** ensures plans exist before coding begins
- **Git pre-commit hooks** prevent commits without corresponding implementation plans
- **Shifts from documentation to mechanical constraints** - addresses incidents where agents rationalized away requirements

### 2. Automation Over Documentation Framework

A new guidance document establishing when to use code vs. documentation for skill requirements.

- **Clear decision criteria**: objective, programmatically detectable requirements should trigger automation
- **Reduces documentation churn** - when violations are 100% detectable, use automation
- **Framework for future skill development** - establishes pattern for similar enforcement needs

### 3. PR Creation Safety Gate

Adds mandatory user preview and approval before pull request creation in the `finishing-a-development-branch` skill.

- **Defense-in-depth approach**: skill-level approval gate + permission rules + system prompts
- **Preview-then-confirm pattern** prevents bypassing approval workflows through rationalization
- **Follows pattern from `jira-publisher` skill** - proven safety-critical workflow

### 4. Continuous Execution Pattern

Removes artificial 3-task batching checkpoints from `executing-plans`, allowing uninterrupted workflow through multiple tasks.

- **Improved development velocity** - no artificial pauses
- **Only genuine blockers cause pauses** - maintains quality gates
- **Preserves all safety checks** - verification still runs at appropriate times

### 5. Writing-Skills Governance

Strengthens skill modification governance with enhanced discoverability and rationalization counters.

- **Enhanced discoverability** of the writing-skills meta-skill
- **Rationalization counters** against "just adding a section" shortcuts
- **Clear guidance on TDD treatment vs. quick updates** - when skills need full testing methodology

### 6. Plugin Cache Documentation and Anti-Patterns

Comprehensive documentation of plugin cache behavior and elimination of vulnerable path resolution patterns.

- **Anti-pattern warnings** for `find ... | head -1` (non-deterministic when multiple cache versions exist)
- **${CLAUDE_PLUGIN_ROOT} documentation** - session-bound environment variable for safe script paths
- **Session binding mechanics** - explains why restart is required after updates
- **Cache diagnostics** - troubleshooting procedures for stale cache detection
- **Implementation plan cleanup** - replaced all vulnerable patterns with safe alternatives

**Problem solved:** Multi-source documentation failure where implementation plans taught non-deterministic patterns that could select stale plugin cache when multiple versions existed. Research identified that no documentation source explained session binding, cache version conflicts, or diagnostic procedures.

**Impact:** Prevents future stale cache bugs by teaching correct patterns and providing troubleshooting tools.

## Philosophy

**Automation over documentation** for objective constraints, while preserving judgment-based guidance for subjective decisions. Skills are TDD for documentation—we test first, then write documentation that makes tests pass, iterating to close loopholes where agents rationalize around requirements.

---

[View upstream project](https://github.com/obra/superpowers)
