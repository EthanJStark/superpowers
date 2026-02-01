# Test Scenario: Worktree Isolation During Multi-Directory Investigation

## Purpose

Test that agent maintains worktree context when investigation requires checking files in other directories (reproduces Episode 2 scenario).

## Setup

1. Create main project repository with existing files
2. Create second repository with related data
3. Agent must investigate second repo while implementing in worktree

## Test Plan

### Scenario 1: Basic Isolation

**Given:**
- Worktree created: `.worktrees/test-isolation`
- Simple plan: Create 2 files in worktree

**When:**
- Agent executes plan with worktree parameter

**Then:**
- Both files created in `.worktrees/test-isolation/`
- Main repo `git status` shows clean
- Agent outputs worktree path confirmations

### Scenario 2: Multi-Directory Investigation

**Given:**
- Worktree created: `.worktrees/episode-investigation`
- Plan requires checking `/other-repo/data.txt` before implementation
- Plan creates 3 new files based on investigation

**When:**
- Agent executes plan
- Agent reads from `/other-repo/data.txt`
- Agent creates files based on investigation

**Then:**
- Agent reads from other repo successfully
- All created files in `.worktrees/episode-investigation/`
- Main repo `git status` shows clean
- Agent explicitly returns to worktree after investigation
- Agent outputs: "Returned to worktree: [path]"

### Scenario 3: Lost Context Detection

**Given:**
- Worktree created: `.worktrees/detection-test`
- Simulated agent confusion (manually `cd` to main repo mid-execution)

**When:**
- Agent attempts next task

**Then:**
- Agent detects: `pwd` doesn't match worktree path
- Agent outputs: "ERROR: Worktree context lost!"
- Agent stops execution
- Agent reports expected vs actual path

## Acceptance Criteria

- [ ] Scenario 1: All files in worktree only
- [ ] Scenario 2: Investigation successful, files in worktree only
- [ ] Scenario 3: Context loss detected and reported

## Expected Agent Behavior

### Before Each Task:
```
Validating worktree context...
Current directory: /path/to/.worktrees/test-isolation ✓
```

### After Each Task:
```
✓ Task N complete. Working in worktree: /path/to/.worktrees/test-isolation
```

### Post-Execution:
```
Post-Execution Checklist:
✓ Current directory: /path/to/.worktrees/test-isolation
✓ All work in worktree: 3 files modified
✓ Main repo clean: No changes
✓ Tests passing
```
