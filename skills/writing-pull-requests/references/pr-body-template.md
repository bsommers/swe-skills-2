## Summary

<!-- 1–3 sentences: what changes for users or callers, and why. -->
Export no longer drops rows when an input file lacks a trailing newline. CSV and TSV writers now share one line splitter.

## Issues

Closes #12
Closes #15

## Changes

<!-- Grouped by issue. Say what changed and where; don't narrate the commits. -->
- **#12 CSV drops last row:** `src/export/csv.py` iterates `splitlines()` instead of `split("\n")[:-1]`.
- **#15 TSV has the same bug:** `src/export/tsv.py` uses the shared `iter_rows()` in `src/export/_lines.py`.

## Why this approach

<!-- Alternatives considered and why they were rejected. -->
A shared helper fixes both writers in one place. Switching to `csv.reader` was rejected for now because it changes quoting behavior (tracked in #18).

## How verified

<!-- Exact commands and their results. Say what was NOT run. -->
```
$ pytest -q                      # 214 passed, 0 skipped
$ ruff check .                   # All checks passed
$ tool export fixtures/no-eol.csv --format csv | wc -l   # 3 (was 2)
```
Not run: the Windows CI job (runs on push).

## Risk and rollback

<!-- Blast radius, migrations, flags, compatibility. Is a revert safe? -->
Low. Output is unchanged for inputs that already end in a newline (covered by the existing golden tests). No schema or config changes. A revert is safe.

## Reviewer notes

<!-- Where to start and what deserves scrutiny. -->
Start with `_lines.py`. Check the empty-file case in `test_export.py::test_empty`.

## Follow-ups

<!-- Out-of-scope work found along the way, as issue links. -->
- #18 Evaluate `csv.reader` for quoted newlines
