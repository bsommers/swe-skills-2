---
name: architecture-best-practices
description: Use when structuring a new system or component, defining subsystem boundaries, decoupling business logic from infrastructure, evaluating technical trade-offs, or refactoring tangled dependencies.
---

# Architecture Best Practices

## Overview

Effective architecture isolates what is volatile from what is stable. It keeps core business rules independent of delivery mechanisms, databases, and third-party frameworks, making systems verifiable, cost-effective to evolve, and resistant to technical rot.

## Core Architectural Principles

1. **Dependency Inversion & Clean Boundaries:**
   - High-level business policies must not depend on low-level implementation details.
   - Core domain logic must have zero dependencies on web frameworks, ORMs, databases, or third-party SDKs.
   - Define interfaces (ports) in the domain layer; implement external communication (adapters) in outer infrastructure layers (`designing-testable-seams`).

2. **Explicit Contracts & DTOs:**
   - Never leak internal domain entities or raw database models across subsystem or network boundaries.
   - Enforce explicit, versioned Data Transfer Objects (DTOs) with strict contract validation at all ingress and egress points (`planning-with-contracts`, `evolving-schemas-and-contracts`, `api-contract-audit`).

3. **Unidirectional, Acyclic Dependencies:**
   - Module dependency graphs must be strictly directed and acyclic (DAG).
   - Circular dependencies (`A -> B -> A`) indicate leaky abstraction boundaries and shared mutable state.
   - When two modules require mutual access, extract the shared abstraction into a separate leaf module or invert the dependency using events or interfaces.

4. **High Cohesion & Single Responsibility:**
   - Group code that changes together for the same business reason into cohesive modules.
   - Avoid monolithic God classes or sprawling service files that mix business calculation, persistence, and notification logic (`managing-complexity-budgets`, `code-architecture-review`).

5. **Discrete Pipeline Staging:**
   - Multi-stage processes (compilers, ETL workflows, data ingest) must flow through discrete, sequential stages where each stage transforms immutable data shapes (`designing-layered-pipelines`, `designing-data-pipelines`).
   - Prevent execution logic from leaking into thin wrapper modules.

6. **Resilience & Fault Isolation:**
   - Isolate external network boundaries using timeouts, circuit breakers, and retries with jittered exponential backoff (`sizing-limits-from-measurement`).
   - A degradation or failure in an external dependency must fail cleanly and locally without exhausting thread pools or cascading across downstream services.

7. **Document Invariants & Decision Records:**
   - When making architectural decisions that are costly to reverse, document evaluated alternatives, trade-offs, and invariants in an Architecture Decision Record (`defending-architecture-decisions`).

## Common Mistakes

- Framework entrenchment: tightly binding business logic to a specific ORM or web framework, making upgrades and testing difficult.
- Leaky abstractions: passing active database transactions, HTTP request contexts, or raw filesystem paths into domain entities.
- Premature distributed complexity: splitting into microservices before component boundaries and data access patterns stabilize in a modular monolith.
- In-place cyclic patching: hiding circular dependencies with inline local imports rather than repairing the broken layer hierarchy.
- Speculative abstraction: constructing complex plugin engines or generic abstractions before having two concrete, verified implementations (`designing-plugin-contracts`).
