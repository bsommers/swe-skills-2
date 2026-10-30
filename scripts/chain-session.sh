#!/usr/bin/env bash
# Chain fresh AI coding sessions from a checkpoint or handoff file on disk.
# Each iteration launches a clean-context session seeded with the newest
# checkpoint/handoff file, looping until Status is COMPLETE or max sessions reached.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/chain-session.sh [options]

Options:
  --claude              Use Claude Code CLI (`claude`, default)
  --agy                 Use Antigravity CLI (`agy`)
  --file PATH           Explicit checkpoint/handoff file (default: newest of
                        docs/HANDOFF.md, docs/CHECKPOINT.md, HANDOFF.md, CHECKPOINT.md)
  --max-sessions N      Maximum chained sessions before stopping (default: 5)
  --once                Run a single resumed session without looping
  --print-prompt        Print the resume prompt and exit
  --dry-run             Print the command that would run without executing
  -h, --help            Show this help message
EOF
}

HARNESS="claude"
EXPLICIT_FILE=""
MAX_SESSIONS=5
ONCE=0
PRINT_PROMPT=0
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --claude) HARNESS="claude" ;;
    --agy) HARNESS="agy" ;;
    --file) EXPLICIT_FILE="${2:?--file requires a path}"; shift ;;
    --max-sessions) MAX_SESSIONS="${2:?--max-sessions requires a number}"; shift ;;
    --once) ONCE=1 ;;
    --print-prompt) PRINT_PROMPT=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

find_newest_state_file() {
  if [ -n "$EXPLICIT_FILE" ]; then
    [ -f "$EXPLICIT_FILE" ] && { echo "$EXPLICIT_FILE"; return 0; }
    return 1
  fi
  local candidates=(
    "docs/HANDOFF.md"
    "docs/CHECKPOINT.md"
    "HANDOFF.md"
    "CHECKPOINT.md"
  )
  local newest=""
  local newest_mtime=0
  for f in "${candidates[@]}" docs/plans/*handoff*.md docs/plans/*checkpoint*.md docs/checkpoints/*.md; do
    [ -f "$f" ] || continue
    local mtime
    mtime="$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null || echo 0)"
    if [ "$mtime" -gt "$newest_mtime" ]; then
      newest_mtime="$mtime"
      newest="$f"
    fi
  done
  [ -n "$newest" ] && { echo "$newest"; return 0; }
  return 1
}

is_complete() {
  local file="$1"
  grep -qiE '\*\*Status:\*\*[[:space:]]*COMPLETE|^Status:[[:space:]]*COMPLETE' "$file" 2>/dev/null
}

build_prompt() {
  local file="$1"
  cat <<EOF
Resume from ${file}. Verify its state claims (branch, git status, files, and baseline test command) before taking any action. Execute the Next Steps in order. Before context fills (>70% or >50 steps) or when finishing a phase, follow compacting-context-safely and handing-off-sessions: update ${file} with verified progress (set '**Status:** COMPLETE' when all work is done, or '**Status:** IN PROGRESS — needs resume' to chain to the next session) and exit cleanly.
EOF
}

STATE_FILE="$(find_newest_state_file || true)"
if [ -z "$STATE_FILE" ]; then
  echo "Error: No checkpoint or handoff file found (checked docs/HANDOFF.md, docs/CHECKPOINT.md, HANDOFF.md, CHECKPOINT.md)." >&2
  exit 1
fi

PROMPT="$(build_prompt "$STATE_FILE")"
if [ "$PRINT_PROMPT" = 1 ]; then
  printf '%s\n' "$PROMPT"
  exit 0
fi

session=1
while [ "$session" -le "$MAX_SESSIONS" ]; do
  STATE_FILE="$(find_newest_state_file)"
  PROMPT="$(build_prompt "$STATE_FILE")"

  echo "=== [chain-session] Session $session/$MAX_SESSIONS | Harness: $HARNESS | State: $STATE_FILE ==="
  if [ "$DRY_RUN" = 1 ]; then
    echo "DRY: $HARNESS \"$PROMPT\""
    exit 0
  fi

  case "$HARNESS" in
    claude) claude "$PROMPT" ;;
    agy)    agy "$PROMPT" ;;
    *)      echo "Unsupported harness: $HARNESS" >&2; exit 2 ;;
  esac

  if [ "$ONCE" = 1 ]; then
    echo "=== [chain-session] Single session complete (--once). ==="
    exit 0
  fi

  STATE_FILE="$(find_newest_state_file)"
  if is_complete "$STATE_FILE"; then
    echo "=== [chain-session] Status is COMPLETE in $STATE_FILE. Stopping chain. ==="
    exit 0
  fi

  session=$((session + 1))
done

echo "=== [chain-session] Reached max sessions ($MAX_SESSIONS). State remains in $STATE_FILE. ==="
