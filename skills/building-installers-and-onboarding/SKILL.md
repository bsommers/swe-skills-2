---
name: building-installers-and-onboarding
description: Use when planning, building, or remediating user setup and initialization commands (init, setup, doctor), multi-target installers (user home, global, or custom prefix), or in-tool workflow guidance and next-step hints that show users how to bootstrap and run a project.
---

# Building Installers and Onboarding

## Overview

A tool fails its first-time user when installing it requires root, running `<tool> init` exits with no hint of what to run next, or docs stop at installation without a bootstrap workflow. Apply this across **planning** (specify install scopes and user state transitions), **build** (implement the installer, `init`, and CLI breadcrumbs), and **post-build remediation** (fix onboarding dead-ends in an existing codebase). Pair with `building-small-cli-tools`, `keeping-repos-portable`, and `writing-user-guides`.

## 1. Multi-Target Installer (`install.sh` / package installer)

Provide a single idempotent installer supporting three target scopes (see `references/installer-template.sh`):

| Scope | Flag / Env | Default Paths | Privilege |
|---|---|---|---|
| **User home (default)** | `--local` | `${XDG_BIN_HOME:-$HOME/.local/bin}`, `${XDG_DATA_HOME:-$HOME/.local/share}/<tool>` | Unprivileged |
| **System global** | `--global` | `/usr/local/bin`, `/usr/local/share/<tool>` | Checks write access; fails cleanly if root is missing |
| **Custom path** | `--prefix DIR` / `PREFIX=DIR` | `DIR/bin`, `DIR/share/<tool>` | User-defined (CI, sandboxes, custom layout) |

Required installer behavior:
- Support `--local`, `--global`, `--prefix DIR`, `--dry-run`, `--uninstall`, `--force`, and `-h/--help`.
- Never overwrite unmanaged files without `--force`; `--uninstall` removes only what was installed.
- Check whether the target `bin` directory is in `$PATH`; if missing, print the exact `export PATH="<bin_dir>:$PATH"` line, then print the first command to run (`<tool> init`).

## 2. User Setup & Initialization (`<tool> init` & `doctor`)

- **Idempotent `<tool> init`:** Detect existing config or state; never clobber without `--force`. Support `--non-interactive` (or `--yes`) with sensible defaults for CI and unattended agents.
- **Preflight check (`<tool> doctor` / `check`):** Validate runtimes, env vars, credentials, and permissions before doing work, printing a one-line remedy per missing item.
- **Runnable starter state:** `<tool> init` must emit a valid config or starter project so the very next command succeeds out of the box.

## 3. In-Tool Workflow Guidance & Next-Step Hints

Never leave a user asking "`<tool> init` — then what?" (see `references/onboarding-cli-patterns.md`):

- **Progressive `Next steps:` breadcrumbs in code:** Every lifecycle command (`install`, `init`, `doctor`, `build`, or bare `<tool>`) prints 1–3 concrete, copy-pasteable next commands:
  ```text
  Initialized workspace in ./<tool>.toml
  Next steps:
    1. <tool> doctor              # verify environment and dependencies
    2. <tool> run example.yml     # execute your first workflow
    3. <tool> guide               # view the full end-to-end workflow guide
  ```
- **Built-in workflow guide (`<tool> guide` + `--help` epilog):** Embed the canonical lifecycle (`install → init → verify → run`) in the CLI so guidance works offline.
- **Synchronized docs (`writing-user-guides`):** Mirror the exact `install → init → next steps` walkthrough in `README.md` and `docs/user-guide/`, verified in a clean temp directory (`layered-verification-gates`).

## Phase Checklist

| Phase | Required Deliverables |
|---|---|
| **Planning** | Specify install scopes (`--local`, `--global`, `--prefix`), `<tool> init` outputs, and user state transitions (`installed → initialized → verified → running`) (`planning-with-contracts`). |
| **Build** | Implement `scripts/install.sh`, `<tool> init`, `<tool> doctor`, `<tool> guide`, and `Next steps:` hints; test all three scopes in `mktemp -d`. |
| **Post-Build Remediation** | Run a zero-state walkthrough in an empty dir; patch any command that exits silently or forces users to read source code to find the next step. |

## Common Mistakes

- **`init` dead-end:** Printing `"Initialized."` and exiting without naming created files or the next command.
- **Hardcoded destination:** Forcing `/usr/local/bin` (`sudo`) or a fixed `$HOME` path with no `--prefix`.
- **Interactive-only bootstrap:** Hanging in CI/agent runs because `init` prompts on stdin without `--non-interactive`.
- **Doc/CLI drift:** Quickstart commands in `README.md` that differ from the tool's `Next steps:` hints (`keeping-docs-in-sync`).
