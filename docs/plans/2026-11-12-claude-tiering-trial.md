# Plan: Claude model-tiering trial branch

Date: 2026-11-12. Status: DRAFT, awaiting approval of step order. Source: `docs/MODEL-APPLICABILITY-REVIEW.md` (read its caveats: reviewer estimates, templates only skimmed, no eval runs behind the verdicts).

## Goal
Make the skill set fit Haiku, Sonnet 5.5, Opus 5.5 and Fable 5.2 without forking skills per model. Cut tokens that frontier models do not need; keep guardrails and repo facts for everyone.

## Design (one source of truth, two tiers)
Tiers: **frontier** = Opus 5.5, Fable 5.2. **standard** = Sonnet 5.5, Haiku. Sonnet's fit with the frontier core is unproven and is tested separately (step 6).

1. **Lean core in every `SKILL.md`**: class A (repo/env facts) and class B (guardrails) only. Remove agent-detection tables, Mermaid flowcharts, stale rate tables.
2. **`references/basics.md`** holds the generic (class C) detail. Core carries one line: "Haiku/Sonnet or unsure: read `references/basics.md` first." Frontier models skip it.
3. **`--profile frontier`** in `scripts/install.sh` omits the nearly-all-textbook skills. Default stays `all` until evidence supports changing it.

No per-model copies. Profiles are per install, so Haiku subagents inside a frontier session get the frontier set; the `references/` pointer covers them.

## Preconditions
- PR #4 merged; `chore/phase3-portability` merged or abandoned (state not verified here).
- Branch `trial/claude-tiering` cut from updated `main`. Trial only; no merge to `main` without a results review.
- Baseline recorded on `main` before any change (see Measurement).

## Steps (one commit per group; run the gate after each)
1. **Remove noise (all models).** Delete agent-detection tables/flowcharts: `api-contract-audit`, `dependency-audit`, `code-architecture-review` (+ `AGENT_TUNING.md`), `pr-review`, `refactor-execute`, `test-coverage`.
2. **Fix stale content.** `token-finops` rate table (add Opus 5.5, Fable 5.2) and make its per-turn status line opt-in; drop Antigravity tier names from `adaptive-model-routing`; re-check `compacting-context-safely` cache-TTL arithmetic against current harness behavior.
3. **Core + basics split** for the "partly overkill" skills: `compacting-context-safely`, `building-unattended-agent-loops`, `building-trustworthy-benchmarks`, `clustering-failures-by-root-cause`, `designing-exhaustive-test-cases`, `building-code-generators`, `layered-verification-gates`, `handing-off-sessions`, `release`, `test-coverage`, `planning-with-contracts`, `writing-user-guides`, `security-best-practices`, `pr-review`, `refactor-execute`.
4. **Trim textbook skills** to ~100-250 words or move bodies to `references/`: `architecture-best-practices`, `choosing-tools-and-substrates`, `designing-layered-pipelines`, `designing-data-pipelines`, `defending-architecture-decisions`, `building-small-cli-tools`, `designing-testable-seams`, `evolving-schemas-and-contracts`, `designing-plugin-contracts`, `engineering-for-determinism`, `keeping-event-loops-responsive`, `parsing-untrusted-text-robustly`.
5. **Merge duplicates.** `github-issues-script` into `drafting-issue-reports`; merge `showcasing-graphics-in-docs` + `rendering-graphic-examples`. Update README table, `using-swe-skills`, `docs/EVIDENCE.md`, `docs/TESTING.md` (lint requires it).
6. **Profiles + lint.** Add `frontier` profile. Profiles are currently hard-coded in `scripts/install.sh` (`is_in_profile`, usage text); move them to one manifest and fix the existing "core (8)" count mismatch. Lint rules: every skill is in the frontier profile or marked excluded; a "read basics" pointer requires the file; word limits unchanged.
7. **Condense `using-swe-skills` routing table** (~700 words loaded every session). Highest blast radius, so last, own commit.
8. **Add "skip for clear tasks"** to `writing-intent-briefs` and "skip when reversible" to `defending-architecture-decisions`.

## Gate after every step
`scripts/verify.sh` (lint + tests) and `python3 scripts/eval-router.py --self-test`. Note: the router eval is a static self-test of the router file against benchmark cases, not a live model run, so it checks routing text only.

## Measurement (needed because verdicts are unproven)
- Token cost: `wc -w skills/*/SKILL.md` and description-token total, `main` vs branch.
- Behavior: replay the `docs/TESTING.md` pressure scenarios for touched skills on Opus 5.5 and Fable 5.2 (frontier core), then Sonnet 5.5 and Haiku (core + basics). Run each scenario on `main` and on the branch; record pass/fail per model.
- Haiku-risk skills (`handing-off-sessions`, `layered-verification-gates`, `designing-plugin-contracts`, `code-architecture-review`, `compacting-context-safely`, `building-unattended-agent-loops`, `building-trustworthy-benchmarks`) get explicit Haiku runs.
- Store results in `docs/plans/` next to this file.

## Decision rule
Adopt a step only if the branch passes the same scenarios as `main` for every tier it targets. If Sonnet/Haiku regress on a trimmed skill, restore that skill's detail in `references/basics.md`, not in core. If Sonnet passes with the frontier core, collapse to one tier.

## Out of scope / risks
- No skill content changes before approval of this plan.
- Reviewer verdicts are estimates; step 4 deletions are the most speculative, so they run after measurement tooling exists.
- Profile install does not help skills already loaded in a mixed-model session.
