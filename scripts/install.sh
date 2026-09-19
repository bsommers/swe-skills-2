#!/usr/bin/env bash
# Install swe-skills for Claude Code, Antigravity (agy), Cursor, and the cross-runtime ~/.agents alias.
# Default is symlinks (edits here propagate); use --copy for standalone copies.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/skills"

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [targets] [options]

Targets (user-level, any combination; default is --all):
  --claude          ~/.claude/skills/            (Claude Code)
  --agy             `agy plugin install` if agy is on PATH, else ~/.agents/skills/
  --cursor          ~/.cursor/skills/            (Cursor user skills)
  --agents          ~/.agents/skills/            (cross-runtime alias: Codex, Copilot CLI, Gemini, agy)
  --all             all of the above
  --project DIR     project-level: DIR/.claude/skills, DIR/.agents/skills, DIR/.cursor/skills,
                    DIR/.cursor/rules/swe-skills.mdc

Options:
  --copy            copy instead of symlink
  --force           replace existing entries with the same name
  --uninstall       remove what this script installed (only entries pointing here / marked)
  --dry-run         print actions, change nothing
  -h, --help
EOF
}

TARGETS=(); PROJECT=""; MODE=link; FORCE=0; UNINSTALL=0; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --claude|--agy|--cursor|--agents) TARGETS+=("${1#--}") ;;
    --all) TARGETS=(claude agy cursor agents) ;;
    --project) PROJECT="${2:?--project needs DIR}"; shift ;;
    --copy) MODE=copy ;;
    --force) FORCE=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --dry-run) DRY=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done
[ ${#TARGETS[@]} -eq 0 ] && [ -z "$PROJECT" ] && TARGETS=(claude agy cursor agents)

run() { if [ "$DRY" = 1 ]; then echo "DRY: $*"; else "$@"; fi; }
MARK=".swe-skills-2"   # marker file inside copied skill dirs

install_into() {  # $1 = destination skills dir
  local dest="$1" name target
  run mkdir -p "$dest"
  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"; target="$dest/$name"
    if [ "$UNINSTALL" = 1 ]; then
      if [ -L "$target" ] && [ "$(readlink "$target")" = "${skill%/}" ]; then run rm "$target"; echo "removed $target"
      elif [ -d "$target" ] && [ -f "$target/$MARK" ]; then run rm -rf "$target"; echo "removed $target"
      fi
      continue
    fi
    if [ -e "$target" ] || [ -L "$target" ]; then
      if [ "$FORCE" = 1 ]; then run rm -rf "$target"
      elif [ -L "$target" ] && [ "$(readlink "$target")" = "${skill%/}" ]; then continue
      else echo "skip (exists, use --force): $target" >&2; continue
      fi
    fi
    if [ "$MODE" = copy ]; then run cp -R "${skill%/}" "$target"; [ "$DRY" = 1 ] || : > "$target/$MARK"
    else run ln -s "${skill%/}" "$target"; fi
  done
  echo "$([ "$UNINSTALL" = 1 ] && echo uninstalled || echo installed) → $dest"
}

for t in "${TARGETS[@]:-}"; do
  case "$t" in
    claude) install_into "$HOME/.claude/skills" ;;
    cursor) install_into "$HOME/.cursor/skills" ;;
    agents) install_into "$HOME/.agents/skills" ;;
    agy)
      if command -v agy >/dev/null 2>&1 && [ "$UNINSTALL" = 0 ]; then
        run agy plugin install "$REPO_ROOT"
      elif command -v agy >/dev/null 2>&1; then
        run agy plugin uninstall swe-skills || true
      else
        echo "agy not found; using ~/.agents/skills instead" >&2
        install_into "$HOME/.agents/skills"
      fi ;;
  esac
done

if [ -n "$PROJECT" ]; then
  [ -d "$PROJECT" ] || { echo "no such directory: $PROJECT" >&2; exit 1; }
  PROJECT="$(cd "$PROJECT" && pwd)"
  for d in .claude/skills .agents/skills .cursor/skills; do install_into "$PROJECT/$d"; done
  rule="$PROJECT/.cursor/rules/swe-skills.mdc"
  if [ "$UNINSTALL" = 1 ]; then run rm -f "$rule"
  else run mkdir -p "$PROJECT/.cursor/rules"; run cp "$REPO_ROOT/templates/cursor/swe-skills.mdc" "$rule"; fi
fi
