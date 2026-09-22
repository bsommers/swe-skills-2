#!/usr/bin/env bash
set -e

# check_graphify.sh - Graphify availability detector and installer helper

echo "=== Checking Graphify & Knowledge Graph Tooling ==="

has_graphify=false

if command -v graphify >/dev/null 2>&1; then
    echo "✓ Found 'graphify' binary on PATH: $(command -v graphify)"
    has_graphify=true
elif command -v gsd-tools >/dev/null 2>&1; then
    echo "✓ Found 'gsd-tools' on PATH: $(command -v gsd-tools)"
    has_graphify=true
elif [ -f "$HOME/.gemini/antigravity/gsd-core/bin/gsd-tools.cjs" ]; then
    echo "✓ Found Antigravity GSD Core at $HOME/.gemini/antigravity/gsd-core/bin/gsd-tools.cjs"
    has_graphify=true
fi

if [ "$has_graphify" = true ]; then
    echo "Graphify is available."
    exit 0
else
    echo "Graphify CLI is NOT installed."
    echo ""
    echo "Installation options:"
    echo "1. Python (recommended):"
    echo "   pip install graphify-cli  OR  uv tool install graphify-cli"
    echo "2. GSD / Node.js:"
    echo "   npx -y @opengsd/gsd-core@latest --local"
    echo ""
    exit 1
fi
