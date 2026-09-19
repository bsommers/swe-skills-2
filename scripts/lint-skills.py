#!/usr/bin/env python3
"""Lint every skills/*/SKILL.md: frontmatter, naming, discovery, cross-references, portability.

Supporting files (e.g. references/) are checked for portability and TODO/TBD too.

Exit 0 when clean, 1 when any error is found. Stdlib only.
Usage: python3 scripts/lint-skills.py [--words]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ABS_PATH_RE = re.compile(r"(/home/[A-Za-z0-9_-]+|/Users/[A-Za-z0-9_-]+)")
MAX_DESC = 1024
WARN_DESC = 500
WARN_WORDS = 900


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def main():
    show_words = "--words" in sys.argv
    names = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    errors, warnings = [], []
    total_words = 0
    prefixes = {n.split("-", 1)[0] for n in names}

    for name in names:
        f = SKILLS / name / "SKILL.md"
        if not f.exists():
            errors.append(f"{name}: missing SKILL.md")
            continue
        text = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{name}: no YAML frontmatter")
            continue
        if fm.get("name") != name:
            errors.append(f"{name}: frontmatter name {fm.get('name')!r} != directory")
        if not NAME_RE.match(name):
            errors.append(f"{name}: name must be lowercase letters, digits, hyphens")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{name}: missing description")
        else:
            if len(desc) > MAX_DESC:
                errors.append(f"{name}: description {len(desc)} chars > {MAX_DESC}")
            elif len(desc) > WARN_DESC:
                warnings.append(f"{name}: description {len(desc)} chars (> {WARN_DESC} preferred)")
            if not desc.startswith("Use when"):
                errors.append(f"{name}: description must start with 'Use when'")
            if re.search(r"\b(I|my|we|our)\b", desc):
                errors.append(f"{name}: description must be third person")
        extra = set(fm) - {"name", "description"}
        if extra:
            warnings.append(f"{name}: extra frontmatter keys {sorted(extra)}")
        if ABS_PATH_RE.search(text):
            errors.append(f"{name}: contains an absolute home path")
        if "TODO" in text or "TBD" in text:
            errors.append(f"{name}: contains TODO/TBD")
        # cross-references: `some-skill-name` in backticks must exist when it looks like a skill id
        for ref in set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", body)):
            if ref in names:
                continue
            # only flag hyphenated tokens whose leading word matches an existing skill's
            if ref.split("-", 1)[0] in prefixes:
                errors.append(f"{name}: references unknown skill `{ref}`")
        for extra_file in sorted(p for p in (SKILLS / name).rglob("*") if p.is_file() and p != f):
            rel = extra_file.relative_to(SKILLS)
            try:
                extra_text = extra_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if ABS_PATH_RE.search(extra_text):
                errors.append(f"{rel}: contains an absolute home path")
            if "TODO" in extra_text or "TBD" in extra_text:
                errors.append(f"{rel}: contains TODO/TBD")
        words = len(body.split())
        total_words += words
        if words > WARN_WORDS:
            warnings.append(f"{name}: {words} words (> {WARN_WORDS}); consider a references/ file")
        if show_words:
            print(f"{words:5d}  {name}")

    # router must list every other skill
    router = (SKILLS / "using-swe-skills" / "SKILL.md").read_text(encoding="utf-8")
    for name in names:
        if name != "using-swe-skills" and f"`{name}`" not in router:
            errors.append(f"router: using-swe-skills does not mention `{name}`")

    print(f"{len(names)} skills, {total_words} words total")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
