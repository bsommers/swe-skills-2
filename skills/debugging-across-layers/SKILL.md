---
name: debugging-across-layers
description: Use when a failure persists no matter which setting you change, when behavior differs between environments, when imports or config resolve to the wrong thing, or after resuming work from a checkpoint where state may have changed.
---

# Debugging Across Layers

## Overview

Complements systematic root-cause debugging (find the cause before fixing). This skill covers the class where **the cause lives in a layer you aren't looking at**: server config below the client, a shadowed package, stale state, a leaked resource.

## Procedure

1. **Name the layers** the request crosses: caller → library → proxy → service → runtime → OS/hardware.
2. **Vary one knob** and record whether the failure *point* moves (time, count, message). If it doesn't move after 2–3× changes, stop tuning that knob.
3. **Inspect effective state at the lower layer,** not your intent: loaded model/context size, container `inspect`, resolved config, process env dump, `pip show`/`which`, actual open ports.
4. **Run the cheap suspects checklist** below.
5. **Reproduce minimally,** then fix at the layer where the cause lives.
6. **Add a regression test or a startup assertion** that would have caught it (e.g. verify the effective limit at boot and log it).

## Cheap suspects

| Suspect | Check |
|---|---|
| Shadowed module (local dir named like a dependency) | `python -c "import x; print(x.__file__)"` |
| Version drift in stdlib/runtime behavior | seed/typing/API errors after an interpreter upgrade |
| Port or resource already in use | `ss -ltnp`; change default, make configurable |
| Env var not honored by *every* code path | grep for hardcoded paths; single settings module |
| Resource leak | connections/handles created per call, never closed; DB refuses after N |
| Stale or missing state | generated data "gone", untracked files, caches |
| Wrong environment | venv/container differs from the one you tested |
| Overridden request params | server ignores per-request options you set |

## Resuming from a checkpoint

Never trust a handoff note's *state* claims. Re-verify: do the files it says exist still exist? Are services up? Did the branch move? A checkpoint said "data generated" — the data directory was empty. Regenerate, then continue.

## Common mistakes

- Escalating a parameter a fourth time.
- Fixing in the wrong layer (bigger client timeout for a server-side context cap).
- Assuming the environment you debugged in is the one that failed.
- Fix without the guard that would have surfaced it earlier.

Pairs with `sizing-limits-from-measurement` and `handing-off-sessions`.
