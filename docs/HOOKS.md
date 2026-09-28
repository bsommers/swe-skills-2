# Context-guard hooks (opt-in)

The `compacting-context-safely` skill only helps if it loads at the right moment, and an agent
is a poor judge of how full its own context is. These hooks let the harness fire it instead.
Nothing here is active until you install it.

| Hook | Event | Behavior |
|---|---|---|
| `nudge` | `UserPromptSubmit` | Reads token usage from the transcript. Past a threshold (default 70%), injects a reminder to load the skill, checkpoint **while there is still room**, and provide the user with a tailored `/compact` command. Re-fires every +10%. |
| `preinvocation` | `PreInvocation` (agy) | Runs before model generation in Antigravity. When session steps (default 50) or transcript size exceeds limits, injects an ephemeral checkpoint and fresh session reminder. Also provides adaptive model routing hints for high-complexity prompts. |
| `pretooluse` | `PreToolUse` (agy) | Intercepts `invoke_subagent` calls. Evaluates prompt and role complexity, automatically overwriting `Model` (`pro`, `flash`, `flash_lite`) to conserve tokens. |
| `precompact` | `PreCompact` | On a **manual** `/compact` with no checkpoint touched in the last 20 min, exits 2 to block and says what to do. On **auto**-compaction it never blocks: the window is already full and the agent gets no turn to checkpoint, so blocking would stall the session. |
| `sessionstart` | `SessionStart` (`compact`, `clear`, `resume`) | Injects the newest checkpoint plus the skill's verify-continuity instructions. With no checkpoint after a reset, it says so, and tells the agent to ask rather than reconstruct. |
| `pre-commit` | Git `pre-commit` | Blocks git commits containing absolute home paths, unmasked secrets/keys, manifest version mismatches, or skill linter failures (`git_pre_commit.py`). |

`scripts/hooks/context_guard.py report` prints current use and the checkpoint it found — useful in a
status line or when checking configuration.

## Install

```bash
scripts/hooks/install-hooks.py --claude              # ~/.claude/settings.json
scripts/hooks/install-hooks.py --claude --project .  # this repo's .claude/settings.json
scripts/hooks/install-hooks.py --agy                 # Antigravity (SessionStart and PreInvocation)
scripts/hooks/install-hooks.py --git                 # .git/hooks/pre-commit
```

Add `--dry-run` to preview, `--uninstall` to remove. Hooks default to executing via `uv run` if `uv` is found on `PATH` (configurable via `--uv` or `--no-uv`). Installing is idempotent, backs up an existing
`settings.json`, and leaves hooks you added yourself alone.

For `agy`, the plugin must be re-imported before the new hooks register (installing over an existing
import updates the files but not the recorded components):

```bash
scripts/hooks/install-hooks.py --agy
agy plugin uninstall swe-skills && agy plugin install .   # components become [skills, hooks]
```

Check with `agy plugin list`. agy copies the plugin, so re-run this after changing `hooks.json`; the
copied hook command still points at this repo's script, so edits to `context_guard.py` take effect
immediately.

**Antigravity (`agy`) context guard.** `agy` loads plugin hooks from a root `hooks.json` and supports
`SessionStart` and `PreInvocation` (it has no in-place `/compact` or `PreCompact`). `--agy` installs
both hooks: `PreInvocation` monitors step count (default 50) and transcript size, injecting an
ephemeral checkpoint reminder when context grows large, while `SessionStart` injects the newest
checkpoint on startup or reset. `--agy` writes `hooks.json` at the plugin root and gitignores it,
so installing the plugin never turns hooks on for someone who did not ask.

## Configure

Environment variables, all optional:

| Variable | Default | Meaning |
|---|---|---|
| `SWE_SKILLS_CONTEXT_LIMIT` | `200000` | Context window size in tokens |
| `SWE_SKILLS_CONTEXT_PCT` | `70` | First nudge at this percent used |
| `SWE_SKILLS_CONTEXT_PCT_STEP` | `10` | Re-nudge every N more percent |
| `SWE_SKILLS_AGY_STEP_LIMIT` | `50` | Step count before agy nudge |
| `SWE_SKILLS_AGY_STEP_STEP` | `15` | Re-nudge agy every N more steps |
| `SWE_SKILLS_AGY_BYTES_LIMIT` | `500000` | Transcript bytes before agy nudge |
| `SWE_SKILLS_MODEL_ROUTER_ENABLED` | `1` | `0` disables adaptive model routing in hooks |
| `SWE_SKILLS_MODEL_ROUTER_DEFAULT_TIER` | `flash` | Fallback tier for standard tasks (`flash` / `flash_lite`) |
| `SWE_SKILLS_MODEL_ROUTER_DEBUG` | `0` | `1` prints router debug diagnostics to stderr |
| `SWE_SKILLS_CONTEXT_GUARD_BLOCK` | `1` | `0` stops blocking manual `/compact` |
| `SWE_SKILLS_CHECKPOINT_GLOBS` | see below | `:`-separated globs, relative to cwd |
| `SWE_SKILLS_CHECKPOINT_FRESH_MINUTES` | `20` | Checkpoint age the compaction guard accepts |
| `SWE_SKILLS_CHECKPOINT_FRESH_HOURS` | `12` | Checkpoint age injected at an ordinary session start |
| `SWE_SKILLS_CONTEXT_GUARD_DEBUG` | `0` | `1` prints internal errors to stderr |

Default checkpoint globs: `docs/plans/*checkpoint*.md`, `docs/checkpoints/*.md`, `docs/CHECKPOINT.md`,
`CHECKPOINT.md`, `.claude/checkpoints/*.md`.

## Notes and limits

- A hook that fails must not break a session, so unexpected errors exit 0 silently. Set
  `SWE_SKILLS_CONTEXT_GUARD_DEBUG=1` when something seems not to fire.
- Token use comes from the last main-thread assistant turn in the transcript; subagent
  (`isSidechain`) turns are ignored, since they don't consume the main window. The transcript is
  written asynchronously, so the reading can lag by a turn.
- The context limit isn't in the transcript. If your model's window isn't 200k, set
  `SWE_SKILLS_CONTEXT_LIMIT`, or the percentages will be wrong.
- The installed commands embed absolute paths to this repo and to the Python that ran the installer.
  Re-run the installer after moving the repo.
- Tests: `python3 -m unittest discover tests`.
