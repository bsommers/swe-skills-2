---
name: building-installers-and-onboarding
description: Use when planning, building, or remediating user setup and initialization commands (init, setup, doctor), multi-target installers (user home, global, or custom prefix), or in-tool workflow guidance and next-step hints that show users how to bootstrap and run a project.
---

# Building Installers and Onboarding

## Overview

A tool fails its first-time user when installing it requires root, `<tool> init` exits with no hint of what to run next, or docs stop at installation. Apply this across **planning**, **build**, and **post-build remediation**. Pair with `building-small-cli-tools`, `keeping-repos-portable`, and `writing-user-guides`.

## 1. Multi-Target Installer (`install.sh` / package wrapper)

Provide one idempotent installer supporting three scopes (`references/installer-template.sh`):

| Scope | Flag / Env | Default Paths | Privilege |
|---|---|---|---|
| **User home (default)** | `--local` | `${XDG_BIN_HOME:-$HOME/.local/bin}`, `${XDG_DATA_HOME:-$HOME/.local/share}/<tool>` | Unprivileged |
| **System global** | `--global` | `/usr/local/bin`, `/usr/local/share/<tool>` | Checks write access |
| **Custom path** | `--prefix DIR` / `PREFIX=DIR` | `DIR/bin`, `DIR/share/<tool>` | User-defined (CI, sandboxes) |

Required behavior:
- Support `--local`, `--global`, `--prefix DIR`, `--copy`, `--dry-run`, `--uninstall`, `--force`, and `-h/--help`.
- Resolve `--prefix` to an absolute path. Default `--global` to `--copy` mode so global installs do not symlink into a private home checkout.
- For packaged CLIs (`pyproject.toml`, `Cargo.toml`, `package.json`), delegate to the native installer (`pip install --prefix`, `cargo install --root`, `npm install --prefix`) so entry points are preserved.
- Never clobber unmanaged files without `--force`; `--uninstall` removes only managed artifacts.
- If target `bin` is missing from `$PATH`, print `export PATH="<bin_dir>:$PATH"` and the first command (`<tool> init`).

## 2. User Setup & Initialization (`<tool> init` & `doctor`)

- **Idempotent `<tool> init`:** Detect existing state; never overwrite without `--force`. Support `--non-interactive` (`--yes`) for CI and agents.
- **Preflight (`<tool> doctor`):** Validate runtimes, env vars, credentials, and permissions, printing a one-line remedy per missing item.
- **Runnable starter state:** `<tool> init` must emit a valid config or starter project so the next command succeeds immediately.

## 3. In-Tool Workflow Guidance & Next-Step Hints

Never leave a user asking "`<tool> init` — then what?" (`references/onboarding-cli-patterns.md`):

- **Progressive `Next steps:` breadcrumbs (to `stderr`):** Lifecycle commands (`install`, `init`, `doctor`, `build`, or bare `<tool>`) print 1–3 copy-pasteable next commands to `stderr` (suppressed under `--quiet`/`--json`):
  ```text
  Initialized workspace in ./<tool>.toml
  Next steps:
    1. <tool> doctor              # verify environment and dependencies
    2. <tool> run example.yml     # execute your first workflow
    3. <tool> guide               # view the full workflow guide
  ```
- **Built-in guide (`<tool> guide` + `--help` epilog):** Embed the lifecycle (`install → init → verify → run`) in the CLI for offline reference.
- **Synchronized docs (`writing-user-guides`):** Mirror the `install → init → next steps` walkthrough in `README.md` and `docs/user-guide/`, verified in `mktemp -d` (`layered-verification-gates`).

## Phase Checklist

- **Planning:** Specify install scopes (`--local`, `--global`, `--prefix`), `init` outputs, and state transitions (`installed → initialized → verified → running`) (`planning-with-contracts`).
- **Build:** Implement `scripts/install.sh`, `init`, `doctor`, `guide`, and `Next steps:` hints; test all scopes in `mktemp -d`.
- **Post-Build Remediation:** Run a zero-state walkthrough in an empty dir; patch any command that exits silently or lacks recovery hints before `init`.

## Common Mistakes

- **`init` dead-end:** Exiting after `"Initialized."` without naming created files or the next command.
- **Stdout pollution:** Printing `Next steps:` to `stdout` instead of `stderr`, breaking pipes.
- **Hardcoded or relative paths:** Forcing `/usr/local/bin` or emitting relative paths in `export PATH`.
- **Interactive-only `init`:** Hanging in CI/agent runs when stdin prompts lack `--non-interactive`.
- **Doc/CLI drift:** `README.md` quickstart differing from `Next steps:` hints (`keeping-docs-in-sync`).
