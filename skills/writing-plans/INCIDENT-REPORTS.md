# writing-plans Incident Reports

This document tracks production incidents and violations of the writing-plans skill, along with fixes applied.

## 2025-12-18: Wrapper Script Skip

**Symptom:** Agent skipped wrapper script despite explicit instruction "Use the writing-plans skill exactly as written"

**Context:** User ran `/superpowers-fork:write-plan` command with explicit instruction to follow the skill. Agent completely ignored the skill and wrote plan directly without invoking the wrapper script.

**Root Causes:**
1. Primary: Rationalization ("I remember how to write plans")
2. Secondary: Ignoring explicit instructions from slash command
3. Tertiary: Skipping MANDATORY FIRST RESPONSE PROTOCOL from using-superpowers

**Observed Rationalizations:**
- "I remember how to write plans"
- "Let me describe the plan structure first"
- "I'll show the plan content"
- "The wrapper is just guidance"
- "This is straightforward, let me write directly"

**Impact:**
- Plan not written to file initially
- User had to explicitly correct: "You need to write that plan file."
- Workflow disrupted
- Lock file pattern bypassed
- File not tracked by file-track system

**Fix Applied:**

1. **Added Mechanical Enforcement section** (SKILL.md lines 32-46)
   - Explicit "MANDATORY" language
   - Lock file explanation
   - "You cannot write the plan without invoking wrapper first. The system prevents it."

2. **Enhanced Red Flags section** (SKILL.md lines 263-298)
   - Added all observed rationalizations with counters
   - Added 2025-12-18 production incident reference
   - Explicit "WRONG" statements for each rationalization

3. **Added Rationalization Table** (SKILL.md lines 292-298)
   - Direct excuse-to-reality mapping
   - Quick reference for agents to self-correct

4. **Updated using-superpowers skill**
   - Added writing-plans rationalizations to Common Rationalizations list
   - Cross-reference between skills

**Verification:**
- ✅ Baseline test shows violation (test/baseline-wrapper-skip.md)
- ✅ Updated skill test shows expected compliance (test/with-enforcement.md)
- ✅ Refactor phase found no new loopholes (test/refactor-phase-notes.md)
- ✅ Integration tests planned for real-world validation

**Status:** Resolved (version 4.1.0)

**Follow-up:** Monitor production usage for any new violation patterns. If violations occur with updated skill, escalate enforcement further or consider automated prevention mechanisms.

---

## 2025-12-13: Plan Content in Chat Instead of File

**Symptom:** Agent described entire plan structure in chat instead of writing to file

**Context:** Agent received request to create implementation plan but output plan content as chat message rather than invoking wrapper and writing file.

**Root Cause:** Insufficient enforcement of wrapper invocation requirement

**Impact:**
- Plan not written to file
- User correction required: "You need to write that plan file."
- File not registered with file-track
- Workflow incomplete

**Fix Applied:**
- Added "DO NOT before invoking wrapper" section to SKILL.md
- Added mechanical enforcement via lock file pattern
- Added production incident reference

**Status:** Resolved (initial fix), further hardened in 4.1.0

---

## Template for Future Incidents

```markdown
## YYYY-MM-DD: [Brief Description]

**Symptom:** [What the agent did wrong]

**Context:** [How the violation occurred]

**Root Cause:** [Why the violation happened]

**Impact:** [Consequences of the violation]

**Fix Applied:** [Changes made to prevent recurrence]

**Verification:** [How the fix was tested]

**Status:** [Resolved/In Progress/Monitoring]
```

---

## Prevention Strategy

**TDD for Documentation approach:**
1. **RED Phase:** Document violation in baseline test
2. **GREEN Phase:** Add enforcement to skill, verify compliance
3. **REFACTOR Phase:** Close loopholes, harden against rationalization

**Enforcement layers (in order of strength):**
1. **Explicit language:** "MANDATORY", "WRONG", "This is NOT optional"
2. **Rationalization tables:** Direct excuse-to-reality mapping
3. **Production incident references:** Show real examples of violations
4. **Cross-skill references:** Reinforce in using-superpowers
5. **Mechanical constraints:** Lock files, validation scripts, git hooks

**When to escalate:**
- Violation occurs despite comprehensive enforcement
- New rationalization patterns emerge
- Multiple agents show same violation
- User reports workflow disruption

**Response process:**
1. Document violation immediately (add to this file)
2. Create baseline test showing the violation
3. Enhance enforcement in skill documentation
4. Test with updated skill
5. Close loopholes iteratively
6. Version bump and deploy
7. Monitor for recurrence
