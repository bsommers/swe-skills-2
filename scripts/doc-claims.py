#!/usr/bin/env python3
"""Mechanical doc-alignment pass: broken relative links, missing backticked paths, and count claims.

Count claims ("69 skills") are listed for manual verification; a real count is shown when the
noun matches a directory of that name. Paths in history files (CHANGELOG, checkpoints, plans) are not
checked; intentionally absent paths go in `.doc-claims-ignore` (globs). Exit 1 if broken links or paths are found. Stdlib only.
"""
import argparse
import fnmatch
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "dist", "__pycache__", "target", "docs/reviews"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
TICK = re.compile(r"`([A-Za-z0-9_.][A-Za-z0-9_./-]*/[A-Za-z0-9_.*/-]*|[A-Za-z0-9_-]+\.(?:md|py|sh|json|toml|ya?ml))`")
COUNT = re.compile(r"\b(\d{1,4})\s+([a-z][a-z-]{2,20})\b")
NOUN_SKIP = {"lines", "words", "days", "hours", "minutes", "seconds", "bytes", "tokens", "times", "chars", "px"}


HISTORY = ("CHANGELOG.md", "docs/CHECKPOINT.md", "docs/plans/")  # past-tense records: links checked, paths not
IGNORE_FILE = ".doc-claims-ignore"


def load_ignore(root):
    """Glob patterns (one per line, # comments) for backticked paths that are intentionally absent."""
    f = root / IGNORE_FILE
    if not f.is_file():
        return []
    return [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def docs(root):
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        if any(rel == s or rel.startswith(s + "/") or f"/{s}/" in f"/{rel}" for s in SKIP_DIRS):
            continue
        yield p


def real_counts(root):
    """noun -> count for each top-level or one-deep directory (skills -> 69)."""
    out = {}
    for d in [root, *[c for c in root.iterdir() if c.is_dir() and not c.name.startswith(".")]]:
        for c in d.iterdir():
            if c.is_dir() and not c.name.startswith("."):
                out[c.name.lower()] = len([x for x in c.iterdir() if not x.name.startswith(".")])
    return out


def scan(root):
    broken, counts = [], []
    real = real_counts(root)
    ignore = load_ignore(root)
    for p in docs(root):
        rel = p.relative_to(root).as_posix()
        in_fence = False
        example = rel.startswith(("skills/", "templates/") + HISTORY)  # these show example paths; check links only
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in LINK.finditer(line):
                t = m.group(1).split("#")[0]
                if t and not re.match(r"^[a-z]+:", t) and not t.startswith("/") and not (p.parent / t).exists():
                    broken.append((rel, i, "link", m.group(1)))
            for m in TICK.finditer(line if not example else ""):
                t = m.group(1)
                if "/" not in t or "*" in t or "<" in t or t.startswith(("~", "/", "http")) or t.count("/") == 0 and "." not in t:
                    continue
                if any(fnmatch.fnmatch(t, g) for g in ignore):
                    continue
                if not (root / t).exists() and not (p.parent / t).exists():
                    broken.append((rel, i, "path", t))
            for m in COUNT.finditer(line):
                n, noun = int(m.group(1)), m.group(2)
                if noun in NOUN_SKIP or n < 5:
                    continue
                actual = real.get(noun) if noun in real else real.get(noun.rstrip("s"))
                if actual is not None and actual != n:
                    counts.append((rel, i, f"claims {n} {noun}, found {actual}"))
    return broken, counts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", nargs="?", default=".")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"no such directory: {root}", file=sys.stderr)
        return 2
    broken, counts = scan(root)
    for rel, i, kind, t in broken:
        print(f"BROKEN {kind:4} {rel}:{i}  {t}")
    for rel, i, msg in counts:
        print(f"COUNT  {rel}:{i}  {msg}")
    print(f"\n{len(broken)} broken, {len(counts)} count mismatches (counts need manual confirmation)")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
