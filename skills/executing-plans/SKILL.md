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

## Remember
- Review plan critically first
- Execute all tasks continuously (don't pause between tasks)
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop ONLY when blocked or need clarification, don't guess
