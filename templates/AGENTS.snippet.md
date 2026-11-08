## Engineering skills

This repo uses the swe-skills library. Start with the `using-swe-skills` skill (`/eng <task>`) to choose the 1–3 skills relevant to the task and to size the process (tool / app / system).

- **Discover local tools & VMs first (`using-local-tool-registry`):** Query `python3 scripts/tool-registry.py recommend --task "<task>"` to use local sandboxes (`cvm`), Windows/BSD VMs (`win-devvm`, `fedora-vms`, `freebsd-kvm`), and static analyzers (`flowscope`, `synth`).
- **Local CI first (`running-local-ci`):** Execute all builds, linters, and test suites locally (`scripts/verify.sh`, `~/src/gha-vm-runners/local-ci.sh`) before pushing. Conserve hosted GitHub Actions CI minutes as a standing rule unless explicitly overridden.
- **Verify before claiming:** Run the gate commands below and show their output.
- **Ask before outward actions:** Confirm before push, tag, publish, delete, or writes outside this repo.

### Gate commands
<!-- replace with this project's exact commands -->
```bash
# verify: ./scripts/verify.sh --quick
# test:   <command>
# lint:   <command>
# docs:   <command>
```
