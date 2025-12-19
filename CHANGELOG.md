# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2025-12-19

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
