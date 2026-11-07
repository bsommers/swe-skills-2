# Periodic Checkpoint & Compaction Cadence (Hooks + Self-Check)

Agents judge their own context fullness poorly. Combine **automated lifecycle hooks** (`scripts/hooks/context_guard.py`) with **agent self-checks at natural task boundaries** so checkpoints stay fresh and context is compacted/reset before quality degrades or cold-cache penalties hit.

---

## 1. Automated Hook Triggers (`scripts/hooks/context_guard.py`)

Install hooks across harnesses so the runtime monitors turn/step cadence, token percentage, and idle gaps automatically:

```bash
python3 scripts/hooks/install-hooks.py --claude --agy --git
# If using Antigravity (agy), re-register plugin hooks:
agy plugin uninstall swe-skills && agy plugin install .
```

| Trigger | Threshold (Env Override) | Hook Event | Action Fired |
|---|---|---|---|
| **Periodic Turn Cadence (Claude)** | Every `12` assistant turns without a fresh `<20m` checkpoint (`SWE_SKILLS_CHECKPOINT_CADENCE_TURNS=12`) | `UserPromptSubmit` (`nudge`) | Injects `[context guard] Periodic checkpoint cadence reached...` reminder to update `docs/CHECKPOINT.md` at the next boundary and suggest `/compact` on phase switch. |
| **Periodic Step Cadence (`agy`)** | Every `25` steps without a fresh `<20m` checkpoint (`SWE_SKILLS_CHECKPOINT_CADENCE_STEPS=25`) | `PreInvocation` (`preinvocation`) | Injects ephemeral reminder to refresh `docs/CHECKPOINT.md` at the next stable boundary. |
| **Context Window Ceiling (Claude)** | `>= 70%` of window, then every `+10%` (`SWE_SKILLS_CONTEXT_PCT=70`) | `UserPromptSubmit` (`nudge`) | Mandates immediate pre-flight checkpoint + tailored `/compact keep: ...` or `/clear`. |
| **Step / Transcript Ceiling (`agy`)** | `>= 50` steps (then `+15`) or `>= 500 KB` transcript (`SWE_SKILLS_AGY_STEP_LIMIT=50`) | `PreInvocation` (`preinvocation`) | Mandates immediate `docs/CHECKPOINT.md` refresh + advising user to start a fresh session (`/exit`, `Ctrl+D`, or New Chat). |
| **Cold Prompt-Cache Resume** | `>= 30 min` idle with `>= 30k` tokens / `>= 15` steps (`SWE_SKILLS_IDLE_MINUTES=30`) | `UserPromptSubmit` / `PreInvocation` | Flags 12.5x expired prompt-cache rebuild cost; instructs agent to answer concisely, checkpoint, and compact/reset. |
| **Uncheckpointed Manual Compact** | No checkpoint modified in `< 20 min` (`SWE_SKILLS_CHECKPOINT_FRESH_MINUTES=20`) | `PreCompact` (`precompact`) | Exits `2` to block manual `/compact` until `docs/CHECKPOINT.md` is written. |
| **Post-Reset / Startup Continuity** | Checkpoint `< 12h` old on startup, or any age after `compact`/`clear` | `SessionStart` (`sessionstart`) | Auto-injects `docs/CHECKPOINT.md` / `docs/HANDOFF.md` and instructs agent to verify git/test state before acting. |

---

## 2. Agent Self-Check Cadence (When to Check & Suggest Without Waiting for a Nudge)

Even before a hook threshold fires (or in environments where hooks are not yet installed), check context status and refresh `docs/CHECKPOINT.md` at **every natural boundary**:

1. **At session start or project setup:**
   Run `python3 scripts/hooks/context_guard.py report`. If output shows `hooks: claude=missing` or `agy=missing`, recommend installing the hooks so periodic checkpointing and compaction nudges run automatically.
2. **After every completed phase, milestone, commit, or `/release`:**
   Refresh `docs/CHECKPOINT.md` while tests are green, and suggest `/compact` (Claude) or starting a fresh session (`agy`) before starting the next phase.
3. **At phase transitions (`using-swe-skills`):**
   When shifting from **Planning → Implementation → Verification/Review → Release**, checkpoint and compact/reset so stale phase skills and exploration logs do not replay on every tool turn.
4. **Every ~10–15 turns / ~25 tool steps during deep debugging or multi-file implementation:**
   Run `python3 scripts/hooks/context_guard.py report`. If `recommendation:` is `CHECKPOINT_DUE` or `COMPACT_OR_RESET_NOW`, write/update `docs/CHECKPOINT.md` immediately and surface the compaction/reset recommendation to the user.
5. **Before any pause > 5–15 minutes:**
   Write `docs/CHECKPOINT.md`, stop background watchers, and suggest `/compact` or `/exit` to avoid the 12.5x 5-minute prompt-cache expiration penalty.
