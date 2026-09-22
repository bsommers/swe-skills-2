# Safe Refactoring Reference & Catalog of Code Transformations

A reference guide for applying Martin Fowler refactoring patterns with deterministic safety.

---

## 1. Core Refactoring Principles

1. **Rule of Two Hats**: You wear either the *Refactoring Hat* (changing structure without altering behavior) or the *Adding Functionality Hat* (changing behavior), never both at the same time.
2. **Small Steps with Fast Feedback**: Make the smallest verifiable change, compile, run tests, and commit.
3. **Preserve Public Contracts**: If changing a function signature used by external consumers, create an overload or wrapper first.

---

## 2. Refactoring Transformations Catalog

### Pattern 1: Parameter Object / DTO Introduction
- **Problem**: Function has 5+ parameters (`foo(a, b, c, d, e)`), leading to argument position bugs and fragile signatures.
- **Solution**: Bundle related parameters into a typed configuration object or DTO interface (`foo(options: FooOptions)`).

### Pattern 2: Replace Magic Primitives with Value Objects
- **Problem**: Passing strings for IDs, currencies, or email addresses (`orderId: string`, `price: number`).
- **Solution**: Create lightweight immutable Value Objects (`UserId`, `Money`, `EmailAddress`) with built-in validation.

### Pattern 3: Extract & Delegate (Decomposing Large Files)
- **Problem**: File has grown beyond 400+ lines mixing HTTP routing, business validation, database queries, and metrics.
- **Solution**: Extract data access to `*Repository`, validation to `*Validator`, and business rules to `*Service`.

### Pattern 4: Branch by Abstraction (Major Architectural Migrations)
- **Problem**: Swapping out a major subsystem (e.g. database client, auth provider, or payment gateway) without breaking production.
- **Solution**:
  1. Define an interface abstraction over the existing subsystem.
  2. Implement an adapter for the current subsystem.
  3. Implement a new adapter for the replacement subsystem.
  4. Use a feature toggle to route traffic gradually.
  5. Delete the legacy adapter once verified in production.
