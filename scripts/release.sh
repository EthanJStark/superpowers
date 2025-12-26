#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# Get new version
NEW_VERSION=$(jq -r '.version' .claude-plugin/plugin.json)
echo -e "${GREEN}✓ Released version: $NEW_VERSION${NC}\n"

# Show push instructions
echo -e "${YELLOW}📤 Next steps:${NC}"
echo "1. Review the changes:"
echo "   git show HEAD"
echo ""
echo "2. Push to GitHub (triggers marketplace update):"
echo "   git push --follow-tags"
echo ""
echo "3. Verify marketplace:"
echo "   - Company marketplace will read plugin.json from GitHub"
echo "   - Users can install: superpowers-fork@renaissance-marketplace"
