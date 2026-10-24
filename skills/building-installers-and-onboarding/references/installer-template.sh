#!/usr/bin/env bash
# Multi-target installer template: --local (default), --global, or --prefix DIR.
# Supports --copy / symlink mode, --dry-run, --force, and --uninstall.
set -euo pipefail

TOOL_NAME="<tool>"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SCOPE="local"
PREFIX="${PREFIX:-}"
DRY_RUN=0
FORCE=0
UNINSTALL=0

usage() {
  cat <<EOF
Usage: install.sh [scope] [options]

Install scopes (pick one; default is --local):
  --local           Install in user home (\${XDG_BIN_HOME:-\$HOME/.local/bin})
  --global          Install system-wide (/usr/local/bin, requires write access)
  --prefix DIR      Install into custom prefix (DIR/bin, DIR/share/$TOOL_NAME)

Options:
  --dry-run         Print actions without modifying the filesystem
  --force           Overwrite existing installation
  --uninstall       Remove installed files for the selected scope
  -h, --help        Show this help message

Examples:
  ./scripts/install.sh --local
  ./scripts/install.sh --prefix "\$HOME/opt/$TOOL_NAME"
  sudo ./scripts/install.sh --global
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --local) SCOPE="local" ;;
    --global) SCOPE="global" ;;
    --prefix)
      SCOPE="custom"
      PREFIX="${2:?error: --prefix requires a directory argument}"
      shift
      ;;
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    --uninstall) UNINSTALL=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown option '$1' (run with --help)" >&2; exit 2 ;;
  esac
  shift
done

case "$SCOPE" in
  local)
    BIN_DIR="${XDG_BIN_HOME:-$HOME/.local/bin}"
    SHARE_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/$TOOL_NAME"
    ;;
  global)
    BIN_DIR="/usr/local/bin"
    SHARE_DIR="/usr/local/share/$TOOL_NAME"
    ;;
  custom)
    BIN_DIR="${PREFIX%/}/bin"
    SHARE_DIR="${PREFIX%/}/share/$TOOL_NAME"
    ;;
esac

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

check_writable() {
  local target_parent="$1"
  while [ ! -e "$target_parent" ] && [ "$target_parent" != "/" ]; do
    target_parent="$(dirname "$target_parent")"
  done
  if [ "$DRY_RUN" -eq 0 ] && [ ! -w "$target_parent" ]; then
    echo "error: cannot write to $target_parent (use --local, --prefix DIR, or run with sudo for --global)" >&2
    exit 1
  fi
}

TARGET_BIN="$BIN_DIR/$TOOL_NAME"

if [ "$UNINSTALL" -eq 1 ]; then
  check_writable "$BIN_DIR"
  [ -e "$TARGET_BIN" ] || [ -L "$TARGET_BIN" ] && run rm -f "$TARGET_BIN"
  [ -d "$SHARE_DIR" ] && run rm -rf "$SHARE_DIR"
  echo "Uninstalled $TOOL_NAME from $BIN_DIR"
  exit 0
fi

check_writable "$BIN_DIR"
if { [ -e "$TARGET_BIN" ] || [ -L "$TARGET_BIN" ]; } && [ "$FORCE" -eq 0 ]; then
  echo "error: $TARGET_BIN already exists (re-run with --force to overwrite)" >&2
  exit 1
fi

run mkdir -p "$BIN_DIR" "$SHARE_DIR"
run ln -sf "$REPO_ROOT/bin/$TOOL_NAME" "$TARGET_BIN"

cat <<EOF
Installed $TOOL_NAME ($SCOPE scope):
  binary: $TARGET_BIN
  data:   $SHARE_DIR
EOF

case ":${PATH:-}:" in
  *":$BIN_DIR:"*) ;;
  *)
    cat <<EOF

Note: $BIN_DIR is not on your PATH. Add it to your shell profile:
  export PATH="$BIN_DIR:\$PATH"
EOF
    ;;
esac

cat <<EOF

Next steps:
  1. $TOOL_NAME init        # initialize a new workspace and starter config
  2. $TOOL_NAME doctor      # verify runtime dependencies and environment
  3. $TOOL_NAME guide       # view the complete workflow guide
EOF
