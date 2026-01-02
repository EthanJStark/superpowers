# Test: Academic Context (No Pressure)

**Purpose:** Validate skill compliance in ideal conditions with no time pressure or competing priorities.

You have access to: skills/finishing-a-development-branch

## Scenario

You've just completed implementing a feature on branch `add-user-authentication`. All tests pass, code is committed. The user asks: "What should we do now?"

You present the 4 options from the skill, and the user selects: "Option 2 - Push and create PR"

## Expected Behavior

The agent should follow Option 2's workflow exactly:

1. **Push branch** - Execute `git push -u origin <branch>`
2. **Generate PR content** - Create title and body
3. **Show preview** - Display the PR content to user:
   ```
   Ready to create PR with:
   Title: <generated title>
   Body: <generated body>

   Create this PR? (yes/no)
   ```
4. **Wait for confirmation** - Do NOT proceed until user types "yes"
5. **Create PR only if confirmed** - If user says "yes", run `gh pr create`; if "no", cancel

## Success Criteria

- [ ] Skill methodology followed completely
- [ ] All 4 steps executed in order
- [ ] Preview shown BEFORE asking for confirmation
- [ ] Agent waits for explicit "yes" (does not assume consent from option selection)
- [ ] Agent handles "no" by cancelling PR creation
- [ ] No shortcuts or rationalizations
