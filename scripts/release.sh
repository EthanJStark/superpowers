#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for required tools
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ Error: jq is not installed${NC}"
    echo "Install with: brew install jq"
    exit 1
fi

echo -e "${YELLOW}🚀 Superpowers Plugin Release${NC}\n"

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo -e "${RED}❌ Error: Uncommitted changes detected${NC}"
    echo "Please commit or stash changes before releasing"
    git status -s
    exit 1
fi

# Check we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo -e "${RED}❌ Error: Not on main branch${NC}"
    echo "Current branch: $CURRENT_BRANCH"
    echo "Switch to main before releasing"
    exit 1
fi

# Show commits since last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
echo -e "${YELLOW}📝 Commits since last tag ($LAST_TAG):${NC}"
if [[ "$LAST_TAG" == "none" ]]; then
    git log --oneline --decorate=short
else
    git log $LAST_TAG..HEAD --oneline --decorate=short
fi
echo ""

# Preview version bump
echo -e "${YELLOW}🔍 Analyzing commits for version bump...${NC}"
cz bump --dry-run || {
    echo -e "${RED}❌ No version bump needed${NC}"
    echo "No conventional commits found since last tag"
    exit 0
}
echo ""

# Confirm release
read -p "Proceed with release? (yes/no): " CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
    echo -e "${YELLOW}⚠️  Release cancelled${NC}"
    exit 0
fi

# Perform version bump
echo -e "${GREEN}✓ Bumping version...${NC}"
cz bump --yes

# Sync marketplace manifest version
MARKETPLACE_MANIFEST="../../.claude-plugin/marketplace.json"
if [[ -f "$MARKETPLACE_MANIFEST" ]]; then
    echo -e "${GREEN}✓ Syncing version to local marketplace...${NC}"

    # Extract new version
    NEW_VERSION=$(jq -r '.version' .claude-plugin/plugin.json)

    # Update marketplace.json with new version and description
    jq --arg version "$NEW_VERSION" \
       '(.plugins[] | select(.name == "superpowers-fork") | .version) = $version |
        (.plugins[] | select(.name == "superpowers-fork") | .description) = "Production-tested fork with writing-plans automation - v\($version)"' \
       "$MARKETPLACE_MANIFEST" > "${MARKETPLACE_MANIFEST}.tmp"

    # Verify JSON is valid after modification
    if ! jq empty "${MARKETPLACE_MANIFEST}.tmp" 2>/dev/null; then
        echo -e "${RED}❌ Error: Marketplace JSON invalid after update${NC}"
        rm "${MARKETPLACE_MANIFEST}.tmp"
        exit 1
    fi

    # Atomic replace
    mv "${MARKETPLACE_MANIFEST}.tmp" "$MARKETPLACE_MANIFEST"

    echo -e "${GREEN}✓ Marketplace updated to version $NEW_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Local marketplace manifest not found (expected at $MARKETPLACE_MANIFEST)${NC}"
    echo "   Plugin version updated, but marketplace sync skipped"
fi
echo ""

# Get new version (already extracted above if marketplace exists)
if [[ -z "$NEW_VERSION" ]]; then
    NEW_VERSION=$(jq -r '.version' .claude-plugin/plugin.json)
fi
echo -e "${GREEN}✓ Released version: $NEW_VERSION${NC}\n"

# Get absolute path to marketplace manifest for commit
MARKETPLACE_DIR="$(cd ../.. && pwd)"

# Show push instructions
echo -e "${YELLOW}📤 Next steps:${NC}"
echo ""
echo "1. Review plugin changes:"
echo "   git show HEAD"
echo ""
echo "2. Review and commit marketplace sync:"
echo "   cd $MARKETPLACE_DIR"
echo "   git diff .claude-plugin/marketplace.json"
echo "   git add .claude-plugin/marketplace.json"
echo "   git commit -m \"chore: sync marketplace to plugin v$NEW_VERSION\""
echo ""
echo "3. Push both repositories:"
echo "   # Plugin repository (already in it)"
echo "   cd $(pwd)"
echo "   git push --follow-tags"
echo ""
echo "   # Marketplace wrapper repository"
echo "   cd $MARKETPLACE_DIR"
echo "   git push"
echo ""
echo "4. Verify marketplace:"
echo "   - Local marketplace will show updated version"
echo "   - Company marketplace (if synced) will read plugin.json from GitHub"
