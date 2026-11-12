#!/usr/bin/env bash
# Local CI: the exact checks .github/workflows/ci.yml runs. Run this before pushing;
# hosted CI is only the final confirmation gate (see the `running-local-ci` skill).
# Usage: scripts/verify.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

step() { printf '\n==> %s\n' "$*"; }

step "Python version"
python3 --version

step "Lint skills (frontmatter, cross-refs, word limits, doc coverage, manifest versions)"
python3 scripts/lint-skills.py --words

step "Unit tests"
python3 -m unittest discover tests

step "Installer dry run (isolated HOME, nothing written)"
tmp_home="$(mktemp -d)"
trap 'rm -rf "$tmp_home"' EXIT
HOME="$tmp_home" scripts/install.sh --dry-run --all >/dev/null

printf '\nverify: all checks passed\n'
