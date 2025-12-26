# Frontmatter Acceptance Criteria Test Plan

## Test 1: Generate Plan with Acceptance Criteria

**Steps:**
1. Invoke writing-plans skill wrapper
2. Provide plan name: "test-acceptance-frontmatter"
3. Write plan with 2 tasks, each generating 1 acceptance criterion
4. Verify frontmatter includes `acceptance` array
5. Verify each criterion has: id, category, description, steps, passes, notes
6. Verify passes=false initially
7. Verify steps array has 5-10 items

**Expected:**
- Plan file created with acceptance array in frontmatter
- All fields present and valid
- Follows schema from docs/acceptance-criteria-schema.md

---

## Test 2: Validate Frontmatter Schema

**Steps:**
1. Run validate-frontmatter.py on generated plan
2. Verify validation passes
3. Modify acceptance criterion to remove required field
4. Run validation again
5. Verify validation fails with helpful error

**Expected:**
- Valid plans pass validation
- Invalid plans fail with clear errors
- Acceptance array is validated

---

## Test 3: Update Acceptance Criterion Status

**Steps:**
1. Use executing-plans workflow
2. Read acceptance criteria from frontmatter
3. Execute verification steps for one criterion
4. Update `passes` field to true using Edit tool
5. Add notes: "Verified on 2025-12-26"
6. Verify other fields unchanged

**Expected:**
- Passes field updates successfully
- Immutable fields remain unchanged
- Notes are added correctly

---

## Test 4: Verify Cleanup

**Steps:**
1. Verify generate_acceptance.py has been removed
2. Verify DEPRECATED.md has been removed
3. Verify writing-plans SKILL.md no longer references deprecated script
4. Verify .gitignore ignores *-acceptance.json files

**Expected:**
- Scripts no longer exist in repository
- Documentation contains no deprecated references
- Acceptance.json files are gitignored
- New workflow uses frontmatter only

---

## Test 5: Complete Workflow Integration

**Steps:**
1. Create plan with writing-plans (includes acceptance)
2. Validate frontmatter
3. Rename plan
4. Use executing-plans to implement
5. Mark acceptance criteria as passing
6. Verify all acceptance criteria tracked in frontmatter
7. Verify no separate JSON files created

**Expected:**
- Seamless workflow from planning → execution → verification
- Single source of truth (plan file)
- No sync issues or orphaned files
