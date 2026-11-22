---
name: auditing-privilege-and-writes
description: Use when reviewing a diff or unfamiliar code for writes outside the project or runtime directory, shell-rc or ssh or cron or service edits, permissions and temp files, path traversal and symlinks, process spawning, unsafe or FFI code, local servers and tokens, deserialization, terminal-escape injection, or secrets in logs and argv.
---

# Auditing Privilege and Writes

## Overview

Question: **what can this code change or reach beyond its stated job, and can an attacker steer it?** Static review only; never run untrusted code. Prefer a concrete exploit sketch ("a local user can read the token from `ps`") over a vague "may be unsafe".

## Checklist (add each hit from `references/recipes.md` as a candidate)

1. **Write targets:** every file/dir created, written, renamed, deleted. Must stay inside the project or the app's runtime dir via one safe helper (0700 dirs, 0600 atomic files). Flag `$HOME` dotfiles, shell rc, `~/.ssh`, `authorized_keys`, crontab, launchd/systemd units, autostart, git hooks, `/etc`, `/tmp` fixed names.
2. **Paths:** user or network input joined into paths without canonicalize-and-prefix check; `..`, absolute paths, symlink following (`O_NOFOLLOW`, `lstat`), zip/tar extraction, TOCTOU between check and use.
3. **Permissions:** umask, `chmod 777/666`, world-readable secrets, default file modes, Windows ACLs.
4. **Temp files:** predictable names, no `O_EXCL`, shared `/tmp`, not cleaned.
5. **Process spawning:** shell strings, `shell=True`, unvalidated argv, PATH lookup of bare names, secrets passed in argv or env visible in `ps`, URLs opened via `xdg-open`; see `hardening-trust-boundaries`.
6. **Unsafe/FFI:** each `unsafe`/`ctypes`/cgo block has a justified invariant (`// SAFETY:`), correct signatures, no raw pointer from untrusted lengths.
7. **Local servers/IPC:** bind address (loopback only), auth on every route, token entropy and constant-time compare, Host/Origin checks (DNS rebinding, CSRF), socket file mode, per-connection timeouts, request limits (`bounding-untrusted-resource-use`). Hand-rolled HTTP parsers: one request per connection, reject `Transfer-Encoding` and duplicate `Content-Length`, cap head and body; note a sound parser as a positive.
8. **Tokens and CSPRNG:** OS randomness only (`getrandom`, `/dev/urandom`, `secrets`, `crypto.randomBytes`), >= 128 bits, no `rand()`/time seeds, duplicated generators merged into one helper.
9. **Token leakage:** tokens in URLs, logs, error text, RPC replies, argv, browser history, transcripts; redact by default.
10. **Deserialization:** `pickle`, `yaml.load`, `eval`, Java/Ruby native formats, unbounded JSON into privileged structs.
11. **Terminal/escape injection:** untrusted text reaching a terminal, log viewer or title without stripping control sequences (`hardening-trust-boundaries`, `parsing-untrusted-text-robustly`); also terminal graphics/escape output enabled by guessing capability from env vars (category `compat`).
12. **Sandbox/capabilities:** `sandbox` flags, CSP, iframe `allow-*`, container `--privileged`, mounted sockets, broad extension or OAuth scopes, list/read APIs (RPC, MCP resources) exposing every key of a shared store instead of the intended prefix. Rendering untrusted HTML needs CSP with `connect-src 'none'`.
13. **Concurrent writers:** overwrite without revision/ETag check silently clobbers other writers.

## Severity

| Level | Meaning |
|---|---|
| critical | arbitrary write/exec from untrusted input; persistence via rc/cron/ssh/service edits; auth bypass on a local service |
| high | token or secret leaked to logs/argv/URLs/other users; weak RNG for secrets; traversal or symlink write; shared-machine local-user access |
| medium | missing CSP/sandbox hardening, DoS from blocking server loop, unchecked concurrent overwrite, unjustified `unsafe` |
| low | loose modes on non-secret files, minor missing validation, ignored persist errors |
| info | hardening suggestions |

## False positives

Writes inside the declared runtime dir through the approved helper; `/tmp` use via `mkstemp`/`tempfile`; loopback servers with random tokens and Host/Origin checks; `unsafe` that is documented and minimal; test-only code under `#[cfg(test)]`/`tests/`. Confirm by reading the call site and the helper before reporting.

## Common mistakes

- Reviewing the new helper but not the call sites that bypass it.
- Calling a loopback server safe on a shared machine: any local user can reach it, so the token is the only barrier.
- Reporting every `unsafe` instead of asking what invariant holds.
- Forgetting build/test scripts and docs examples that write to `$HOME`.

## Output

Categories `privilege`, `trust-boundary`, `resource-bounds`, `parsing`; IDs `PRV-`, `TRU-`, `RES-`, `PAR-`; fields per `reviewing-code-security` (`references/findings.md`).
