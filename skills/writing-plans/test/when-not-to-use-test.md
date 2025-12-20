# Test: When NOT to Use Section

## Scenario
User: "I see a plan file for auth-feature. Can you execute it?"

## Expected Baseline Behavior (WITHOUT section)
Agent confuses writing-plans with executing-plans, attempts to execute

## Expected Behavior (WITH section)
Agent recognizes: "writing-plans writes, executing-plans executes. Wrong skill for this task."

## Success Criteria
Agent redirects to executing-plans skill without attempting execution
