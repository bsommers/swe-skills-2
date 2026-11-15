---
name: reviewing-repo-health
description: Use when asked to review a whole repository against its goals, grade it, make it "A+", or produce a plan with milestones; when a deep review should fan out to parallel subagents on matched model tiers; or when review, docs and plans may have drifted apart.
---

# Reviewing Repo Health

## Overview

A whole-repo review is five phases that end in one ranked, approvable plan. Findings come from independent lenses; the plan comes from a single synthesis pass. **Read-only until the user approves the plan.**

## Setup (two commands)

```bash
scripts/detect-harness.py            # which agent harness, subagents?, tier -> model names
scripts/review-kickoff.py --goal "<one sentence>"   # creates docs/reviews/<date>/ with lens prompts
```

Without the scripts, create `docs/reviews/<date>/` by hand: `baseline.md`, `prompts/NN-lens.md`, `results/`, `REVIEW.md`.

## Phases

| # | Phase | Do | Tier (`routing-work-across-harnesses`) |
|---|---|---|---|
| 0 | Baseline | Run the repo's gate; record pass, fail, skips (`layered-verification-gates`) | fast |
| 1 | Lenses | One subagent per `prompts/NN-lens.md`, in parallel, each writing `results/NN-lens.md` (`running-multi-lens-audits`, `orchestrating-subagents`) | standard; frontier for architecture and security |
| 2 | Code review | Run the harness's high-effort review on the repo or diff; else `pr-review`. Reproduce every finding | frontier |
| 3 | Docs alignment | `auditing-doc-alignment` over README, agent files, docs, plans, manifests | standard |
| 4 | Uplift plan | `planning-grade-a-uplift`: grade, gaps, work items, milestones | frontier, one pass |
| 5 | Synthesis | Merge results into `REVIEW.md`: verdict, ranked findings, plan, open questions | you |

## Rules

1. **The user's goal, not generic quality.** Start from the repo's stated goals (README, purpose, roadmap). A finding that doesn't touch a goal is a footnote.
2. **A named model is a request.** If the harness can't select it, use the nearest tier and say so in `REVIEW.md`. Never silently downgrade the synthesis.
3. **No subagents? Run lenses sequentially.** Write each result to its file before starting the next lens; the files, not your memory, carry state.
4. **Evidence or it isn't a finding.** File, line, command, output. Unreproduced items go in a separate "unverified" list.
5. **Other agents may be editing.** Check `git status` first; write only under `docs/reviews/`; never touch files you didn't create. Use a worktree for any fix.
6. **Don't file, push or fix** without approval. Outward actions follow `committing-and-releasing-cleanly`.
7. **Report numbers with conditions** (`making-verifiable-claims`).

## Output contract

`REVIEW.md`: (1) verdict and grade per dimension, (2) findings table: severity, location, evidence, fix, (3) plan by milestone, (4) doc-conformance list, (5) what was not checked.

The reusable prompt for harnesses without skills is `references/prompt.md`.

## Common mistakes

- Reviewing files instead of goals, so the plan polishes the wrong things.
- Letting lenses read each other's results before merge (anchoring).
- Skipping the baseline run, then blaming old failures on the review.
- Asking the strongest model to do the survey as well as the synthesis.
- Writing the plan before verifying findings.
