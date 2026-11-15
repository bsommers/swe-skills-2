---
name: auditing-doc-alignment
description: Use when README, agent instruction files, docs, plans, changelog and manifests may disagree with the code or each other; before a release or public launch; or when asked whether documentation and planning are consistent and what it would take to fix them.
---

# Auditing Doc Alignment

## Overview

Docs drift in bulk, not per change (`keeping-docs-in-sync` covers the per-change case). Treat every checkable statement as a **claim**, verify it against a source of truth, and plan the fixes as one batch.

## Procedure

1. **Inventory.** README, `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`/rules, `docs/`, plans and roadmaps, CHANGELOG, manifests, CI config.
2. **Mechanical pass.** `scripts/doc-claims.py [root]` lists broken relative links, backticked paths that don't exist, and count claims ("69 skills", "8 hooks") beside the real count.
3. **Extract claims by hand** for what a script can't see: commands, versions, feature status, "done" markers in plans, named files and flags.
4. **Verify each claim** by running or counting it. Precedence for truth: running code and tests, then manifests, then docs, then plans.
5. **Classify drift:**
   - `stale`: was true, no longer
   - `contradiction`: two docs disagree
   - `missing`: real behavior with no doc
   - `phantom`: doc describes something that doesn't exist
   - `plan-rot`: plan item done, abandoned or superseded but still marked open
6. **Write the conformance plan:** one row per drift, in the table below. Prefer fixing the doc; fix the code only when the doc states the intended behavior.
7. **Add a guard** for each class that can recur: a lint check, a generated count, a single source for repeated tables.

```
| # | Claim (file:line) | Truth (evidence) | Class | Fix | Guard |
```

## Rules

- Count claims are the commonest drift; generate them or lint them rather than retyping.
- A plan with no status is not a plan. Every plan file gets `open`, `done`, or `superseded by <file>`.
- Duplicate tables are a defect: keep one, link from the rest.
- Report what you did not read.

## Common mistakes

- Trusting the README over the code.
- Fixing docs without a guard, so they drift again.
- Treating old plans as current requirements.
- Rewriting prose for style during an alignment pass; keep diffs to the claims.
