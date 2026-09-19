---
name: choosing-tools-and-substrates
description: Use when picking a language, framework, database, library, or runtime for a new component, when adding a dependency, or when a proposed stack seems chosen out of habit rather than fit.
---

# Choosing Tools and Substrates

## Overview

Choose by **measurable fit to the requirement**, not habit or fashion. No language is dogma; the cost of a choice includes build, deploy, maintenance, and how well it composes with what exists. Record the choice and the strongest rejected alternative in one line.

## Fit table (starting points, not laws)

| Requirement | Lean toward |
|---|---|
| Single static binary, sub-second startup, memory safety, CLI speed | Rust / Go / Zig |
| Glue, orchestration, data wrangling, graph ingestion, fast iteration | Python |
| Portable, accessible UI needing no install | HTML/CSS/JS (web standards) |
| Runs inside a browser page/extension | JavaScript/TypeScript |
| Reproducible small tool anyone can run | stdlib-only Python or shell |
| Formal parsing, strong types over an AST/IR | a typed functional language or TypeScript/Rust enums |
| Relationship-heavy queries | graph DB; otherwise a boring relational DB |
| Buffering bursts between producer and a slow writer | a queue, not a bigger DB |

## Procedure

1. Write the 2–4 requirements that actually discriminate (latency, footprint, deploy target, team skill, existing ecosystem).
2. Shortlist 2–3 options. Prototype only if the requirement is a real unknown; measure it.
3. Prefer the **standard library** for tooling. Every third-party dependency needs a one-line reason and a pinned version.
4. Prefer what composes: plain files, JSON, SARIF, CLI exit codes, HTTP. Interop across languages goes through these, not through shared runtimes.
5. Check operational cost: reproducible install, offline behavior, licensing, upgrade path, maintainer health.
6. Note the decision (see `defending-architecture-decisions` if hard to reverse).

## Python environments

Use `uv` (`uv venv`, `uv run`, lockfile) when available for fast, hermetic, reproducible installs. Fall back to `python -m venv` without failing when `uv` is absent (offline/legacy hosts).

## Pinning and drift

Pin exact tool and language versions (lockfiles, `rust-toolchain`, container tags). Watch for drift: a newer interpreter can change a stable-looking API (e.g. what types a seeding function accepts).

## Common mistakes

- Choosing the familiar stack for a requirement it can't meet (startup latency, footprint).
- A dependency for something 20 lines of stdlib does.
- Two languages where one would do, with no measured reason.
- Renaming your package the same as a dependency (shadowing); pick a distinct name.
- Deciding once and never revisiting when the requirement changes.
