#!/usr/bin/env python3
"""Detect which agent harness is running this process and print tier -> model suggestions.

Order: SWE_HARNESS override, known env vars, ancestor process names, else "unknown".
Heuristic only; override with SWE_HARNESS=claude|agy|opencode|pi|cursor. Stdlib only.
"""
import argparse
import json
import os
import subprocess
import sys

# harness -> (env vars that imply it, process-name tokens, subagents, {tier: suggestion})
HARNESSES = {
    "claude": (("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT"), ("claude",), "yes",
               {"fast": "haiku", "standard": "sonnet", "frontier": "opus"}),
    "agy": (("ANTIGRAVITY_AGENT", "AGY_SESSION"), ("agy", "antigravity"), "yes",
            {"fast": "flash", "standard": "flash", "frontier": "pro"}),
    "opencode": (("OPENCODE",), ("opencode",), "yes",
                 {"fast": "<cheapest configured>", "standard": "<mid configured>", "frontier": "<strongest configured>"}),
    "pi": (("PI_CODING_AGENT",), ("pi",), "no",
           {"fast": "<cheapest via --model>", "standard": "<mid via --model>", "frontier": "<strongest via --model>"}),
    "cursor": (("CURSOR_AGENT", "CURSOR_TRACE_ID"), ("cursor-agent", "cursor"), "yes",
               {"fast": "fast", "standard": "inherit", "frontier": "<strongest selectable>"}),
}
UNKNOWN_TIERS = {"fast": "?", "standard": "?", "frontier": "?"}


def ancestor_names(pid=None, limit=12):
    """Process names from the parent upward. Linux /proc first, `ps` fallback; [] if neither works."""
    names, pid = [], pid or os.getppid()
    for _ in range(limit):
        if pid <= 1:
            break
        try:
            with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
                stat = fh.read()
            name = stat[stat.index("(") + 1:stat.rindex(")")]
            ppid = int(stat[stat.rindex(")") + 2:].split()[1])
        except (OSError, ValueError):
            try:
                out = subprocess.run(["ps", "-o", "comm=,ppid=", "-p", str(pid)],
                                     capture_output=True, text=True, timeout=3).stdout.split()
                name, ppid = os.path.basename(out[0]), int(out[-1])
            except (OSError, ValueError, IndexError, subprocess.SubprocessError):
                break
        names.append(name.lower())
        pid = ppid
    return names


def detect(env=None, ancestors=None):
    env = os.environ if env is None else env
    forced = env.get("SWE_HARNESS", "").strip().lower()
    if forced:
        if forced in HARNESSES:
            return forced, "SWE_HARNESS"
        return "unknown", f"SWE_HARNESS={forced!r} is not one of {sorted(HARNESSES)}"
    for name, (vars_, _, _, _) in HARNESSES.items():
        for v in vars_:
            if env.get(v):
                return name, f"env {v}"
    names = ancestor_names() if ancestors is None else ancestors
    for n in names:
        for name, (_, tokens, _, _) in HARNESSES.items():
            if n in tokens:
                return name, f"ancestor process {n}"
    return "unknown", "no signal"


def report(env=None, ancestors=None):
    name, how = detect(env, ancestors)
    if name == "unknown":
        return {"harness": name, "detected_by": how, "subagents": "unknown", "tiers": UNKNOWN_TIERS}
    _, _, subagents, tiers = HARNESSES[name]
    return {"harness": name, "detected_by": how, "subagents": subagents, "tiers": tiers}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args(argv)
    r = report()
    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"harness={r['harness']}  (detected by: {r['detected_by']})")
        print(f"subagents={r['subagents']}")
        for t in ("fast", "standard", "frontier"):
            print(f"tier.{t}={r['tiers'][t]}")
        if r["harness"] == "unknown":
            print("hint: set SWE_HARNESS=claude|agy|opencode|pi|cursor; see skills/routing-work-across-harnesses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
