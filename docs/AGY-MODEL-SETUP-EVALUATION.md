# Evaluation: pasted Antigravity (agy) skill/subagent setup

Date: 2026-11-14. Status: implemented per recommended path.
Subject: a pasted setup proposing `session-router` + `docker-git-ops` skills and
`architect` / `ops-executor` / `bulk-worker` subagent profiles bound to
"Gemini 4 Carbon/Argon/Hydrogen" and "Gemini 3.8 Flash".

## Verdict
Reasonable pattern, but do not adopt as written. It is a sketch that does not fit
this repo's design, and several claims are unverified.

## What it gets right
- Router skill separated from subagent profiles that bind model + tool permissions
  (more reliable than hoping dynamic `invoke_subagent` picks up a model).
- `architect` is read-only (`commandExecutionPolicy: deny`, no edit tools) and
  returns a spec for an executor, consistent with `orchestrating-subagents`.
- Escalate-on-failure rule matches `orchestrating-subagents` rule 1.
- Context-isolation advice matches existing skills.

## Problems
1. **Unverified names/fields.** `gemini-4-carbon|argon|hydrogen`, `gemini-3.8-flash`,
   frontmatter fields (`commandExecutionPolicy`, `skills:`, tool names) and
   `workspace: "branch"` come from a chatbot answer; the paste itself says to verify
   via `/models`. Confirm against real agy docs before writing anything.
2. **Hard-codes model names into a SKILL.md.** `skills/adaptive-model-routing` uses
   abstract tiers (`flash_lite`, `flash`, `pro`) plus a Claude/OSS column. Hard-coding
   product names goes stale and is agy-only. The tiering plan
   (`docs/plans/2026-11-12-claude-tiering-trial.md`) chose one source of truth, no
   per-model forks. New models = new rows in the tier matrix.
3. **Crude routing.** Classifies by task type (Docker/Git -> Hydrogen) instead of the
   density signal (impact radius x ambiguity x safety criticality) and the
   test-time-compute vs parametric-capacity split. Ignores `right-sizing-process`.
   Description ("multi-step session") is broad enough to fire on nearly everything.
4. **`docker-git-ops` is generic and overlaps** `layered-verification-gates`,
   `committing-and-releasing-cleanly`, `hardening-ci-workflows`. No real verification
   gate or rollback; runs `docker compose up -d --build` without confirmation.
5. **Tool gaps.** `bulk-worker` can edit but not search (`search_directory` missing);
   `ops-executor` lacks `search_web`; `architect` "Carbon / Argon" is ambiguous.
6. **`SESSION_STATE.md`** duplicates `handing-off-sessions` and checkpoint hooks.

## Recommended path
- Verify real model IDs and frontmatter schema in agy (`/models`, docs).
- Add new models as rows in `skills/adaptive-model-routing` tier matrix and in
  `scripts/hooks/model_router.py`.
- Ship the three subagent profiles as an optional template under `templates/`
  (like `templates/cursor/`), not as skills; confine model names to those templates.
- Drop `session-router` and `docker-git-ops` as skills.

## Relevant existing files
- `skills/adaptive-model-routing/SKILL.md` (tier matrix, `invoke_subagent` hook)
- `skills/orchestrating-subagents/SKILL.md`
- `scripts/hooks/model_router.py`, `scripts/install.sh` (`--agy`, `~/.agents/skills`)
- `docs/MODEL-APPLICABILITY-REVIEW.md`, `docs/plans/2026-11-12-claude-tiering-trial.md`

## Verification & Implementation (2026-11-14)
- Verified `agy models` IDs: `gemini-3.8-flash-{low,medium,high}`, `gemini-4-hydrogen-{low,medium,high,xhigh}`, `gemini-4-argon-{low,medium,high}`, `gemini-4-carbon-{low,medium,high}`, `gemini-pro-orchestrator{,-argon}`, `claude-{sonnet,opus}-5-5-{low,medium,high}`, `gpt-oss-120b-medium`.
- Verified `agy` custom agent frontmatter via `agy plugin validate`: `model:` and `invoke_subagent` ONLY accept abstract tiers (`inherit|flash_lite|flash|pro`); concrete `agy models` IDs in agent `model:` fail validation (`Invalid model tier ... The loader skips this agent`) and are for main-session `--model` / `/model` only. `commandExecutionPolicy` accepts `off|auto|eager|sandbox` (not `deny`), `mainAgent`/`subagent` booleans, `tools` allowlist, `inheritMcp`/`inheritCustomizations` (no `skills:` field).
- Updated `skills/adaptive-model-routing/SKILL.md` tier matrix and `scripts/hooks/model_router.py` (`TIER_TO_AGY_MODEL` advisory output in `evaluate`; `pretooluse` keeps abstract tiers).
- Added `templates/agy/agents/{architect,ops-executor,bulk-worker}.md` and `templates/agy/agents/README.md`.
