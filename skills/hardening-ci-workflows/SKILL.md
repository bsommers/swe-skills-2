---
name: hardening-ci-workflows
description: Use when writing or reviewing CI/CD workflow files (GitHub Actions or similar), adding third-party actions, granting workflow permissions, adding a dependency policy or format gate, or when a workflow handles pull requests from forks.
---

# Hardening CI Workflows

## Overview

A workflow runs with your repo's credentials on code and inputs you don't fully control. Treat the workflow file as a trust boundary (`hardening-trust-boundaries`): pin what you import, minimize what it can do, never let data become shell code.

## Rules

1. **Pin third-party actions to a full commit SHA** with the tag as a comment: `uses: org/action@<40-hex> # v1.2.3`. Tags move; SHAs don't.
2. **Verify the SHA resolves to that tag** before committing, e.g. `gh api repos/OWNER/REPO/commits/TAG -q .sha`. A pin that doesn't match its comment is worse than none.
3. **Least privilege.** Workflow-level `permissions: contents: read`; grant `write` only on the single job that needs it.
4. **Checkout with `persist-credentials: false`** unless a later step must push.
5. **No expression interpolation into `run:`.** Never write `${{ inputs.x }}` or `${{ github.event.* }}` inside a script (script injection). Pass via `env:` and quote `"$VAR"`.
6. **Untrusted code uses `pull_request`**, not `pull_request_target` (which runs with secrets and write token on fork code).
7. **`concurrency` & quota conservation (`running-local-ci`).** Set a `concurrency` group per ref with `cancel-in-progress: true`, set explicit `timeout-minutes` on every job, and gate heavy multi-OS matrices to tags or `workflow_dispatch` so routine work runs via local CI (`using-local-tool-registry`) and conserves hosted GitHub Actions minutes.
8. **Dependency policy gate** (cargo-deny, `npm audit`, pip-audit equivalent): advisories, license allowlist, unknown registries and git sources denied, wildcard versions denied. Derive the license allowlist from the real dependency tree and justify each license inline.
9. **Failures are readable.** Print failure excerpts inside collapsible log groups so the cause is visible without downloading artifacts.
10. **Test on every OS you ship to** — run cross-OS checks locally first via VMs (`using-local-tool-registry`, `running-local-ci`) before burning remote matrix minutes.
11. **Format gate with legacy drift:** land a mechanical format-only PR first, then enable the gate. Never mix them.

## Landing order

Portability fixes that CI depends on (`keeping-repos-portable`) -> format-only PR -> CI/infra PR -> everything else.

## Common mistakes

- SHA copied from a fork or a different tag than the comment.
- Job-level `write` copied to the whole workflow.
- `pull_request_target` "because secrets are needed" on fork code.
- License allowlist pasted from another project, so it permits things you never audited.
- Enabling a gate that fails on day one, then disabling it.

See `references/workflow-skeleton.md` for a minimal hardened workflow and a policy-file outline. Review of incoming workflow changes: `pr-review`. Dependency risk itself: `dependency-audit`.
