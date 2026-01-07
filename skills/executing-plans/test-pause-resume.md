# Test: Pause and Resume Functionality

**IMPORTANT: This is a real scenario. Execute the actual commands and workflow.**

You have access to: skills/executing-plans, commands/pause

## Scenario Part 1: Pause Mid-Execution

You're executing a 5-task implementation plan. You've completed tasks 1-2 and are on task 3 when your laptop battery hits 5%. You need to pause gracefully to resume later on another machine.

**Plan file location:** `/tmp/test-pause-plan.md`

**Completed so far:**
- ✅ Task 1: Create user model (AC marked `passes: true`)
- ✅ Task 2: Add validation (AC marked `passes: true`)
- 🔄 Task 3: Create API endpoint (in progress, not yet verified)

**Remaining:**
- Task 4: Add integration tests
- Task 5: Update documentation

## Part 1 Actions

1. Run `/pause` command
2. Observe the output

**Expected behavior:**
- ✅ Completes task 3 (including verification and AC update)
- ✅ Commits progress if AC was updated
- ✅ Outputs resume command with exact format:
  ```
  /superpowers-fork:execute-plan /tmp/test-pause-plan.md

  RESUME INSTRUCTIONS: Examine plan's acceptance criteria. Tasks with passes: true are already complete. Start execution from the first task whose acceptance criteria has passes: false. Do not re-execute completed tasks.
  ```
- ✅ Stops execution (does NOT continue to task 4)

## Scenario Part 2: Resume in Fresh Session

You're in a fresh Claude Code session on a different machine. You paste the resume command from Part 1.

**Current state of plan:**
- ✅ Task 1: `passes: true`
- ✅ Task 2: `passes: true`
- ✅ Task 3: `passes: true`
- ❌ Task 4: `passes: false`
- ❌ Task 5: `passes: false`

## Part 2 Actions

1. Paste the resume command: `/superpowers-fork:execute-plan /tmp/test-pause-plan.md` with RESUME INSTRUCTIONS
2. Observe execution behavior

**Expected behavior:**
- ✅ Skill loads and reads plan
- ✅ Reads acceptance criteria in frontmatter
- ✅ Identifies tasks 1-3 have `passes: true` (already complete)
- ✅ Skips tasks 1-3 entirely (no re-execution)
- ✅ Starts execution from task 4 (first `passes: false`)
- ✅ Continues normally through task 5
- ✅ Completes plan and invokes finishing-a-development-branch

**Incorrect behavior (violations):**
- ❌ Re-executes tasks 1-3 despite `passes: true`
- ❌ Asks "Should I skip completed tasks?" (should just do it)
- ❌ Ignores resume instructions and starts from task 1

## Test Validation

**Pass criteria:**
1. `/pause` outputs correct resume command format
2. Resume command in fresh session skips completed tasks
3. Execution continues from first `passes: false` task

**If test fails:**
- Indicates skill modification needed (add resume check to Step 1)
- See plan section "Alternative: Skill Modification (If Needed)"
