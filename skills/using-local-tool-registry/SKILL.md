---
name: using-local-tool-registry
description: Use when starting or optimizing planning, build, execution, cross-platform testing, or release cycles to discover and leverage local tools, VM sandboxes (cvm, win-devvm, fedora-vms, freebsd-kvm), local CI runners (gha-vm-runners), and static analyzers in ~/src.
---

# Using the Local Tool Registry

## Overview

Before writing throwaway harness scripts, skipping cross-OS tests, or burning remote CI minutes, query the centralized **Local Tool Registry** (`scripts/tool-registry.py`). It indexes local engineering tools, virtual machine runners, sandboxes, local CI harnesses, and static analyzers across `~/src` so agent sessions can accelerate every lifecycle phase (`plan`, `build`, `execute`, `test`, `ci`, `release`).

## Core Rules

1. **Query the registry at the start of planning, testing, and release.**
   ```bash
   # Recommend tools for the current task & phase
   python3 scripts/tool-registry.py recommend --task "<task description>" --phase test

   # Search by keyword, category, or lifecycle phase
   python3 scripts/tool-registry.py search vm --phase test
   python3 scripts/tool-registry.py show cvm
   python3 scripts/tool-registry.py show win-devvm
   ```
2. **Match local VMs and tools to the engineering lifecycle:**
   - **Planning & Code Intelligence (`plan`):** Use `gitnexus`, `ontologic`, and `eval` to map dependency graphs and benchmark baselines before touching code.
   - **Isolated Execution, Sandboxing & Branching (`build`, `execute`):** Use **`cvm`** (`~/src/ai/projects/cvm`) to run untrusted code, risky migrations, or parallel multi-agent swarms inside isolated KVM/QEMU, Firecracker, Apple VZ, Seatbelt, Podman, or Docker sandboxes. Use `cvm snapshot`, `cvm branch`, and `cvm restore` for instant copy-on-write rollback.
   - **Cross-Platform Tri-OS & BSD Verification (`test`, `release`):**
     - **Windows 11 (`win-devvm`, `~/src/infra/win-devvm`):** Boot the unattended rootless KVM/libvirt (Linux) or Parallels ARM64 (macOS) Windows 11 guest (`./vm.sh start && ./vm.sh ssh`) pre-provisioned with MSVC Build Tools, rustup, Python, Node, and CMake to test Windows drivers (`designing-plugin-contracts`) and build Windows release binaries (`building-release-binaries`).
     - **Fedora & FreeBSD (`fedora-vms`, `freebsd-kvm`):** Boot `~/src/infra/fedora-vms/cr-fedora-latest.sh` or `~/src/vms/scripts/run-fbsd.sh` for RPM/SELinux/systemd and BSD `kqueue`/portability testing.
   - **Local CI & Security Gates (`ci`, `test`):** Run **`gha-vm-runners`** (`~/src/gha-vm-runners/local-ci.sh`) and **`flowscope`** / **`synth`** locally to validate full CI pipelines and SAST/SARIF gates without spending hosted GitHub Actions minutes (`running-local-ci`).
3. **Keep the registry fresh (`update`).**
   - When new repositories or tools are cloned or created under `~/src`, run:
     ```bash
     python3 scripts/tool-registry.py update
     ```
   - The updater merges curated tool definitions (`docs/tool-registry.seed.json`) with live `~/src` discovery into the user state index (`~/.local/share/swe-skills/tool-registry.json`).

## Reference

- Complete CLI usage, JSON schema, and VM orchestration recipes: `references/local-tools-and-vm-catalog.md`

## Common Mistakes

- **Skipping Windows/BSD tests on Linux/macOS:** Marking cross-OS tests as "can only test in GitHub CI" when `win-devvm`, `cvm`, and `freebsd-kvm` are available locally.
- **Running risky commands on the host:** Executing destructive system/process tests directly on the host instead of inside a `cvm` sandbox or snapshot branch.
- **Hardcoding machine-specific user paths:** Always reference registry tools via `~` or `$HOME` (`~/src/...`) in committed docs and scripts (`keeping-repos-portable`).
