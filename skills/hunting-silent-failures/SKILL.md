---
name: hunting-silent-failures
description: Use when reviewing code with low test coverage, after adding a permissive parser or adapter, when output looks plausible but subtly wrong or empty, or when asked to QA a test suite for real gaps rather than count coverage.
---

# Hunting Silent Failures

## Overview

The worst bugs don't crash; they return something plausible and wrong. **Read the untested code**, feed it strange but legal inputs, and look for data dropped, coerced, ignored, or swallowed.

For measuring coverage percentage, generating reports, or wiring CI gates, use `test-coverage` instead — this skill is for reading the gaps it finds and probing them for actual bugs, not producing the report.

## Method

1. List files/functions with no tests (coverage report, or `git grep` for names with no test references).
2. For each, read it asking: *what legal input makes this quietly do nothing or the wrong thing?*
3. Probe with the input set below. Record actual output next to expected.
4. For each confirmed bug: write the failing regression test first, fix, note it in the commit.
5. Choose loud vs soft failure deliberately (below).

## Probe inputs

Empty · null/undefined · single item · huge · duplicates · a `Date`/timestamp · year-like string (`"2020"`) · numeric string · nested empty · Unicode · negative/zero · the key your auto-detect can't find · an unreachable dependency.

## Smells

| Smell | Example |
|---|---|
| Reflection drops values | `Object.entries(new Date())` is empty, so dates vanish |
| Permissive coercion | `Date.parse("2020")` treats a number as a date |
| Dead parameter | argument accepted, never forwarded by the caller |
| Empty success | auto-detected key not found → renders an empty chart, no message |
| Swallowed exception | `except: pass`, `catch {}` around the important call |
| Defaults that mask config | wrong env var silently falls back to a default path |
| Zero-cost failure | timeout returns nothing and nothing is billed or logged |
| Tests that can't fail | assertions dead after an early return |

## Loud or soft?

- **Data of record / correctness-critical:** raise a typed error naming what and why.
- **Presentation where one bad tab would crash the whole view:** render, but `warn` with the key, the reason, and the fallback used. Never render *silently*.
- Either way, cover with a test that asserts the warning or error.

## Example (real)

A QA read of untested files found four silent bugs: dates dropped by a flattener, year strings typed as dates, an adapter rendering an empty chart with no warning, and a pipeline option that was never forwarded. Ten new tests pinned all four.

## Common mistakes

- Trusting a coverage number instead of reading the uncovered branches.
- Adding a broad `try/except` "for robustness" — that *creates* silent failures.
- Fixing the symptom without a regression test.
