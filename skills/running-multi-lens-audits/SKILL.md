---
name: running-multi-lens-audits
description: Use when auditing a codebase, test suite, benchmark, or plan in depth before a release, after a big milestone, or when a single reviewer keeps missing whole classes of problems.
---

# Running Multi-Lens Audits

## Overview

One reviewer sees one angle. Partition the audit by **lens** (orthogonal questions), not by file, run lenses independently (parallel subagents if available), then **verify every finding by reproduction** before filing it.

## Lenses (adapt to the target)

| Lens | Asks |
|---|---|
| Correctness / logic | wrong results, off-by-one, matching/normalization, error paths |
| Data / ground truth | are inputs, labels, fixtures, examples valid and compiling? |
| Measurement / statistics | sample sizes, intervals, denominators, gameable metrics |
| Security / threat model | injection, secrets, permissions, contamination, adversarial inputs |
| Operations | determinism, portability, reproducibility, observability |
| Docs / claims | stale counts, wrong commands, unverified statements |

## Procedure

1. **Recon.** Discover layout, entry points, test commands. **Run the test suite first** for a baseline; note skips.
2. **Write a prompt file per lens** (`prompts/NN-lens.md`) with its focus checklist and expected output format.
3. **Run lenses independently.** Each returns candidate findings with location and evidence.
4. **Reproduce every finding** with a minimal failing script or test. Drop what you can't reproduce (or mark as unverified).
5. **Classify:** `[defect]` (wrong behavior) · `[quick-fix]` (cheap, high value) · `[stats]` · `[roadmap]` · `[docs]`.
6. **File one document per finding** (to draft them as GitHub issues, load `drafting-issue-reports`), e.g. `.audit/issues/NN-slug.md`:
   ```
   # [defect] Short title
   ## Problem      exact repro, code, impact
   ## Proposed fix concrete change + test + migration
   _Source: audit YYYY-MM-DD, <branch> @ <commit>_
   ```
7. **Remediate in tiers:** 0 correctness & safety → 1 measurement/statistics → 2 data quality → 3 roadmap features.
8. **Close the loop:** rerun full suite; reconcile counts in docs; note issue → commit mapping.

## Rules

- Lenses don't see each other's conclusions until the merge step (avoids anchoring).
- Every finding carries evidence; "looks wrong" is not a finding.
- Audit findings about the *auditor's own tooling* count too.

## Example outcome

A four-lens audit of a benchmark suite filed 51 issues (12 defects, 23 stats, 11 roadmap, 4 quick-fixes, 1 docs). Remediating them in tier order left 453 passing tests and zero label drift across 21 corpora.

## Common mistakes

- Partitioning by directory, so each auditor re-derives the same context and misses cross-cutting flaws.
- Filing unreproduced findings.
- Fixing roadmap items before defects.
- No baseline test run, so pre-existing failures get blamed on the audit's fixes.
