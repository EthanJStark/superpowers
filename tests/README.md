# Test Infrastructure

## Overview

Executable test framework for validating skills and plugin functionality.

This directory contains automated tests for the Superpowers plugin, organized by test category. Tests validate that skills trigger correctly, work in various scenarios, and maintain expected behavior across changes.

## Test Categories

### Explicit Skill Requests (`explicit-skill-requests/`)

**Purpose:** Validates that skills trigger correctly when users explicitly request them, even in pressure scenarios where the agent might be tempted to skip formal processes.

**Test Scenarios:**
- `action-oriented.txt` - User wants fast action without formalities
- `after-planning-flow.txt` - Request to execute plan after brainstorming
- `claude-suggested-it.txt` - Following Claude's suggestion to use a skill
- `i-know-what-sdd-means.txt` - User familiar with skill abbreviations
- `mid-conversation-execute-plan.txt` - Executing plan mid-conversation
- `please-use-brainstorming.txt` - Direct request for brainstorming
- `skip-formalities.txt` - User wants to skip formal skill setup
- `subagent-driven-development-please.txt` - Explicit SDD request
- `use-systematic-debugging.txt` - Direct request for debugging skill

**Run:**
```bash
# Run all explicit skill request tests
./tests/explicit-skill-requests/run-all.sh

# Run single scenario
./tests/explicit-skill-requests/run-test.sh <scenario-name>

# Run multi-turn conversation test
./tests/explicit-skill-requests/run-multiturn-test.sh

# Test with Haiku model
./tests/explicit-skill-requests/run-haiku-test.sh
```

### Skill Triggering Tests (`skill-triggering/`)

**Purpose:** Validates that skills trigger correctly based on user prompts matching skill descriptions.

**Tested Skills:**
- systematic-debugging
- test-driven-development
- writing-plans
- dispatching-parallel-agents
- executing-plans
- requesting-code-review

**Run:**
```bash
# Run all skill triggering tests
./tests/skill-triggering/run-all.sh

# Run specific skill test
./tests/skill-triggering/run-test.sh <skill-name> <prompt-file> [max-iterations]
```

### Integration Tests (`subagent-driven-dev/`)

**Purpose:** End-to-end scenarios validating skill interactions and workflows.

**Test Scenarios:**
- `go-fractals/` - Testing subagent-driven development with Go project
- `svelte-todo/` - Testing with Svelte/TypeScript project

**Run:**
```bash
# Run specific integration test
./tests/subagent-driven-dev/run-test.sh <test-name>

# Examples:
./tests/subagent-driven-dev/run-test.sh go-fractals
./tests/subagent-driven-dev/run-test.sh svelte-todo
```

### Claude Code Tests (`claude-code/`)

**Purpose:** Tests specific to Claude Code CLI integration.

**Features:**
- Token usage analysis
- Subagent-driven development workflows
- Skill loading and execution
- Test helpers and utilities

**Run:**
```bash
# Run skill tests
./tests/claude-code/run-skill-tests.sh

# Run subagent-driven development tests
./tests/claude-code/test-subagent-driven-development.sh

# Analyze token usage
python3 tests/claude-code/analyze-token-usage.py <log-file>
```

### OpenCode Tests (`opencode/`)

**Purpose:** Tests for OpenCode integration (legacy).

**Run:**
```bash
# Run all OpenCode tests
./tests/opencode/run-tests.sh

# Individual test categories
./tests/opencode/test-plugin-loading.sh
./tests/opencode/test-skills-core.sh
./tests/opencode/test-priority.sh
./tests/opencode/test-tools.sh
```

## Fork-Specific Extensions

### Frontmatter Acceptance Tests

**Files:**
- `tests/test-frontmatter-acceptance.md` - Test scenarios for frontmatter acceptance criteria feature
- `tests/test-results-frontmatter-acceptance.md` - Results from frontmatter tests

**Purpose:** Validates fork-specific feature for tracking acceptance criteria in plan frontmatter. This feature allows executing-plans skill to track acceptance criteria pass/fail status directly in implementation plan frontmatter.

## Running Tests

### Run All Tests

```bash
# From repository root
./tests/skill-triggering/run-all.sh
./tests/explicit-skill-requests/run-all.sh
./tests/claude-code/run-skill-tests.sh
./tests/opencode/run-tests.sh
```

**Note:** Integration tests (`subagent-driven-dev/`) require explicit test name and are not included in "run all" commands.

### Run Specific Test Category

```bash
# Skill triggering
./tests/skill-triggering/run-all.sh

# Explicit skill requests
./tests/explicit-skill-requests/run-all.sh

# Integration test (specific scenario)
./tests/subagent-driven-dev/run-test.sh go-fractals
```

### Run Single Test

```bash
# Skill triggering (single skill)
./tests/skill-triggering/run-test.sh systematic-debugging prompts/systematic-debugging.txt

# Explicit skill request (single scenario)
./tests/explicit-skill-requests/run-test.sh action-oriented
```

## Adding New Tests

### Adding a Skill Triggering Test

1. Create prompt file: `tests/skill-triggering/prompts/<skill-name>.txt`
2. Add skill to `SKILLS` array in `tests/skill-triggering/run-all.sh`
3. Run test: `./tests/skill-triggering/run-test.sh <skill-name> prompts/<skill-name>.txt`

### Adding an Explicit Skill Request Test

1. Create prompt file: `tests/explicit-skill-requests/prompts/<scenario>.txt`
2. Add scenario description to this README
3. Run test: `./tests/explicit-skill-requests/run-test.sh <scenario>`

### Adding an Integration Test

1. Create test directory: `tests/subagent-driven-dev/<test-name>/`
2. Add required files:
   - `design.md` - Design document for agent to work from
   - `plan.md` - Implementation plan for agent
   - `scaffold.sh` - Script to set up test environment
3. Run test: `./tests/subagent-driven-dev/run-test.sh <test-name>`

## Test Output

Tests create timestamped output directories in `/tmp/superpowers-tests/`:

```
/tmp/superpowers-tests/
  <timestamp>/
    skill-triggering/
      <skill-name>/
        conversation.jsonl
        results.txt
    explicit-skill-requests/
      <scenario>/
        conversation.jsonl
        results.txt
    subagent-driven-development/
      <test-name>/
        project/  # Test project files
        logs/     # Execution logs
```

## CI/CD Integration

**Future:** These tests can be integrated into CI/CD pipelines to validate:
- PRs don't break skill triggering
- Skills maintain expected behavior
- Regression protection for skill changes

**Requirements for CI:**
- Claude Code CLI installed
- API keys configured
- Sufficient test credits/quota

## Maintenance

### Updating Tests After Skill Changes

When modifying a skill:
1. Update corresponding test prompts if trigger conditions change
2. Run skill-specific tests to verify behavior: `./tests/skill-triggering/run-test.sh <skill-name> ...`
3. If skill behavior changes intentionally, update expected behavior documentation

### Reviewing Test Failures

Test failures indicate:
- Skill not triggering when it should
- Skill triggering when it shouldn't
- Behavior regression after changes

**Investigation steps:**
1. Review test output in `/tmp/superpowers-tests/<timestamp>/`
2. Check conversation.jsonl for agent behavior
3. Compare with previous test runs
4. Adjust skill or test as appropriate

## References

- Skill development: `skills/writing-skills/SKILL.md`
- TDD methodology: `skills/testing-skills-with-subagents/SKILL.md`
- Upstream repository: https://github.com/obra/superpowers
