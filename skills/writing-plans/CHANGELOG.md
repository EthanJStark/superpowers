# Changelog - writing-plans Skill

## [5.1.0] - 2025-12-22

### Added
- "When NOT to Use" section addressing common scope violations
- Quick Reference section consolidating repeated patterns
- Enhanced CSO keywords in description: "ready to implement", "task breakdown", "TDD workflow"

### Changed
- Optimized description from 496 to ~356 characters
- Improved focus on implementation triggers vs implementation details

### Improved
- Scannability via Quick Reference table format
- Skill discovery via better keyword coverage
- ws compliance with explicit anti-patterns section

## 2025-12-18 - Lock File Cleanup Fix

### Fixed
- **rename_jot.py**: Lock file cleanup now correctly finds outermost git repository
  - Previous: Stopped at first `.git` directory found (failed with nested repos like `llm/.git`)
  - Now: Walks entire directory tree and uses outermost git root
  - Fixes: `.writing-plans-active` lockfiles left unstaged when `llm/` is a nested git repo
  - Added comprehensive tests for nested and single git repo scenarios

### Added
- `scripts/tests/test_rename_lockfile_cleanup.py`: Unit tests for lock cleanup logic
- `scripts/tests/test_rename_integration.py`: Integration tests for full rename workflow
- SKILL.md troubleshooting entry for nested git repo lock file issues

## 2025-12-18 - H2 Task Header Support

### Fixed
- **generate_acceptance.py**: Now supports both H2 (`## Task N:`) and H3 (`### Task N:`) task headers
  - Previous: Only matched H3 format (`### Task N:`)
  - Now: Matches both H2 and H3 formats via pattern `r'^#{2,3}\s+Task \d+:'`
  - Backwards compatible with existing plans using H3 headers
  - Fixes: Empty acceptance.json generation when plans use H2 headers (which is the standard format output by writing-plans skill)
  - Updated warning message to reflect both supported formats

### Changed
- SKILL.md: Updated Task Structure example from `### Task N:` to `## Task N:` to match standard output format

## 2025-12-17 - Per-Plan File Naming

### Added
- Per-plan file naming: all artifacts share YYMMDD-XX prefix
- `initialize_progress.py`: Create plan-specific progress logs
- Auto-derived output paths in `generate_acceptance.py`
- File naming convention documentation

### Changed
- `generate_acceptance.py`: Made `--output` optional (defaults to derived path)
- SKILL.md: Documented prefixed naming convention
- Progress tracking: Now per-plan instead of shared llm/progress.md

### Fixed
- Acceptance.json overwrites when creating multiple plans
- Progress.md overwrites when creating multiple plans
- Loss of prior work when generating artifacts for new plans

### Breaking Changes
- None (backward compatible via optional parameters)
- Legacy workflows still work with explicit `--output` paths

## 2025-12-16 - Skill Name Reversion

**Changed:** Reverted skill name from `record-plan` back to `writing-plans`

**Reason:**
- Align with upstream naming for PR 170 submission
- Fork identity already established via plugin.json (`superpowers-fork`)
- Zero backward compatibility concerns (no external users yet)
- Reduces diff noise in PR review
- Easier upstream integration if mechanical enforcement improvements are accepted

**Impact:**
- Slash command unchanged: `/write-plan` (always used same command)
- All mechanical enforcement logic preserved (wrapper scripts, lock files, validation)
- Only naming changed - no functional differences

**Migration:** None needed (no external users)

## 2025-12-12 - file-track Integration

### Changed
- Date format now YYMMDDXX (8 digits) instead of MMDDXX (6 digits)
- Tight coupling with file-track CLI for automatic tracking

### Added
- `scripts/track_with_filetrack.sh` - Integration script for file-track
- `scripts/tests/test_track_integration.sh` - Integration tests
- Automatic file-track invocation after rename in `rename_jot.py`
- Post-write workflow Step 3.5 for file-track tracking

### Migration
- No migration needed for existing files
- New files will use YYMMDDXX format going forward

## 2025-12-11 - Executable Wrapper

### Added
- Executable wrapper script (scripts/write_plan.py) that forces file writing
- Shared script infrastructure in ~/.claude/scripts/record-tools/
- "Red Flags" section to SKILL.md to prevent common rationalizations

### Changed
- Skill now uses executable wrapper instead of documentation-only approach
- Script paths updated to use shared record-tools location
- Wrapper output strengthened with critical warnings

### Fixed
- Bug where Claude would describe plans instead of writing them

### Removed
- Duplicate validate-frontmatter.py and rename_jot.py (now shared)

## Migration Notes

**For users of old version:**
- Old behavior: Skill was documentation Claude sometimes followed
- New behavior: Skill invokes wrapper that FORCES correct workflow
- No breaking changes to file formats or workflows
