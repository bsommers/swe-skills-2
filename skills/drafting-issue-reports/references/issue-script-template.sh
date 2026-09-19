#!/usr/bin/env bash
# Draft issues for review. Nothing is filed unless you pass --file.
#
#   ./draft-issues.sh           # dry run: print every issue
#   ./draft-issues.sh --file    # create them with gh (after review)
#   REPO=owner/name ./draft-issues.sh --file
#
# Index (severity order):
#   1. [bug, major]        CSV export drops last row when input lacks trailing newline
#   2. [enhancement, minor] Add --dry-run to sync
set -euo pipefail

REPO="${REPO:-}"                      # empty = repo of the current directory
MODE=dry-run
[[ "${1:-}" == "--file" ]] && MODE=file

# Labels these issues use that the repo does not have yet. Create them only after review:
#   gh label create <name> --color <hex> --description "<text>"
LABELS_TO_CREATE=()

check_labels() {
  local have missing=()
  have="$(gh label list ${REPO:+--repo "$REPO"} --limit 500 --json name -q '.[].name')"
  for l in "$@"; do grep -qxF "$l" <<<"$have" || missing+=("$l"); done
  if ((${#missing[@]})); then
    echo "Missing labels: ${missing[*]}. Create them or edit this script." >&2
    exit 1
  fi
}

# issue "<title>" "<label>,<label>" <<'BODY' ... BODY
issue() {
  local title="$1" labels="$2" body
  body="$(cat)"
  if [[ $MODE == file ]]; then
    gh issue create ${REPO:+--repo "$REPO"} --title "$title" --label "$labels" --body "$body"
  else
    printf '=== %s  [%s]\n%s\n\n' "$title" "$labels" "$body"
  fi
}

# Every label used below, checked before anything is created so a run cannot fail halfway.
[[ $MODE == file ]] && check_labels bug enhancement major minor

issue "CSV export drops last row when input lacks trailing newline" "bug,major" <<'BODY'
## Summary
`export --format csv` silently omits the final record when the input file does not end with a newline.

## Description
**Steps to reproduce**
1. `printf 'id,name\n1,a\n2,b' > in.csv` (no trailing newline)
2. `tool export in.csv --format csv -o out.csv`
3. `wc -l out.csv`

**Expected:** 3 lines (header + 2 rows). **Actual:** 2 lines; row `2,b` is missing. Exit code 0.

**Evidence:** `src/export/csv.py:88` iterates `text.split("\n")[:-1]`, which drops the last element whether or not it is empty.
**Environment:** main @ abc1234, Python 3.12.

## Why it matters
Data is lost with no error, so users only find out downstream. It affects any file saved without a final newline, which some editors do by default.

## Suggested fix
Iterate `text.splitlines()`, or use `csv.reader` on the file object. Add a regression test with and without a trailing newline.

## Acceptance criteria
- [ ] Both input forms export every row
- [ ] Regression test in `tests/test_export.py`
- [ ] No change to output when the input already ends in a newline

_Source: manual QA of export, main @ abc1234_
BODY

issue "Add --dry-run to sync" "enhancement,minor" <<'BODY'
## Summary
Let `sync` show what it would change without writing.

## Description
`sync` writes to the destination immediately. The only preview today is to copy the destination first.

## Why it matters
Users run `sync` against shared directories. A preview lowers the risk of an accidental overwrite and makes the command safe to script.

## Suggested fix
Add `--dry-run`, which runs the planning step and prints the plan table, then exits 0 before the write step. Test that the destination is byte-identical after a dry run.

## Acceptance criteria
- [ ] `sync --dry-run` lists creates, updates, and deletes, and writes nothing
- [ ] Documented in `--help` and the README

_Source: user request, main @ abc1234_
BODY
