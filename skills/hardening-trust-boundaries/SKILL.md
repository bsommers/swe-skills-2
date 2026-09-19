---
name: hardening-trust-boundaries
description: Use when code passes data into a shell, SQL/Cypher/query language, filesystem path, template, container build, extension permission, or secret store; when running model-written or third-party code; or before shipping anything that handles untrusted input.
---

# Hardening Trust Boundaries

## Overview

Injection happens where data becomes code. At each boundary, **separate data from instructions structurally**, grant least privilege, and be honest about what a control does and doesn't stop.

## Rules by boundary

| Boundary | Do | Don't |
|---|---|---|
| Shell | pass an **argument array** (`subprocess.run([...])`, `callProcess`); validate/allowlist values | string-build a command; `shell=True`; pipe-to-shell (`curl … \| sh`) |
| SQL / Cypher / other query language | parameters (`$param`); escape literals and identifiers if you must generate text | concatenate user text; trust "sanitized" values from a prior step |
| Filesystem | resolve and check the path stays under an allowed root; reject `..` and absolute inputs | join user input into paths blindly |
| Secrets | read from env/secret store; use obvious placeholders in fixtures (`example.com`, `hunter2_placeholder`) | commit keys, real-shaped tokens, or registered domains |
| Container builds | allowlist base images; forbid fetch-and-exec `RUN` lines; review the Dockerfile as a committed file | build arbitrary third-party images |
| Executing model/third-party code | no network, drop all capabilities, `no-new-privileges`, pid/mem caps, host-enforced timeout | rely on the script's own restraint |
| Extensions / plugins | narrowest host permissions; no unneeded web-accessible resources | request "all URLs" for convenience |
| Telemetry | none by default; offline-capable core | phone home silently |
| Reflected content (exports, logs) | escape/sanitize for the output context | assume upstream content is safe |

## Honest labels

A base-image allowlist and a pipe-to-shell check are **speed bumps, not a sandbox**. Say so. Document what remains possible.

## Verify controls

- Add a **security test tier**: injection payloads against every generator/CLI, expecting refusal or safe escaping.
- Scan for pipe-to-shell, hardcoded absolute paths, and secret-shaped strings in pre-commit.
- **Negative twins must be truly safe.** A "sanitized" sample that still has a secondary flaw (command injection in the sanitizer, path traversal in an upload check) misleads every scanner tested against it.

## Order of operations

1. List trust boundaries in the design (`defending-architecture-decisions` Stability pass).
2. For each, pick the structural separation from the table.
3. Add one negative test per boundary.
4. Re-scan before release.

## Common mistakes

- Escaping in one layer and concatenating in the next.
- Allowlists that match by prefix and are bypassed by lookalikes.
- Treating "internal only" input as trusted.
- Security fixes without a regression test.
