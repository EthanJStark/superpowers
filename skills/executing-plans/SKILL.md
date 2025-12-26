---
name: executing-plans
description: Use when partner provides a complete implementation plan to execute - loads plan, reviews critically, executes all tasks continuously, stops only for blockers or ambiguity, reports when complete
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks continuously, report when complete or blocked.

**Core principle:** Continuous execution with stops only for blockers or ambiguity.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

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
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers-fork:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

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

## Progress Tracking

**Reading acceptance criteria:**

Acceptance criteria are in the plan file's frontmatter as the `acceptance` array:

```yaml
---
acceptance:
  - id: feature-verification
    category: functional
    description: What to verify
    steps: [...]
    passes: false
    notes: ""
```

**Updating passes status:**

After verifying all steps for a criterion succeed:

1. Update the `passes` field in frontmatter to `true`
2. Optionally add execution notes
3. Commit the change with message: "test: mark [criterion-id] as passing"

**DO NOT:**
- Modify id, category, description, or steps
- Remove acceptance criteria
- Add new criteria during execution
- Reorder criteria

## Reading Plan Frontmatter

**To read acceptance criteria:**

```python
import yaml

def read_acceptance_criteria(plan_file_path):
    """Read acceptance array from plan frontmatter."""
    with open(plan_file_path, 'r') as f:
        content = f.read()

    # Split frontmatter from content
    if not content.startswith('---'):
        return []

    parts = content.split('---', 2)
    if len(parts) < 3:
        return []

    frontmatter = yaml.safe_load(parts[1])
    return frontmatter.get('acceptance', [])
```

**To update passes status:**

Use Edit tool to update the specific criterion's `passes` field from `false` to `true`.

## Remember
- Review plan critically first
- Execute all tasks continuously (don't pause between tasks)
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop ONLY when blocked or need clarification, don't guess
