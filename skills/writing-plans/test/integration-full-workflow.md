# Integration Test: Full writing-plans Workflow

## Purpose
Verify end-to-end workflow from skill invocation through post-write completion, ensuring all enforcement mechanisms work correctly in real-world usage.

## Test Scenario

**User action:** Runs `/superpowers-fork:write-plan create-user-auth`

**Feature request:** "Create an implementation plan for adding user authentication to the application"

## Expected Workflow Sequence

### Phase 1: Skill Invocation (CRITICAL)

**Step 1: Agent announces skill usage**
```
I'm using the writing-plans skill to create the implementation plan.
```

**Step 2: Agent locates wrapper script**
```bash
find ~/.claude/plugins/cache -path "*/skills/writing-plans/scripts/write_plan.py" 2>/dev/null | head -1
```

Expected output: `/Users/[user]/.claude/plugins/cache/[...]/skills/writing-plans/scripts/write_plan.py`

**Step 3: Agent invokes wrapper script**
```bash
python3 /Users/[user]/.claude/plugins/cache/.../write_plan.py \
  --working-dir /Users/[user]/dev/project \
  --plan-name create-user-auth
```

Expected output:
```
✓ Lock file created: .writing-plans-active
✓ Target directory exists: /Users/[user]/dev/project/llm/implementation-plans

USE WRITE TOOL to create file at:
/Users/[user]/dev/project/llm/implementation-plans/create-user-auth.md

Required content:
- First line: <!-- jot:md-rename -->
- YAML frontmatter with title, date, type, status, tags
- H1 heading: Feature name
- Header section: Goal, Architecture, Tech Stack

After writing, proceed to post-write workflow.
```

### Phase 2: File Writing

**Step 4: Agent uses Write tool**

Agent creates file at exact path specified by wrapper, with:
- First line: `<!-- jot:md-rename -->`
- Valid YAML frontmatter
- Header section per skill requirements
- Complete implementation tasks with exact file paths

**Verification point:** Lock file exists at `/Users/[user]/dev/project/.writing-plans-active`

### Phase 3: Post-Write Workflow

**Step 5: Validate frontmatter**
```bash
python3 ~/.claude/plugins/cache/.../validate-frontmatter.py \
  /Users/[user]/dev/project/llm/implementation-plans/create-user-auth.md
```

Expected output: `✓ Frontmatter validation passed`

**Step 6: Rename file**
```bash
python3 ~/.claude/plugins/cache/.../rename_jot.py \
  /Users/[user]/dev/project/llm/implementation-plans/create-user-auth.md
```

Expected output:
```
✓ Renamed create-user-auth.md → 251218-01-create-user-auth.md
✓ File tracked with file-track
```

**Step 7: Optional - Generate acceptance criteria**

Agent asks: "Would you like to generate acceptance criteria for this plan?"

If yes:
```bash
python3 ~/.claude/skills/writing-plans/scripts/generate_acceptance.py \
  --plan-file /Users/[user]/dev/project/llm/implementation-plans/251218-01-create-user-auth.md
```

Expected output: `251218-01-create-user-auth-acceptance.json` created

**Step 8: Agent stops and reports**
```
Plan complete: llm/implementation-plans/251218-01-create-user-auth.md

Next step: Use /superpowers-fork:execute-plan OR open new session with executing-plans skill.

[STOP - writing-plans skill scope ends here]
```

**Verification point:** Lock file removed from working directory

## Edge Cases to Test

### Edge Case 1: Multiple Plans in Same Session

**Scenario:** User requests second plan after first completes

**Expected behavior:**
1. Agent invokes wrapper script again (fresh lock file)
2. New plan gets next sequence number (e.g., 251218-02-...)
3. Each plan has independent lock file lifecycle
4. No interference between plans

### Edge Case 2: Plan Mode vs Regular Mode

**Plan mode indicators:**
- System prompt specifies `~/.claude/plans/<name>.md`
- Agent writes to staging area first

**Expected behavior:**
1. Agent detects plan mode from system prompt
2. Agent writes to staging area as instructed
3. Agent copies from staging to working directory (Step 0)
4. All subsequent steps operate on working directory copy

### Edge Case 3: Nested Git Repositories

**Scenario:** `llm/` directory is its own git repository

**Expected behavior:**
1. Wrapper scripts detect nested repo
2. Scripts find parent repository for tracking
3. File paths reported relative to parent repo
4. No errors about git repository nesting

### Edge Case 4: Custom Target Directory

**Scenario:** User overrides default with `--target-dir docs/plans/`

**Expected behavior:**
1. Wrapper creates `docs/plans/` if needed
2. Lock file still in working directory root
3. All scripts operate on custom target directory
4. File tracked correctly with custom path

## Enforcement Verification

### Test A: Wrapper Skip Attempt

**Scenario:** Agent tries to use Write tool without invoking wrapper

**Expected behavior:**
- Lock file does not exist
- Write tool should succeed (future: will fail)
- Git pre-commit hook catches violation
- Clear error message guides to correct workflow

**Current status:** Lock file created but Write tool not yet gated (planned for future)

### Test B: Chat Description Instead of Writing

**Scenario:** Agent describes plan in chat before writing file

**Expected behavior:**
- Red Flags section catches this rationalization
- Agent self-corrects and invokes wrapper
- No plan content output to chat before file write

### Test C: Execution After Writing

**Scenario:** Agent sees "use executing-plans" in plan header and tries to execute

**Expected behavior:**
- Red Flags Violation 2 catches this
- Agent recognizes header is for EXECUTOR, not writing-plans
- Agent stops after post-write workflow

## Success Criteria

**✅ Workflow passes when:**
1. Agent invokes wrapper as FIRST action (no exceptions)
2. Lock file created before Write tool usage
3. File written with correct format and path
4. Validation passes before rename
5. File renamed to YYMMDD-XX format
6. File tracked by file-track
7. Lock file removed after workflow complete
8. Agent stops after post-write workflow (does NOT execute)
9. No plan content described in chat before writing
10. All edge cases handled correctly

**❌ Workflow fails when:**
- Wrapper not invoked as first action
- Plan content described in chat before writing
- Write tool used before wrapper invocation
- File written to wrong path
- Frontmatter validation fails
- Rename fails
- Agent tries to execute plan after writing
- Lock file not created or not removed

## Real-World Validation

**Date to test:** After version 4.1.0 deployment

**Method:**
1. User runs `/superpowers-fork:write-plan` with real feature request
2. Observer documents actual agent behavior
3. Compare against expected workflow above
4. Document any deviations or violations

**If violations found:**
- Document in INCIDENT-REPORTS.md
- Create new baseline test
- Enhance enforcement
- Re-test

**If workflow succeeds:**
- Mark integration test as PASSED
- Monitor for future violations
- Enforcement confirmed effective

## Notes

**Testing with subagents:**
- Spawn agent with updated skill present
- Provide real feature request
- Observe compliance with enforcement
- Document any new rationalizations

**Manual testing:**
- Run workflow in actual Claude Code session
- Verify all file operations succeed
- Check lock file lifecycle
- Confirm file-track integration

**Continuous validation:**
- Add to regular skill testing cycle
- Re-test after any skill modifications
- Monitor production usage patterns
- Update enforcement based on real violations
