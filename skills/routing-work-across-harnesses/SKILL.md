---
name: routing-work-across-harnesses
description: Use when a workflow must run on more than one agent harness (Claude Code, agy, opencode, pi, Cursor), when choosing model tiers or subagents without knowing which harness is in use, or when a plan names a model the current harness may not offer.
---

# Routing Work Across Harnesses

## Overview

Write workflows in **tiers and capabilities**, never in one vendor's model names or commands. Detect the harness, map tiers to what it offers, and degrade in a stated way when a capability is missing.

## Procedure

1. **Detect:** `scripts/detect-harness.py` (add `--json` for scripts). It reports harness, how it knew, subagent support, and suggested model per tier. `SWE_HARNESS=<name>` overrides a wrong guess.
2. **Pick a tier per task:**

| Tier | Use for |
|---|---|
| `fast` | file search, mechanical edits, test runs, lint fixes, formatting |
| `standard` | multi-file integration, survey lenses, debugging, routine review |
| `frontier` | architecture, security audit, plan synthesis, ambiguous trade-offs |

3. **Map to the harness** with `references/harness-matrix.md`: skill directories, subagent mechanism, how to set a model per subagent, native review commands.
4. **Degrade, don't fail:**
   - No per-subagent model: run the work in the main session and say so.
   - No subagents: run lenses sequentially, results written to files between steps.
   - Requested model absent: use the nearest tier, record the substitution in the output.
   - No skill loading: paste the skill body or the portable prompt.
5. **Keep one source.** Skills stay in `skills/`; per-harness differences live only in the matrix, installer targets and `templates/`.

## Rules

- Never hard-code a model ID in a skill; tiers only. IDs live in the matrix and in harness config.
- Escalate a tier on failure, not by default (`orchestrating-subagents`, `token-finops`).
- A harness fact you haven't verified is marked unverified in the matrix; run `scripts/detect-harness.py` and read the harness docs before relying on it.
- Subagent output contracts stay terse and identical across harnesses.

## Common mistakes

- Skill text that says "use /code-review" with no fallback.
- Assuming subagents exist, then silently running everything serially.
- Same strongest model for survey and synthesis.
- Forking a skill per harness instead of adding a matrix row.
