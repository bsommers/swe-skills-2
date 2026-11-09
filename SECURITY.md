# Security Policy

## Supported versions

Only the latest release on `main` receives fixes. Pin a tag if you need a stable version.

## What is in scope

swe-skills is mostly Markdown, but parts of it execute or steer execution:

- **Scripts and hooks** — `scripts/install.sh`, `scripts/hooks/*` (hooks run on agent session events), and any `skills/*/scripts/*`.
- **Skill text that could make an agent act unsafely** — for example, instructions that would lead an agent to run untrusted code, exfiltrate data, weaken a security control, or install an unpinned dependency without asking.
- **CI workflows** in `.github/workflows/`.

Out of scope: vulnerabilities in the agent tools themselves (Claude Code, Antigravity, Cursor) — report those to their vendors.

## Reporting a vulnerability

Please **do not open a public issue**. Use GitHub's private reporting instead:
**Security tab → Report a vulnerability** on this repository.

Include the affected file(s), what an attacker or a misled agent could do, and steps to reproduce. You should get an acknowledgement within 7 days. Fixes are released as a patch version and credited in `CHANGELOG.md` unless you ask otherwise.
