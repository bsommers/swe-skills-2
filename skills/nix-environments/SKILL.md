---
name: nix-environments
description: Use when configuring reproducible development environments, hermetic build toolchains, or system-level dependencies with Nix flakes or devShells, especially when a project requires native C libraries or cross-compiler tools alongside language package managers.
---

# Nix Environments

Nix provides hermetic, bit-for-bit reproducible developer environments across Linux and macOS. In agent-assisted workflows, **Nix is strictly optional**: it enhances determinism when available, but must never become a hard barrier that breaks non-Nix hosts, minimal CI runners, or containerized agents.

Combine Nix for system substrates with language-native package managers (`uv`, `cargo`, `npm`) for dependencies.

## The Three-Tier Execution Hierarchy

Every project supporting Nix must remain runnable through three tiers:

1. **Tier 1 — Hermetic Nix (`nix develop` or `direnv`):**
   Active when `nix` is present. Provides pinned system libraries (compilers, headers, C libraries, OpenSSL, SQLite).
2. **Tier 2 — Standard Toolchain (Host Native):**
   Direct execution (`uv run pytest`, `cargo test`, `npm test`) using host-installed tools when Nix is absent.
3. **Tier 3 — Containerized CI / Minimal Runner:**
   Standard Dockerfile or GitHub Actions runner without mandatory Nix daemon requirements.

Pair with `keeping-repos-portable` and `engineering-for-determinism`.

## Core Rules

1. **Progressive Enhancement, Never Mandatory:**
   Never assume `nix` exists in PATH. Shell scripts and test commands must run directly on the host or inside a standard container without requiring `nix develop`.
2. **Split System Substrate from Language Packages:**
   Use Nix to provide the system tools (Python interpreter, Rust toolchain, `pkg-config`, C compilers, shared libraries). Delegate language packages to language lockfiles (`uv.lock`, `Cargo.lock`, `package-lock.json`).
   - Do not package ephemeral Python wheels or npm dependencies into Nix expressions unless building an immutable production artifact.
3. **No Leaked Store Paths:**
   Never commit or hardcode `/nix/store/...` paths into project configs, scripts, or documentation.
4. **Provide Self-Contained Flakes:**
   Keep `flake.nix` at repo root with pinned `nixpkgs` input. Provide a single default dev shell (`devShells.default`).
5. **Deterministic Shell Hooks:**
   In `shellHook`, set up local directory state cleanly (e.g. `export UV_PROJECT_ENVIRONMENT=.venv`). Never mutate system paths or prompt strings aggressively.

## Standard Setup Recipe

When adding Nix support to a project:

1. **Copy template:** Place `templates/nix/flake.nix` at the project root.
2. **Declare system packages:** Add native packages to `buildInputs` or `packages` (`stdenv.cc`, `pkg-config`, `openssl`).
3. **Verify dual-mode operation:**
   - In Nix: Run `nix develop --command <test-cmd>`.
   - Outside Nix: Run `<test-cmd>` directly on host. Both must pass.
4. **Document optional use:** In `README.md` or `CLAUDE.md`, list Nix under "Optional Hermetic Setup", not as a mandatory prerequisite.

## Mistakes to Avoid

- **Hard-failing when `nix` is missing:** Scripts that begin with `nix develop` without fallback break CI and agent sandboxes.
- **Double-locking language packages:** Packaging every pip package in Nix creates slow derivations and breaks `uv add` iteration.
- **Ignoring non-x86_64 architectures:** Use `flake-utils` or iterate over `["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"]`.
- **Forgetting `pkg-config`:** Native C extensions fail to compile if `pkg-config` and library headers are omitted from `devShell`.
