# Local CI Mirroring & VM Runner Reference

## 1. Local CI Execution Hierarchy

Run checks from fastest/cheapest to heaviest, all on the local host before any `git push`:

| Stage | Tool / Command | Cost & Speed |
|---|---|---|
| **1. Fast Local Gate** | `scripts/verify.sh --quick` (or linter + unit + smoke tests) | 0 CI min · < 15s |
| **2. Full Local Workflow Mirror** | `~/src/gha-vm-runners/local-ci.sh <repo>` (or `scripts/verify.sh`) | 0 CI min · 10s–2m |
| **3. Local Sandbox / Clean-Room** | `~/src/ai/projects/cvm/bin/cvm run --backend kvm -- ./scripts/verify.sh` | 0 CI min · 5s–1m |
| **4. Cross-OS Local VMs** | `win-devvm` (`./vm.sh ssh`), `fedora-vms`, `freebsd-kvm` | 0 CI min · 30s–3m |
| **5. Self-Hosted KVM GHA Runner** | `~/src/gha-vm-runners/gha-vm-runners.sh start` | 0 hosted CI min |
| **6. Hosted GitHub Actions** | Final milestone/release push or explicit user override only | Consumes quota |

## 2. Quota-Conserving GitHub Actions Header Template

```yaml
name: CI

on:
  workflow_dispatch:
  push:
    branches: [main]
    tags: ["v*"]
    paths-ignore:
      - "**.md"
      - "docs/**"
  pull_request:
    branches: [main]
    paths-ignore:
      - "**.md"
      - "docs/**"

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - name: Run local-equivalent verification gate
        run: ./scripts/verify.sh --quick
```

## 3. Adding a Repo to `local-ci.sh`

When creating or updating `.github/workflows/ci.yml`:
1. Keep every workflow `run:` step calling a script in `scripts/` (e.g., `scripts/verify.sh`) rather than embedding 50 lines of inline YAML bash.
2. That way, running `./scripts/verify.sh` or `~/src/gha-vm-runners/local-ci.sh <repo>` on your workstation executes the exact same commands as CI with zero drift.
