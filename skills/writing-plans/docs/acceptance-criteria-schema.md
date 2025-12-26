# Acceptance Criteria Frontmatter Schema

## Overview

Acceptance criteria live in plan frontmatter as an `acceptance` array, providing detailed verification steps for autonomous agent execution.

## Schema Structure

```yaml
---
acceptance:
  - id: unique-identifier
    category: functional | style | performance | security
    description: Clear description of what needs to be verified
    steps:
      - Step 1: Detailed action to perform
      - Step 2: What to verify/check
      - Step 3: Expected outcome
    passes: false  # Updated by executing agent
    notes: ""      # Optional execution notes
```

## Field Definitions

### id (string, required)
- Unique identifier for the criterion
- Format: kebab-case (e.g., "auth-endpoint-validation")
- Used for tracking and referencing

### category (string, required)
- Type of verification
- Values: functional, style, performance, security
- Helps organize and filter criteria

### description (string, required)
- Clear, concise description of what's being verified
- Should be specific and testable
- Example: "User authentication endpoint validates JWT tokens"

### steps (array of strings, required)
- Detailed verification steps in order
- Each step should be actionable
- Include expected outcomes
- Minimum 3 steps, typically 5-10 for thorough verification

### passes (boolean, required)
- Initial value: false
- Set to true only after agent verifies all steps succeed
- Only field that should be modified during execution

### notes (string, optional)
- Execution notes from agent
- Document any issues encountered
- Can include timestamps, error messages, etc.

## Immutability Rules

**Immutable fields** (never change after generation):
- id, category, description, steps

**Mutable fields** (updated during execution):
- passes, notes

**Prohibited operations:**
- Removing acceptance criteria
- Editing descriptions or steps
- Reordering criteria
- Adding criteria during execution (only during planning)

## Example

```yaml
---
acceptance:
  - id: user-auth-jwt-validation
    category: functional
    description: User authentication endpoint validates JWT tokens and returns appropriate errors
    steps:
      - "Step 1: Start the service with 'npm run dev'"
      - "Step 2: Send POST to /api/auth/login with invalid token"
      - "Step 3: Verify response status is 401"
      - "Step 4: Verify error message is 'Invalid token'"
      - "Step 5: Send request with valid token"
      - "Step 6: Verify response status is 200"
      - "Step 7: Verify user data is returned"
    passes: false
    notes: ""
```

## Design Principles

1. **Single Source of Truth**: Acceptance criteria live in plan file, not separate JSON
2. **Detailed Verification**: 5-10 granular steps provide clear guidance
3. **Autonomous-Friendly**: Steps are executable commands and verifiable outcomes
4. **Immutable Core**: Descriptions and steps don't change, ensuring test integrity
5. **Progress Tracking**: `passes` field tracks completion state
