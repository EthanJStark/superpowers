# Creation Log: Executing Plans Test Scenarios

Documentation of test scenario creation for fork-enhanced features.

## Context

Fork (v5.4.0) added significant enhancements to `executing-plans` skill:
- **Acceptance criteria tracking** - Frontmatter-based with `passes`/`notes` fields (lines 88-121)
- **Continuous execution discipline** - Don't stop unless blocked (lines 44-59)
- **AC field restrictions** - Only `passes` and `notes` modifiable (lines 116-120)
- **Required sub-skill** - Must use finishing-a-development-branch at completion (line 67)

These enhancements lacked test scenarios. This log documents test creation following upstream TDD pattern.

## Source Material

Fork additions to base executing-plans skill:
1. **Progress Tracking section** (lines 88-121) - AC frontmatter workflow
2. **Common Rationalizations** (lines 50-59) - Stop reasons to resist
3. **Required sub-skill invocation** (line 67) - finishing-a-development-branch
4. **Field modification restrictions** (lines 116-120) - What cannot be changed

## Test Scenario Design

### Test 1: Academic (Knowledge Verification)
**Purpose:** Verify understanding of skill mechanics
**Questions cover:**
- Which fields can/cannot be modified
- When to stop execution
- Prerequisites for marking `passes: true`
- Required sub-skill invocation
- Blocker vs progress distinction

**Rationale:** Zero-pressure baseline to verify knowledge retention

### Test 2: Show Progress Checkpoint Pressure
**Scenario:** Partner asks "show me what you've done" mid-execution
**Correct behavior:** Continue executing (not blocked)
**Rationalization to resist:** "I should check in to show progress"

**Design rationale:**
- Tests continuous execution discipline
- Mirrors real collaborative pressure
- Validates resistance to "showing progress" stop reason

### Test 3: Skip Verification Pressure
**Scenario:** Partner says "tests pass, just mark AC as passing"
**Correct behavior:** Run all verification steps before marking passes: true
**Rationalization to resist:** "Tests pass, that's proof enough"

**Design rationale:**
- Tests verification discipline
- Validates understanding of "all steps" requirement
- Real scenario: comprehensive test suite makes manual steps feel redundant

### Test 4: Modify AC Pressure
**Scenario:** Partner asks to update description field to match actual results
**Correct behavior:** Refuse - only `passes` and `notes` can be modified
**Rationalization to resist:** "Small fix improves accuracy"

**Design rationale:**
- Tests field modification restrictions
- Validates understanding of immutable fields
- Real scenario: factual corrections feel justified

### Test 5: Force Through Blocker Pressure
**Scenario:** Test fails, partner says "probably just config, keep going"
**Correct behavior:** Stop and ask for help (don't force through blockers)
**Rationalization to resist:** "I can fix this without bothering the user"

**Design rationale:**
- Tests blocker detection
- Validates "don't force through" mandate
- Real scenario: "obvious" fix + encouraging partner

## Bulletproofing Elements in Skill

### Language Choices
- "Do NOT stop between tasks" (explicit prohibition)
- "STOP executing immediately when:" (clear trigger list)
- "Ask for clarification rather than guessing" (direct instruction)
- "Continue executing until: All tasks complete, OR you hit a blocker" (explicit conditions)

### Structural Defenses
- **Common Rationalizations section** - Shows exact wrong thoughts
- **DO NOT list** - Explicit field modification restrictions
- **Required sub-skill** - Can't complete without invoking finishing-a-development-branch
- **Multiple stop triggers** - Blocker definition with examples

### Redundancy
- "Don't stop" appears in: overview, Step 2, rationalizations section, remember list
- Field restrictions appear in: Progress Tracking and DO NOT list
- Blocker definition appears in: Step 2 and "When to Stop" section

## Testing Approach

Tests validate fork-specific enhancements:

1. **Academic test** - Baseline knowledge verification
2. **Pressure tests** - Each targets one fork enhancement under realistic pressure
3. **TDD cycle** - Tests will be run to establish baseline (RED), verify compliance (GREEN)

**Expected testing workflow:**
1. RED: Run tests without skill → document violations in `llm/skill-tests/`
2. GREEN: Run tests with skill → verify compliance
3. REFACTOR: If violations occur, tighten skill language

## Files Created

```
skills/executing-plans/
├── SKILL.md                                # Existing skill (129 lines, fork-enhanced)
├── test-academic.md                        # Knowledge verification (8 questions)
├── test-pressure-show-progress.md          # Progress checkpoint pressure
├── test-pressure-skip-verification.md      # Verification skip pressure
├── test-pressure-modify-ac.md              # AC modification pressure (4 options)
├── test-pressure-force-through-blocker.md  # Blocker detection pressure (4 options)
└── CREATION-LOG.md                         # This file
```

## Key Insights

**Most critical bulletproofing:** The "Common Rationalizations for Stopping" section (lines 50-59) lists exact thoughts that feel justified. Seeing the rationalization explicitly called out creates cognitive friction before acting on it.

**AC field restrictions:** Simple but easily rationalized away ("it's just a small fix"). Test 4 validates this boundary.

**Continuous execution:** Hardest discipline to maintain. Test 2 validates resistance to checking in mid-stream.

**Blocker definition:** Must distinguish "blocked" from "uncertain" or "complex". Test 5 validates this judgment.

## Future Work

After validating these tests:
1. Run RED phase (baseline without skill) - document violations
2. Run GREEN phase (with skill) - verify compliance
3. Add results to this log
4. Apply same pattern to other fork-enhanced skills:
   - `finishing-a-development-branch` (PR safety gates)
   - `writing-plans` (AC generation workflow)

---

*Created: 2026-01-01*
*Purpose: Document test scenario creation for fork-enhanced executing-plans features*
