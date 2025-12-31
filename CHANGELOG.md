# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.4.0] - 2025-12-26

### Added
- Automated version management with Commitizen
- Pre-commit hooks for conventional commit validation
- Release script for streamlined version bumps
- GitHub-hosted plugin workflow documentation

### Changed
- Version bumping now automated based on conventional commits
- CHANGELOG generation automated from commit history

## [5.0.0] - 2025-12-19

## v5.4.0 (2025-12-30)

### Feat

- add ws shorthand command for writing-skills

### Fix

- prevent agent from awaiting background process in command skill execution

## v5.3.2 (2025-12-29)

### Fix

- add .cz.toml to version_files for auto-patching during releases

## v5.3.1 (2025-12-28)

## v5.3.0 (2025-12-28)

### Feat

- add marketplace version sync to release automation

## v5.2.0 (2025-12-26)

### Feat

- add automated release script with commitizen
- **executing-plans**: read acceptance from frontmatter
- **writing-plans**: add acceptance criteria generation

## v5.1.1 (2025-12-23)

### Feat

- inject artifact-root parameter to writing-plans wrapper
- **config**: inject artifact paths into session context
- **writing-plans**: v5.1.0 - CSO and scannability improvements
- **writing-plans**: add Quick Reference section for improved scannability
- **writing-plans**: optimize description for better CSO with implementation triggers
- **writing-plans**: add When NOT to Use section for ws compliance

### Fix

- remove lock files from artifact-root instead of repo root
- use artifact-root for writing-plans lock file location
- restore continuous execution in executing-plans skill

## v5.0.0 (2025-12-19)

### Feat

- merge writing-plans SKILL.md with v4 improvements
- restore writing-plans automation scripts
- add user config reader for artifact destinations

### Fix

- use superpowers-local-dev wrapper for local marketplace
- add root marketplace.json for local development testing
- complete namespace migration to superpowers-fork
- update namespace references to superpowers-fork in CLAUDE.md
- **writing-plans**: correctly cleanup lock files with nested git repos
- **writing-plans**: support H2 task headers in generate_acceptance.py

### Refactor

- update all skill namespace references from superpowers: to superpowers-fork:
- rename plugin to superpowers-fork to avoid upstream collision

## v3.7.1 (2025-12-17)

### Feat

- **writing-plans**: add initialize_progress script
- **writing-plans**: derive acceptance path from plan filename
- **writing-plans**: read default target-dir from user config
- add user config reader for artifact destinations
- **skills**: improve writing-skills discoverability
- replace writing-plans with record-plans

### Fix

- resolve plan path relative to output directory
- **config**: graceful fallback on malformed JSON
- address CodeRabbit security and quality issues
- revert plugin name to 'superpowers' to match skill namespace references
- replace command substitution with two-step approach
- replace $CLAUDE_PLUGIN_ROOT with dynamic path finder
- bundle scripts and fix plugin identity for writing-plans skill
- address CodeRabbit PR #170 review - module system and hardcoded values
- add rationalization counters to finishing-branch skill
- add approval gate to PR creation in finishing-branch skill
- update record-plan script paths to ~/.claude/scripts/
- replace emoji regex placeholder with working implementation

### Refactor

- **writing-plans**: add rationalization counters
- update skill name references from record-plan to writing-plans
- rename record-plan skill to writing-plans for upstream alignment
- **executing-plans**: remove batch pausing, enable continuous execution

### Major Release - Upstream v4.0.0 Integration

**Base:** Rebased onto obra/superpowers v4.0.0 (commit 80643c2)

### Added from Upstream
- **Skill Consolidations:** Merged 6 skills into 3 (systematic-debugging, test-driven-development, writing-skills)
- **Two-Stage Code Review:** Spec compliance review before code quality review in subagent-driven-development
- **Testing Infrastructure:** Added test frameworks and skill triggering tests
- **Skill Description Focus:** Improved "when to use" clarity across all skills

### Preserved from Fork
- **Writing-Plans Automation:** Lock file enforcement, wrapper scripts, git hooks (v4.1.0)
- **Safety Gates:** PR creation approval workflow in finishing-a-development-branch
- **Continuous Execution:** Removed artificial checkpoints in executing-plans
- **Configuration System:** User-configurable artifact destinations
- **Fork Documentation:** IMPROVEMENTS.md, CLAUDE.md, configuration docs

### Changed (BREAKING)
- **Skill Count:** 14 skills (down from 21 via consolidation)
- **Removed Skills:** sharing-skills, standalone debugging skills (now in systematic-debugging), testing-anti-patterns (now in test-driven-development), testing-skills-with-subagents (now in writing-skills)
- **Namespace:** Exclusively `superpowers-fork:` throughout all documentation

### Migration Guide
1. Update skill references if using consolidated skills: `systematic-debugging` now includes condition-based-waiting, defense-in-depth, root-cause-tracing
2. All writing-plans automation works unchanged
3. Namespace already migrated in v4.0.0, no additional changes needed

## [4.0.0] - 2025-12-17

### Changed (BREAKING)
- **Namespace migration**: Changed plugin name from `superpowers` to `superpowers-fork`
- All skill references updated from `superpowers:*` to `superpowers-fork:*`
- **Action required**: Update any external references to use new namespace
- **Reason**: Resolve name collision with upstream obra/superpowers in marketplace

## [3.7.1] - Previous releases

See git history for previous release notes.
