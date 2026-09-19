#!/usr/bin/env python3
"""Fire the `compacting-context-safely` skill at the right moments.

Three hook handlers, one script, stdlib only. Each reads a hook JSON payload on
stdin and writes the hook's JSON output on stdout:

  nudge         UserPromptSubmit — when context passes a threshold, tell the
                agent to load the skill and checkpoint while it still has room.
  precompact    PreCompact — block a *manual* /compact when no fresh checkpoint
                exists (exit 2); never blocks auto-compaction.
  sessionstart  SessionStart — after /compact or /clear, inject the newest
                checkpoint so continuity is verified, not guessed.
  report        Not a hook: print context use as text (status lines, debugging).

Configuration (all optional, env vars):
  SWE_SKILLS_CONTEXT_LIMIT            context window in tokens (default 200000)
  SWE_SKILLS_CONTEXT_PCT              first nudge at this %% used (default 70)
  SWE_SKILLS_CONTEXT_PCT_STEP         re-nudge every N more %% (default 10)
  SWE_SKILLS_CONTEXT_GUARD_BLOCK      1 = block stale manual /compact (default 1)
  SWE_SKILLS_CHECKPOINT_GLOBS         os.pathsep-separated globs, relative to cwd
  SWE_SKILLS_CHECKPOINT_FRESH_MINUTES checkpoint age allowed by precompact (default 20)
  SWE_SKILLS_CHECKPOINT_FRESH_HOURS   checkpoint age injected at session start (default 12)
  SWE_SKILLS_CONTEXT_GUARD_STATE_DIR  where per-session nudge state is kept
  SWE_SKILLS_CONTEXT_GUARD_DEBUG      1 = report internal errors on stderr

A hook that fails must never break the session: unexpected errors exit 0 silently.
"""
import glob
import json
import os
import sys
import time
import traceback
from pathlib import Path

SKILL = "compacting-context-safely"
DEFAULT_GLOBS = [
    "docs/plans/*checkpoint*.md",
    "docs/checkpoints/*.md",
    "docs/CHECKPOINT.md",
    "CHECKPOINT.md",
    ".claude/checkpoints/*.md",
]
MAX_INJECT_CHARS = 4000


def env_int(name, default):
    try:
        return int(os.environ[name])
    except (KeyError, ValueError):
        return default


def env_flag(name, default=True):
    return os.environ.get(name, "1" if default else "0").strip().lower() not in ("0", "false", "no", "")


# ---------------------------------------------------------------- transcript

def context_used(transcript_path):
    """Tokens held by the last main-thread assistant turn, or None if unknown."""
    if not transcript_path:
        return None
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue  # a partially written line: keep looking backwards
        if rec.get("type") != "assistant" or rec.get("isSidechain"):
            continue
        usage = (rec.get("message") or {}).get("usage") or {}
        total = sum(
            usage.get(k) or 0
            for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
        )
        if total > 0:
            return total
    return None


def pct_used(payload):
    used = context_used(payload.get("transcript_path"))
    if used is None:
        return None, None
    limit = max(env_int("SWE_SKILLS_CONTEXT_LIMIT", 200000), 1)
    return used, used * 100.0 / limit


# --------------------------------------------------------------- checkpoints

def checkpoints(cwd):
    pats = os.environ.get("SWE_SKILLS_CHECKPOINT_GLOBS")
    pats = pats.split(os.pathsep) if pats else DEFAULT_GLOBS
    base = Path(cwd or ".")
    found = []
    for pat in pats:
        pat = pat.strip()
        if not pat:
            continue
        root = Path(pat) if os.path.isabs(pat) else base / pat
        for hit in glob.glob(str(root)):
            p = Path(hit)
            try:
                if p.is_file():
                    found.append((p.stat().st_mtime, p))
            except OSError:
                continue
    found.sort(reverse=True)
    return [p for _, p in found]


def newest_checkpoint(cwd, max_age_seconds=None):
    for p in checkpoints(cwd):
        try:
            age = time.time() - p.stat().st_mtime
        except OSError:
            continue
        if max_age_seconds is None or age <= max_age_seconds:
            return p
    return None


# -------------------------------------------------------------------- state

def state_file(session_id):
    base = os.environ.get("SWE_SKILLS_CONTEXT_GUARD_STATE_DIR")
    if not base:
        base = os.path.join(
            os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state"),
            "swe-skills", "context-guard",
        )
    return Path(base) / f"{session_id or 'unknown'}.json"


