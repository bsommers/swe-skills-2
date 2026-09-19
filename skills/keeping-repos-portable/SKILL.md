---
name: keeping-repos-portable
description: Use when writing scripts, configs, docs links or cross-repo references; when something works only on one machine or from one directory; when adding ports, paths or environment assumptions; or before sharing or containerizing a repo.
---

# Keeping Repos Portable

## Overview

A repo should work from a fresh clone on another machine, in CI, and in a container. Absolute paths, ambient state, and OS-specific shell features are the usual breakers — and easy to lint for.

## Rules

1. **No absolute paths in committed files.** No `/home/<user>`, `/Users/<user>`, `C:\…` in code, config, docs, or links. They break clones, containers, and leak usernames.
2. **Resolve from the script.**
   ```bash
   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
   ```
   Python: `Path(__file__).resolve().parent`.
3. **Env override with a relative fallback** for anything outside the repo:
   `SIBLING_DIR="${SIBLING_DIR:-$REPO_ROOT/../sibling}"`.
4. **Shebangs:** `#!/usr/bin/env bash`, `#!/usr/bin/env python3`.
5. **POSIX-safe shell.** Avoid bash-4-only features if macOS's bash 3.2 must run it (associative arrays, `mapfile`); avoid GNU-only flags (`sed -i` differs).
6. **Pin toolchains** and record versions; prefer lockfiles; use `uv` for Python when present with a `venv` fallback.
7. **Configurable ports and paths.** Defaults that collide with common services (8080) should be unusual or overridable via env.
8. **No ambient dependence.** Don't rely on files, env vars, running services, or global installs the repo doesn't document or create.
9. **Relative links in markdown.**
10. **Cross-repo references** are workspace-relative or env-driven; a repo works standalone.

## Lint

```bash
# fails on hardcoded home paths (adjust excludes)
grep -rnE '(/home/[A-Za-z0-9_-]+|/Users/[A-Za-z0-9_-]+|[A-Z]:\\\\Users)' \
  --exclude-dir={.git,node_modules,.venv,dist,build,target,__pycache__} \
  --exclude='*.lock' . && exit 1 || true
```
Also run a **clean-clone** test in a container or temp dir.

## Common mistakes

- Docs that link to `file:///home/…`.
- Scripts that only work when run from the repo root.
- Committing `.env` values instead of `.env.example`.
- "Works on my machine" env state: cached data, stale venvs, untracked outputs.
- Renaming a package after paths were hardcoded elsewhere.
