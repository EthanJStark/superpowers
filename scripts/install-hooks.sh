#!/usr/bin/env bash
# Install git hooks for this repository
# Run once after cloning: ./scripts/install-hooks.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Installing git hooks..."

# Pre-commit: version consistency validation
cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/usr/bin/env bash
# Pre-commit hook: validate version consistency

set -e

# Run version consistency check
./scripts/validate-version-consistency.sh
EOF

chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Git hooks installed:"
echo "  - pre-commit: version consistency validation"
echo ""
echo "Test: Run './scripts/validate-version-consistency.sh' to verify"
