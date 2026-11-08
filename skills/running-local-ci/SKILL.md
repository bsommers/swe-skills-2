---
name: running-local-ci
description: Use when running CI checks, validating branches before push or PR, configuring GitHub Actions triggers, or testing across OS targets while conserving hosted GitHub Actions CI minutes as a standing rule.
---

# Running Local CI & Conserving GitHub Actions Minutes

## Overview

**Standing Rule:** Execute CI checks **locally** as much as possible and conserve hosted GitHub Actions minutes unless the user explicitly overrides this rule. Hosted CI is a final confirmation gate—never a scratchpad for iterative debugging.

## Core Rules

1. **Conserve hosted GitHub Actions minutes by default (Standing Rule).**
   - Never push unverified or intermediate "let's see if CI passes" commits to remote branches unless the user explicitly instructs you to run remote CI.
   - Batch work locally, run the full local CI gate to 100% green, and push once per completed milestone or PR (`committing-and-releasing-cleanly`).
2. **Run the complete CI pipeline locally before any push.**
   - Execute the repository's verification runner (`scripts/verify.sh`), linters, formatters, typecheckers, unit/integration tests, and security scans locally first (`layered-verification-gates`).
   - Use **`gha-vm-runners`** (`~/src/gha-vm-runners/local-ci.sh <repo>`) to mirror `.github/workflows/*.yml` steps directly on the local machine, or boot the disposable local KVM self-hosted runner (`~/src/gha-vm-runners/gha-vm-runners.sh start`) when full GitHub Actions workflow execution is needed without spending hosted minutes (`using-local-tool-registry`).
3. **Use local VMs for multi-OS CI matrix jobs (`using-local-tool-registry`).**
   - Instead of pushing to GitHub Actions to test Windows, Linux, or BSD targets:
     - **Windows x64 / ARM64:** Run tests inside `~/src/infra/win-devvm` (`./vm.sh start && ./vm.sh ssh`).
     - **Clean-room Linux / Containers / microVMs:** Run inside `~/src/ai/projects/cvm` (`cvm run --backend kvm -- ...`).
     - **Fedora / FreeBSD:** Run inside `~/src/infra/fedora-vms` or `~/src/vms/scripts`.
   - Shut down background VMs (`./vm.sh stop`, `./gha-vm-runners.sh stop`) once verification finishes to free host CPU/RAM.
4. **Configure `.github/workflows/*.yml` for minimal minute consumption (`hardening-ci-workflows`).**
   - Always set `concurrency` with `cancel-in-progress: true` so superseded pushes cancel immediately:
     ```yaml
     concurrency:
       group: ${{ github.workflow }}-${{ github.ref }}
       cancel-in-progress: true
     ```
   - Set explicit job `timeout-minutes:` (e.g., `10` or `15`) so hung jobs never burn 360 minutes.
   - Gate heavy multi-OS matrix, fuzzing, or E2E jobs to release tags (`v*`), `workflow_dispatch`, or relevant `paths:` filters—or disable automatic push triggers entirely when `local-ci.sh` is the active workflow.

## Reference

- Local CI mirroring script template, VM runner commands, and workflow throttling patterns: `references/local-ci-and-vm-runners.md`

## Common Mistakes

- **"Push-and-pray" debugging:** Pushing 5 commits in a row to fix linter or Windows path issues on GitHub Actions instead of running `scripts/verify.sh` or `win-devvm` locally.
- **Missing `cancel-in-progress: true`:** Letting 3 obsolete workflow runs finish in parallel when a branch is updated.
- **No `timeout-minutes` on jobs:** A single deadlocked test burning 6 hours of hosted runner quota.
- **Leaving heavy VMs running idle:** Forgetting `./gha-vm-runners.sh stop` or `./vm.sh stop` after local CI completes.
