# Deprecated Scripts

## generate_acceptance.py

**Deprecated:** 2025-12-26
**Reason:** Acceptance criteria moved to plan frontmatter
**Replacement:** writing-plans skill generates acceptance in frontmatter

**Migration:** Not needed (single user, no existing acceptance.json files in use)

### Why Deprecated

Separate acceptance.json files created sync issues:
- Plan and acceptance could diverge
- Required manual generation after plan creation
- Extra file to track and commit

### New Approach

Acceptance criteria now live in plan frontmatter:
- Single source of truth
- Generated during plan creation
- Updated in-place during execution
- No separate files to manage

See: skills/writing-plans/docs/acceptance-criteria-schema.md

## Future Cleanup (v6.0.0+)

Consider removing in future major version:
- generate_acceptance.py (keep for one major version cycle)
- acceptance.json support in any tooling
- References to old workflow in older documentation
