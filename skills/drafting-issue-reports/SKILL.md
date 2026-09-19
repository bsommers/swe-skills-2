---
name: drafting-issue-reports
description: Use when asked to write up bugs, enhancements, or review or audit findings as GitHub issues, when turning a list of problems into a backlog, or when issues should be prepared for human review before anything is filed.
---

# Drafting Issue Reports

## Overview

The deliverable is a **reviewable script**, not filed issues. The user reviews, edits, and runs it. Every issue in it is **verified, deduplicated, labeled from the repo's real label set, and actionable by someone with no context.**

Issues go to GitHub via `gh`. Never run the script, `gh issue create`, or any other GitHub write yourself. Filing is outward-facing (`committing-and-releasing-cleanly`).

## Procedure

1. **Gather and verify.** Reproduce each problem, or cite the exact evidence (`file:line`, commit, log line, failing command). If you can't, keep it but mark the claim `[UNVERIFIED]`. Never invent facts (`grounding-ai-outputs`).
2. **One issue per root cause.** Merge symptoms that share a mechanism; split an item that hides two fixes (`clustering-failures-by-root-cause`).
3. **Deduplicate.** `gh issue list --state all --search "<keywords>"`. Link to an existing issue instead of re-filing it.
4. **Read the label set.** `gh label list`. Use existing labels. Propose a missing one as a commented `gh label create` line at the top of the script; never create one yourself. With `--file`, the script checks all labels before filing anything.
5. **Write the script** from `references/issue-script-template.sh`, issues in severity order.
6. **Check it.** `bash -n` passes, a dry run prints every issue, and no issue has an empty section. Save it where the user prefers (e.g. `.issues/draft-YYYY-MM-DD.sh`).
7. **Report:** the path, an index table (title · labels · severity), and anything `[UNVERIFIED]`.

## Issue body (every section required)

| Section | Contents |
|---|---|
| **Summary** | One sentence a triager can act on. |
| **Description** | Bug: steps to reproduce, expected result, actual result, environment. Enhancement: current behavior and its limit. Evidence inline. |
| **Why it matters** | Who is affected, how often, and the consequence (data loss, wrong output, blocked workflow, cost). This is the justification for the severity label. |
| **Suggested fix** | Approach, likely files, the test that would prove it, alternatives considered. Mark it a suggestion. |
| **Acceptance criteria** | Checkboxes a reviewer can verify. |

Footer: `_Source: <how found>, <branch> @ <short-sha>_`.

## Labels and titles

- **Type** (exactly one): `bug` · `enhancement` · `documentation` · `security` · `chore`/`refactor` · `test`.
- **Severity or priority** (one): e.g. `critical` · `major` · `minor`, or the project's own `P0`–`P3` scheme.
- **Area** (optional): component.
- **Title:** a bug names the symptom and trigger ("CSV export drops last row when input lacks trailing newline"). An enhancement names the capability, in imperative form ("Add `--dry-run` to `sync`"). ≤ 72 chars, no "Bug:" prefix when a label says it.

## Common mistakes

- Filing, or running the script "to test it".
- Unquoted heredocs, which let backticks and `$VAR` in the body run as shell. Use `<<'BODY'`.
- "Why it matters" that restates the description or inflates severity.
- One mega-issue for five findings, or five issues for one cause.
- Labels the repo lacks, so `gh issue create` fails partway.
- A suggested fix with no test, or no acceptance criteria.
