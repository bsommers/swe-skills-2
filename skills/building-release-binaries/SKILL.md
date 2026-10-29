---
name: building-release-binaries
description: Use when building, packaging, or uploading per-platform release binaries (macOS, Linux, Windows) for a tagged version, when a GitHub release is missing assets for some platform, or when cross-compiling a Rust CLI for distribution.
---

# Building Release Binaries Per Platform

Turn an existing tag into downloadable, checksummed archives for each platform, built from exactly what the tag points to. This picks up where the `release` skill stops: `release` decides the version and pushes the tag, and this skill ships the binaries for that tag.

## Core rules

1. **Build the tag, not the working tree.** Check the tag out into a temporary `git worktree` and build there. That keeps uncommitted edits and untracked files out of the release, and a version mismatch can't happen.
2. **Build each platform on the host that can link it.** macOS targets need the macOS SDK, so build `*-apple-darwin` on a Mac. Native GUI frameworks (AppKit, CoreText, QuartzCore) will not link through zig or cross. Windows MSVC needs Windows. Linux gnu and musl can be built on Linux, and `cargo zigbuild` handles musl and glibc floors (`x86_64-unknown-linux-gnu.2.28`).
3. **Use the same names on every host.** Name each archive `<bin>-<tag>-<triple>.tar.gz` (`.zip` on Windows), with an unversioned alias `<bin>-<triple>.*` that "latest" installers download. Inside each archive, put one directory holding the binary plus README, LICENSE and CHANGELOG.
4. **Merge checksums, never overwrite them.** Several hosts upload to the same release one after another. Download the current `SHA256SUMS`, replace only the lines for your own files, and upload the merged file again.
5. **Ask before uploading.** Building is local and safe. `gh release create` and `gh release upload` publish to users, so confirm with the user before running them unless they already said to upload.

## Workflow

```bash
# 0. Confirm the tag exists locally and on the remote, and see which assets the release already has
git fetch --tags && git ls-remote --tags origin | grep "$TAG"
gh release view "$TAG" --json assets -q '.assets[].name'   # error => release not created yet

# 1. Build for this host's native targets (no upload)
scripts/build-binaries.sh "$TAG"                 # or --targets "aarch64-apple-darwin"

# 2. Verify (see below), then publish after the user confirms
scripts/build-binaries.sh "$TAG" --upload        # add --create-release if step 0 errored
```

Run step 1 on every host the platform matrix needs, for example a Mac for darwin, a Linux box for gnu and musl, and Windows for msvc. Each run adds its own files to the release.

If the project already has release scripts (check `scripts/`, `Makefile`, `justfile`, `.github/workflows/release*`, `dist-workspace.toml` for cargo-dist, and `.goreleaser.yaml`), use them and apply the rules above when reviewing them. Install the bundled script only when the project has none.

## Verify before upload

For every archive, unpack it into a temporary directory and check all of these:

| Check | macOS | Linux | Windows |
| :--- | :--- | :--- | :--- |
| Right architecture | `file bin` → `arm64` / `x86_64` | `file bin` | `file bin.exe` → `PE32+` |
| It runs | `./bin --version` (x86_64 runs under Rosetta) | same | same |
| Version matches tag | output contains `${TAG#v}` | same | same |
| Dynamic deps | `otool -L` shows only `/usr/lib` + `/System/Library` | `ldd`: musl is `statically linked` | `dumpbin /dependents` |
| Minimum OS | `otool -l bin \| grep -A3 LC_BUILD_VERSION` → `minos` | glibc floor: `objdump -T bin \| grep GLIBC_ \| sort -V \| tail -1` | — |

Report in the summary which checks you ran and on which host, and name any you skipped. For example, an x86_64 binary that only ran under Rosetta counts as tested on an Intel Mac only if you say so.

## Platform notes

- **macOS signing.** `cargo build` produces an ad-hoc signature (`codesign -dv` shows `Signature=adhoc`). Gatekeeper quarantines downloaded binaries, so users have to run `xattr -d com.apple.quarantine bin` or install through a script that uses `curl` (curl does not set the quarantine bit). Notarizing needs a Developer ID certificate and `xcrun notarytool`. Only offer it; don't do it unprompted.
- **Universal binary (optional).** `lipo -create -output bin <aarch64>/bin <x86_64>/bin`. Ship it as an extra `*-universal-apple-darwin` archive and keep the per-arch archives that installers expect.
- **`--locked`.** The script builds with `--locked`. If `Cargo.lock` is not committed, fix that in the repo before releasing. Don't remove the flag.
- **Windows gnu and msvc.** `x86_64-pc-windows-gnu` cross-builds from Linux with zigbuild. `msvc` builds natively on Windows (Git Bash or MSYS2). If installers ask for one of them by name, upload that one.

## Bundled script

`scripts/build-binaries.sh`: generic for Rust and tested on macOS. It reads the binary name and version from `Cargo.toml`, picks the host's native targets, builds in a worktree with a shared `CARGO_TARGET_DIR` (so rebuilds stay incremental), packages the archives, writes `SHA256SUMS`, and with `--upload` merges and uploads. Copy it into the project's `scripts/` directory, or run it from the skill directory, from inside the repo.

For a project in another language, keep the worktree, naming, checksum-merge and verification steps, and replace only the build line, for example `GOOS=… GOARCH=… go build`, `zig build -Dtarget=…`, or `pyinstaller`.

## Red flags

- An archive built from `HEAD` or the working tree instead of the tag.
- `SHA256SUMS` on the release lists only the last host's files.
- A darwin archive cross-built on Linux whose GUI paths fail at runtime.
- Assets uploaded before `--version` was run on the unpacked binary.
- A release marked Latest with no assets for a platform that the installer's default path downloads.
