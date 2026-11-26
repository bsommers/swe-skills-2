---
name: auditing-egress-and-telemetry
description: Use when reviewing a diff, dependency change, or unfamiliar code for hidden outbound network traffic, telemetry, analytics, crash reporting, update checks, host or environment fingerprinting, secret or PII collection, or install-time and build-time code execution.
---

# Auditing Egress and Telemetry

## Overview

Question: **what leaves this machine, to whom, carrying what, and who agreed?** Only the diff and the repo are evidence; PR text claiming "no telemetry" is a claim to test. Read, do not execute: no builds, install scripts or tests from untrusted code.

## Procedure

1. **Baseline:** list files in the diff; mark new/changed manifests, lockfiles, `build.rs`, `setup.py`, `postinstall`, workflows, Dockerfiles. These are the first targets.
2. **Sweep** with the recipes in `references/recipes.md` over added lines only (`git diff BASE...HEAD | grep '^+'`). Every hit becomes a candidate.
3. **Classify each candidate** by destination, payload, trigger, consent:

| Destination | Examples |
|---|---|
| Loopback | `127.0.0.1`, `::1`, unix socket; not egress, but audit auth in `auditing-privilege-and-writes` |
| User-configured | URL from user config or CLI arg, fetched on explicit command |
| Vendor-fixed | hardcoded host, analytics, crash, update-check, license ping |
| Opaque | host built from env/data/DNS names, encoded paths, redirects |

4. **Trace payload:** hostname, username, paths, env vars, versions, machine id, clipboard, file contents, tokens, command lines. Anything identifying the user or machine is PII.
5. **Trace trigger and consent:** startup, background timer, error handler, install hook, CI step; opt-in, opt-out or silent. Silent plus automatic is the high-risk shape.
6. **Dependencies:** new or bumped packages, typosquats (edit distance 1-2 from a popular name, new maintainer, tiny download count), git/URL dependencies, unpinned versions, lockfile hosts or hashes that changed without a matching manifest change. Hand off to `dependency-audit` for CVE and license depth.
7. **CI/build:** new workflow, `pull_request_target`, secrets exposure, `curl | sh`, unpinned actions (`hardening-ci-workflows`).
8. **Conclude with evidence:** "no egress found" must list the patterns searched and the files covered.

## Severity

| Level | Meaning |
|---|---|
| critical | silent send of secrets, credentials, file contents or identifiers; install/build-time code fetch-and-exec; typosquat or malicious dep |
| high | undisclosed vendor-fixed endpoint, fingerprinting, or beacon on by default; rendered untrusted or agent-written HTML/JS with no CSP `connect-src 'none'` |
| medium | opt-out telemetry or update check without docs; unpinned or new transitive hosts |
| low | documented, opt-in, user-configured fetch lacking timeout, TLS check or size cap |
| info | loopback-only listener, test fixtures, docs links |

## False positives

Docs, comments, test fixtures and `example.com` URLs; loopback servers; URLs the user typed or configured and fetched on request; schema/XML namespace URIs; package registries in lockfiles that match the existing host set. Verify by reading the call site before reporting.

## Common mistakes

- Stopping at "no new dependencies" while a hunk adds `std::net` or `fetch` by hand.
- Treating DNS lookups, WebSocket upgrades, image/CSS/font URLs and `<link>`/`<iframe>` sources as non-egress.
- Missing browser-side egress inside embedded HTML/JS strings.
- Reporting loopback listeners as exfiltration instead of auth findings.

## Output

Findings use category `egress` (or `supply-chain`), ID prefixes `EGR-`/`SUP-`, fields per `reviewing-code-security` (`references/findings.md`).
