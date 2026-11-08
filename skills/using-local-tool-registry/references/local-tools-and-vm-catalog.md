# Local Tool Registry & VM Catalog Reference

## 1. CLI Commands (`scripts/tool-registry.py`)

| Command | Purpose |
|---|---|
| `python3 scripts/tool-registry.py update` | Scans `~/src` (depth $\le 3$), merges curated entries, and writes `~/.local/share/swe-skills/tool-registry.json`. |
| `python3 scripts/tool-registry.py update --write-seed` | Also refreshes the portable repository seed catalog (`docs/tool-registry.seed.json`). |
| `python3 scripts/tool-registry.py recommend --task "..."` | Scores and recommends the best local tools/VMs for a free-text task and `--phase`. |
| `python3 scripts/tool-registry.py search <terms>` | Ranked search across tool names, tags, categories, lifecycle phases, and entrypoints. |
| `python3 scripts/tool-registry.py list --available-only` | Lists all tools verified present on the current machine. |
| `python3 scripts/tool-registry.py show <name>` | Prints full entrypoints, supported platforms, and tags for one tool. |

## 2. Primary VM & CI Tools by Lifecycle Phase

| Tool | Path | Category | Key Entrypoints & Lifecycle Role |
|---|---|---|---|
| **`cvm`** | `~/src/ai/projects/cvm` | `vm-sandbox` | `cvm run --backend kvm -- <cmd>`, `cvm snapshot`, `cvm branch`, `cvm restore`, `cvm mesh`, `cvm serve-mcp`. Isolated 13-backend VM/container sandboxes for unattended agents, risky builds, and multi-OS testing. |
| **`win-devvm`** | `~/src/infra/win-devvm` | `cross-platform-vm` | `./provision.sh`, `./vm.sh start`, `./vm.sh ssh`, `./vm.sh stop`. Unattended Windows 11 x64 (Linux KVM/libvirt) and ARM64 (macOS Parallels) dev VM with MSVC, rustup, Python, Node, CMake. |
| **`gha-vm-runners`** | `~/src/gha-vm-runners` | `local-ci` | `./local-ci.sh <repo>`, `./local-ci.sh --full <repo>`, `./gha-vm-runners.sh start|stop|status`. Mirrors `.github/workflows` locally or inside a disposable Ubuntu 24.04 KVM runner to conserve GitHub Actions minutes. |
| **`fedora-vms`** | `~/src/infra/fedora-vms` | `cross-platform-vm` | `./cr-fedora-latest.sh`. Fedora Linux KVM guest for RPM, systemd, and SELinux testing. |
| **`freebsd-kvm`** | `~/src/vms/scripts` | `cross-platform-vm` | `./run-fbsd.sh`, `./run-kvm-freebsd15.2.sh`. FreeBSD 15.x KVM guest for BSD portability and `kqueue` driver verification. |
| **`flowscope`** | `~/src/flowscope` | `static-analysis` | `flowscope scan . --format sarif -o report.sarif`. Fast local SAST and taint analysis gate. |
| **`synth`** | `~/src/synth` | `benchmark-eval` | `pytest -q`. Synthetic vulnerability corpus and gold SARIF evaluation harness. |
| **`eval`** | `~/src/eval` | `benchmark-eval` | `python3 -m unittest`. Statistical reproducibility, AST complexity, and benchmark auditing suite. |
| **`cli-anything`** | `~/src/utilities/CLI-Anything` | `cli-automation` | 50+ CLI harnesses for desktop/dev tools (Inkscape, Draw.io, Mermaid, GIMP, Blender, LLDB, WireMock). |
