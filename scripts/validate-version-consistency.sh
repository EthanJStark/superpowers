#!/usr/bin/env bash
# Validate that version is consistent across .cz.toml and plugin.json

set -e

# Extract versions
cz_version=$(grep "^version = " .cz.toml | cut -d'"' -f2)
plugin_version=$(jq -r ".version" .claude-plugin/plugin.json)

# Compare
if [ "$cz_version" != "$plugin_version" ]; then
    echo "❌ Version mismatch detected:"
    echo "  .cz.toml: $cz_version"
    echo "  .claude-plugin/plugin.json: $plugin_version"
    echo ""
    echo "Fix: Run 'cz bump' or manually sync versions"
    exit 1
fi

echo "✅ Version consistency validated: $cz_version"
exit 0
