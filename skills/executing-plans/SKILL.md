---
name: executing-plans
description: Use when partner provides a complete implementation plan to execute - loads plan, reviews critically, executes all tasks continuously, stops only for blockers or ambiguity, reports when complete
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks continuously, report when complete or blocked.

**Core principle:** Continuous execution with stops only for blockers or ambiguity.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## How This Skill Works

**The Skill tool loads this content synchronously into your context.** You then read and follow these instructions in your current response.

**After invoking the Skill tool:**
1. Announce you're using this skill
2. Read the plan file immediately
3. Start executing per the process below

**Red flag:** Thinking "I'll wait for the skill to complete" means you've misunderstood - YOU execute the plan by following this skill's guidance.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute All Tasks Continuously

Execute each task in sequence:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed
5. Move immediately to next task

**Continue executing until:**
- All tasks complete, OR
- You hit a blocker (see "When to Stop and Ask for Help" below)

**Do NOT stop between tasks to ask for feedback unless blocked.**

## Common Rationalizations for Stopping (Don't Do These)

**STOP means blocked, not:**
- ❌ "Completed several tasks, should check in"
- ❌ "Next tasks look complex, should get feedback first"
- ❌ "Been working a while, should pause"
- ❌ "Want to show progress"
- ❌ "Significant milestone reached"

**Unless blocked or unclear: keep executing.**

### Step 3: Report When Complete

After all tasks complete and verified:
- Show what was implemented
- Show verification output
- Run post-execution checklist (see below)
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers-fork:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## Post-Execution Checklist

**Before reporting completion, verify:**

### Isolation Verification (If Worktree Used):

- [ ] Current directory: `pwd` shows worktree path
- [ ] All work in worktree: `git status` in worktree shows changes
- [ ] Main repo clean: `cd [main-repo] && git status` shows no changes
- [ ] No contamination: `git status` doesn't show unrelated files

**Output to user:**
```
✓ All tasks complete
✓ Working directory: [worktree-path]
✓ All work isolated in worktree
✓ Main repository unchanged
✓ Ready for: git commit, push, PR creation
```

### General Verification (All Executions):

- [ ] All tasks marked complete in task list
- [ ] No ERROR or FAIL messages in output
- [ ] Tests passing (if applicable)
- [ ] Ready for next step (commit, PR, deploy)

### Example Post-Execution Output:

```
Executing Plan: Feature Implementation
Worktree: .worktrees/feature-x

Task 1: Write failing test ✓
Task 2: Implement feature ✓
Task 3: Verify tests pass ✓

Post-Execution Checklist:
✓ Current directory: /Users/user/project/.worktrees/feature-x
✓ All work in worktree: 3 files modified
✓ Main repo clean: No changes in /Users/user/project
✓ No contamination: Only feature-x files present
✓ Tests passing: All tests green

Ready for: git commit -m "feat: implement feature-x"
```

## Worktree Isolation (If Applicable)

**Detect worktree context:**
- If plan execution started with "start with a new worktree" instruction
- OR if currently in `.worktrees/` directory
- OR if `--worktree` parameter provided

**Then enforce isolation:**

### Before EVERY Task:

1. Run: `pwd`
2. Store expected path: `WORKTREE_PATH=[absolute-path-to-worktree]`
3. Verify: Current directory matches `WORKTREE_PATH`
4. If mismatch: **STOP** and report error:
   ```
   ERROR: Worktree context lost!
   Expected: [WORKTREE_PATH]
   Current: [pwd]

   You must return to worktree before continuing.
   Run: cd [WORKTREE_PATH]
   ```

### After EVERY Task:

1. Output: "✓ Task [N] complete. Working in worktree: [WORKTREE_PATH]"
2. Run: `pwd`
3. Verify: Still in worktree path
4. If not: **STOP** with same error as above

### Multi-Directory Investigation Pattern:

**If you need to investigate other directories:**
- Reading files from main repo or other repos: **OK** (use absolute paths)
- Writing files to main repo or other repos: **NOT OK**
- After investigation: **MUST** return to worktree: `cd [WORKTREE_PATH]`

**Red flag symptoms:**
- Using absolute paths to main repo: `/Users/user/project/src/...`
- Should be using relative paths from worktree: `./src/...`
- If using absolute paths, confirm they're inside worktree

### Example Validation:

```bash
# Before Task 1
pwd  # /Users/user/project/.worktrees/feature-x

# Execute Task 1...

# After Task 1
pwd  # Verify still: /Users/user/project/.worktrees/feature-x
echo "✓ Task 1 complete. Working in worktree: /Users/user/project/.worktrees/feature-x"

# Before Task 2
pwd  # Must still be: /Users/user/project/.worktrees/feature-x
```

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-execution (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan after you've reported blockers
- Fundamental approach needs rethinking mid-execution

**Don't force through blockers** - stop and ask.

### Red Flag: Lost Worktree Context

**Symptoms:**
- Using absolute paths to main repo when in worktree
- `pwd` shows main repo instead of `.worktrees/[name]`
- Files being created outside worktree directory

**Recovery:**
1. Identify expected worktree path
2. Return: `cd [worktree-path]`
3. Verify: `pwd` matches worktree path
4. Resume task execution

**Prevention:**
- Check `pwd` before each task
- Use relative paths (`./src/...`) not absolute (`/full/path/...`)
- After investigation, explicitly return to worktree

## Progress Tracking

**Acceptance criteria live in plan frontmatter:**

```yaml
---
acceptance:
  - id: feature-verification
    category: functional
    description: What to verify
    steps: [...]
    passes: false  # Update this after verification
    notes: ""      # Optional execution notes
```

**After verifying all steps for a criterion succeed:**

1. Use Edit tool to change `passes: false` to `passes: true`
2. Optionally add notes: `notes: "Verified at http://localhost:3000"`
3. Commit: `git commit -m "test: mark [criterion-id] as passing"`

**Example Edit:**

```
old_string: "    passes: false"
new_string: "    passes: true"
```

**DO NOT:**
- Modify id, category, description, or steps
- Remove acceptance criteria
- Add new criteria during execution
- Reorder criteria

## Integration

**Required workflow skills:**
- **superpowers-fork:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **superpowers-fork:writing-plans** - Creates the plan this skill executes
- **superpowers-fork:finishing-a-development-branch** - Complete development after all tasks

**Never:**
- Start implementation on main/master branch without explicit user consent

## Remember
- Review plan critically first
- Execute all tasks continuously (don't pause between tasks)
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop ONLY when blocked or need clarification, don't guess
