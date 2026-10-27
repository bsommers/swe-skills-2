---
name: security-best-practices
description: Use when writing, refactoring, or reviewing code that handles authentication, authorization, cryptography, user input, session tokens, database queries, external integrations, or sensitive data storage.
---

# Security Best Practices

## Overview

Security is a fundamental architectural constraint, not an afterthought or final audit checklist. Systems must be secure by default: enforce least privilege, complete mediation, fail-safe defaults, and defense in depth across every layer.

## Core Defense Pillars

1. **Authentication & Session Management:**
   - Use constant-time comparisons (`crypto.timingSafeEqual`, `hmac.compare_digest`) for secret hashes, signatures, and tokens.
   - Never accept JWTs with `alg: none`. Explicitly pin allowed signature algorithms.
   - Enforce `Secure`, `HttpOnly`, and `SameSite=Strict` (or `Lax`) on session cookies.
   - Implement cryptographically random session IDs with automatic expiration and revocation on logout.

2. **Explicit Authorization & Tenant Isolation:**
   - Verify identity and tenant ownership on every request. Never rely on client-supplied identifiers without server-side validation (prevent Insecure Direct Object References - IDOR).
   - Enforce multi-tenant boundaries at the database query layer (`WHERE tenant_id = :tenant_id AND id = :id`).
   - Distinguish role-based permissions (RBAC) from resource ownership (ABAC).

3. **Cryptographic Rigor & Secrets Management:**
   - Never invent or roll custom encryption algorithms. Use verified implementations of AEAD (AES-256-GCM or ChaCha20-Poly1305).
   - Derive keys and hash passwords using memory-hard functions (Argon2id, scrypt, or PBKDF2 with recommended iteration counts).
   - Zero hardcoded fallback secrets in source code (`os.getenv("SECRET", "dev_secret")` is forbidden). Load secrets from the environment or secret manager, and fail fast if missing.

4. **Input Validation & Structured Seams:**
   - Validate all untrusted input against strict schemas (allowlists) before execution.
   - Parameterize all database queries; never concatenate user strings into SQL or NoSQL queries.
   - Avoid shell execution. When invoking external executables, pass argument arrays directly rather than interpolating shell strings (`hardening-trust-boundaries`, `parsing-untrusted-text-robustly`).

5. **Information Exposure & Error Handling:**
   - Return generic, user-safe error messages to clients (`"Authentication failed"` rather than `"User not found"` or `"Incorrect password"`).
   - Never leak stack traces, database schema details, or environment paths in public HTTP responses.
   - Redact credentials, session tokens, and personal identifiable information (PII) before logging.

6. **Supply Chain & Dependencies:**
   - Pin all dependency versions with lockfiles.
   - Scan package trees for known CVEs and obsolete libraries before committing (`dependency-audit`).

## Common Mistakes

- Hardcoded secrets or permissive defaults in development environments leaking into production.
- Timing attack vulnerabilities caused by variable-time string equality operators (`token == expected`).
- Frontend-only authorization checks where underlying API endpoints remain unprotected.
- Unbounded API endpoints lacking rate limits, enabling brute-force and resource exhaustion attacks (`sizing-limits-from-measurement`).
- Disabling security middlewares (`@csrf_exempt`, disabling CORS) or silencing linter warnings to force tests to pass (`layered-verification-gates`).
