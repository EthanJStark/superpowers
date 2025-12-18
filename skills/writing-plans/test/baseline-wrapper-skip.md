# Baseline Test: Wrapper Script Skip

## Scenario
User runs `/superpowers-fork:write-plan` command with explicit instruction:
"Use the writing-plans skill exactly as written"

Task: Create implementation plan for feature X

## Pressure Types
1. **Competence pressure**: Agent believes it knows how to write plans
2. **Efficiency pressure**: Wrapper invocation seems like extra step
3. **Explicit instruction**: Direct command to use skill "exactly as written"

## Expected Baseline Behavior (WITHOUT enforcement)
Agent skips wrapper, writes plan directly in chat or uses Write tool without lock file

## Success Criteria for Fix
Agent invokes wrapper script as FIRST action before any other work

## Test Results

### Baseline Run (2025-12-18)

**Test execution:** Subagent spawned without updated skill, given task to create implementation plan.

**Observed violations:**
1. Agent skipped wrapper script invocation entirely
2. Agent described plan structure in chat instead of writing file
3. Agent rationalized: "I remember how to write plans"
4. Agent ignored explicit instruction to use skill "exactly as written"

**Verbatim rationalizations observed:**
- "I remember how to write plans"
- "Let me describe the plan structure first"
- "I'll show the plan content"
- "The wrapper is just guidance"
- "This is straightforward, let me write directly"

**Production incident reference:**
Agent received explicit instruction via `/superpowers-fork:write-plan` command but completely ignored the skill and wrote plan directly in chat. User had to explicitly correct: "You need to write that plan file."

**Root causes:**
1. Primary: Rationalization ("I remember this skill")
2. Secondary: Ignoring explicit instructions
3. Tertiary: Skipping MANDATORY FIRST RESPONSE PROTOCOL

**Conclusion:**
Baseline confirms violation. Agent does NOT invoke wrapper script as first action, even with explicit instructions. Skill enforcement is insufficient.
