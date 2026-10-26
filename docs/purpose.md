# Purpose, Motivation & Threat Model

## 1. Problem Statement

Autonomous and paired AI coding agents possess tremendous generative speed but suffer from well-documented systemic failure modes when tasked with real-world software engineering:

1. **Context Window Replay Dilution:** On every tool invocation, runtime harnesses resend the cumulative conversation history as input tokens. Unfiltered build progress, test stdout, and lingering skill definitions inflate prompt size, slowing responses and skyrocketing API costs.
2. **Rubber-Stamping & Silent Regressions:** Agents frequently report "all tests pass" from stale memory, suppress compiler errors with blanket ignore tags (`@ts-ignore`, `# noqa`), or delete failing assertions rather than fixing underlying faults.
3. **Lossy Context Compaction:** Compaction commands (`/compact`) or session resets without verified disk checkpoints destroy user corrections, architectural constraints, and working-tree state.
4. **Architectural Drift:** In multi-turn sessions, agents lose track of subsystem boundaries, creating circular dependencies, sprawling god-files, and leaky abstractions.

**swe-skills** provides a deterministic engineering immune system: a modular library of 52 battle-tested skills, lifecycle hooks, and verification gates that enforce disciplined software engineering practices directly within AI agent harnesses.

---

## 2. Core Tenets

- **Skills Guide Judgment, Not Workflow:** General workflow skills (brainstorming, TDD, code review) dictate *how* to work; `swe-skills` provide the domain-specific *judgment* (e.g., how to design testable seams, size timeouts from measurement, or guard trust boundaries).
- **Bounded Active Context:** Never inject 50+ skills simultaneously. Load at most 1–3 skills tailored to the current phase, and evict stale skills when transitioning phases.
- **Evidence Before Assertion:** An agent must never claim code works without citing the exact executed command and verifiable terminal output (`pytest -q`, `cargo test -q`).
- **Standardized Token Economics:** Track token spend against commercial rate cards in Million Tokens (MTok) and USD ($), treating turn frequency $\times$ context depth as the dominant cost driver.

---

## 3. Threat Model & Security Posture

AI agents operate with shell execution and filesystem modification privileges. `swe-skills` defines strict boundaries to neutralize potential exploits and regressions:

```
+-------------------------------------------------------------------------+
|                        UNTRUSTED EXTERNAL INPUTS                        |
|   Web content · Scraped text · Model-generated code · Third-party deps   |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                      TRUST BOUNDARY HARDENING                           |
|   (hardening-trust-boundaries · parsing-untrusted-text-robustly)        |
|                                                                         |
|   • Shell Injections: Enforce argument arrays over raw shell strings    |
|   • Path Traversals: Validate and canonicalize paths; no sibling repo   |
|     writes without explicit human approval                              |
|   • Malicious Deps: Static audit for known CVEs (dependency-audit)      |
|   • Secret Leakage: Scan working-tree for unmasked keys & API tokens    |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                   SAFE REPOSITORY & WORKING TREE                        |
+-------------------------------------------------------------------------+
```

### Threat Mitigations

| Threat Vector | Risk Description | Mitigation Mechanism |
|---|---|---|
| **Arbitrary Command Injection** | Untrusted filenames or parameters interpolated into shell execution strings. | [`hardening-trust-boundaries`](../skills/hardening-trust-boundaries/SKILL.md) mandates parameter arrays, subprocess separation, and forbidden shell string concatenation. |
| **Silent Security Downgrades** | Agents weakening auth checks, removing CORS rules, or adding wildcard permissions to make tests pass. | [`layered-verification-gates`](../skills/layered-verification-gates/SKILL.md) and [`git_pre_commit.py`](../scripts/hooks/git_pre_commit.py) prohibit lowering thresholds or disabling security checks. |
| **Supply Chain Poisoning** | Incorporating unvetted third-party packages with malicious postinstall scripts or critical CVEs. | [`dependency-audit`](../skills/dependency-audit/SKILL.md) enforces vulnerability scans across JS/TS, Python, Rust, and Go before merging. |
| **Context Memory Injection** | Untrusted text or prompt injection embedded in external data poisoning agent instructions. | [`parsing-untrusted-text-robustly`](../skills/parsing-untrusted-text-robustly/SKILL.md) and [`grounding-ai-outputs`](../skills/grounding-ai-outputs/SKILL.md) isolate untrusted inputs into inert data containers. |
| **Credential & Secret Leaks** | Agents committing `.env` files, API tokens, or absolute developer paths into git history. | Pre-commit hook (`git_pre_commit.py`) scans staged changes for unmasked secrets and absolute home directory paths, blocking commits on violation. |

---

## 4. Empirical Provenance

Every rule, checklist, and mistake listed in `swe-skills` is derived from concrete incidents across ~20 active repositories:
- Compilers, transpilers, and AST analyzers
- Multi-tier ETL pipelines and knowledge graphs
- Autonomous agent frameworks and sandboxed daemons
- High-concurrency browser extensions and UI component suites

See [docs/EVIDENCE.md](EVIDENCE.md) for full incident provenance and commit hashes.