def read_state(session_id):
    try:
        return json.loads(state_file(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def write_state(session_id, data):
    f = state_file(session_id)
    try:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(data), encoding="utf-8")
    except OSError:
        pass  # state is an optimization; losing it only means an extra nudge


# ------------------------------------------------------------------ output

def emit(event, context):
    json.dump({"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}, sys.stdout)
    sys.stdout.write("\n")


# ---------------------------------------------------------------- handlers

def cmd_nudge(payload):
    used, pct = pct_used(payload)
    if pct is None:
        return 0
    first = env_int("SWE_SKILLS_CONTEXT_PCT", 70)
    step = max(env_int("SWE_SKILLS_CONTEXT_PCT_STEP", 10), 1)
    if pct < first:
        return 0
    session = payload.get("session_id")
    state = read_state(session)
    last = state.get("last_nudge_pct")
    if last is not None and pct < last + step:
        return 0
    state["last_nudge_pct"] = int(pct // step * step)
    write_state(session, state)

    cp = newest_checkpoint(payload.get("cwd"), env_int("SWE_SKILLS_CHECKPOINT_FRESH_MINUTES", 20) * 60)
    have = f"A recent checkpoint exists at {cp}; update it rather than starting a new one." if cp else \
        "No recent checkpoint was found."
    emit("UserPromptSubmit", (
        f"[context guard] About {pct:.0f}% of the context window is used ({used} tokens). "
        f"Load the `{SKILL}` skill and follow its pre-flight before the window fills: reach a stable "
        f"point, then write or refresh a checkpoint (user decisions verbatim, dead ends, working-tree and "
        f"background-process state, authorizations, exact next command). {have} "
        f"Answer the user's request first if it is short; do not silently ignore this."
    ))
    return 0


def cmd_precompact(payload):
    trigger = (payload.get("trigger") or "").strip().lower()
    cwd = payload.get("cwd")
    fresh = env_int("SWE_SKILLS_CHECKPOINT_FRESH_MINUTES", 20) * 60
    cp = newest_checkpoint(cwd, fresh)
    if trigger == "auto":
        # Auto-compaction fires when the window is already full; the agent gets no
        # turn to checkpoint, so blocking here would stall the session.
        return 0
    if cp or not env_flag("SWE_SKILLS_CONTEXT_GUARD_BLOCK"):
        return 0
    minutes = env_int("SWE_SKILLS_CHECKPOINT_FRESH_MINUTES", 20)
    sys.stderr.write(
        f"[context guard] Compaction blocked: no checkpoint modified in the last {minutes} min "
        f"(looked for {', '.join(os.environ.get('SWE_SKILLS_CHECKPOINT_GLOBS', os.pathsep.join(DEFAULT_GLOBS)).split(os.pathsep))} under {cwd or '.'}).\n"
        f"Load the `{SKILL}` skill, run its pre-flight, write the checkpoint, then run /compact again. "
        f"To compact anyway: SWE_SKILLS_CONTEXT_GUARD_BLOCK=0.\n"
    )
    return 2


def cmd_sessionstart(payload):
    source = (payload.get("source") or "").strip().lower()
    after_reset = source in ("compact", "clear")
    max_age = None if after_reset else env_int("SWE_SKILLS_CHECKPOINT_FRESH_HOURS", 12) * 3600
    cp = newest_checkpoint(payload.get("cwd"), max_age)
    if not cp:
        if after_reset:
            emit("SessionStart", (
                f"[context guard] Context was reset ({source}) and no checkpoint file was found. "
                f"Do not assume earlier decisions survived: restate the goal and next step, and ask the "
                f"user about anything unclear rather than reconstructing it. See the `{SKILL}` skill."
            ))
        return 0
    try:
        body = cp.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    if len(body) > MAX_INJECT_CHARS:
        body = body[:MAX_INJECT_CHARS] + f"\n… truncated; read {cp} in full."
    when = time.strftime("%Y-%m-%d %H:%M", time.localtime(cp.stat().st_mtime))
    lead = f"Context was reset ({source})." if after_reset else "Session started with a recent checkpoint."
    emit("SessionStart", (
        f"[context guard] {lead} Checkpoint {cp} (modified {when}):\n\n{body}\n\n"
        f"Per the `{SKILL}` skill: verify these state claims (branch, git status, files, background jobs) "
        f"and rerun the baseline check before continuing. Treat approvals recorded above as expired for "
        f"anything outward-facing."
    ))
    return 0


def cmd_report(payload):
    used, pct = pct_used(payload)
    cwd = payload.get("cwd") or os.getcwd()
    if pct is None:
        print("context: unknown (no usage found in transcript)")
    else:
        print(f"context: {used} tokens, {pct:.0f}% of {env_int('SWE_SKILLS_CONTEXT_LIMIT', 200000)}")
    cp = newest_checkpoint(cwd)
    print(f"checkpoint: {cp}" if cp else "checkpoint: none found")
    return 0


HANDLERS = {"nudge": cmd_nudge, "precompact": cmd_precompact, "sessionstart": cmd_sessionstart, "report": cmd_report}


def main(argv):
    if len(argv) != 2 or argv[1] not in HANDLERS:
        sys.stderr.write(f"usage: {Path(argv[0]).name} {{{'|'.join(HANDLERS)}}}  (hook JSON on stdin)\n")
        return 2
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    payload.setdefault("cwd", os.getcwd())
    return HANDLERS[argv[1]](payload)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except SystemExit:
        raise
    except Exception:  # a broken hook must not break the session
        if env_flag("SWE_SKILLS_CONTEXT_GUARD_DEBUG", False):
            traceback.print_exc()
        sys.exit(0)
