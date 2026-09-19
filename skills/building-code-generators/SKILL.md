---
name: building-code-generators
description: Use when writing emitters, transpilers, scaffolders, or any tool that outputs code, config, schemas, diagrams or queries from a model, especially when generated output must compile, parse, or load in a downstream system.
---

# Building Code Generators

## Overview

Generated output is a contract with a downstream tool. **Prove it with the real downstream tool**, escape at the emit boundary, and make output deterministic. Emitters render an IR (see `designing-layered-pipelines`); they do not parse or validate.

## Rules

1. **Downstream smoke tests.** For each target run the real consumer: `ast.parse`/import for Python, `javac` for Java, `rustc`/`cargo check`, an XML parser for XML/RDF, the graph DB's dry-run for queries, the SMT solver for SMT-LIB. A string-match test proves nothing.
2. **Order for dependencies.** Topologically sort types with inheritance/references so parents precede children (otherwise `NameError` on subclassing).
3. **Escape per target, at the last moment.** String literals in Cypher/SQL, XML entities, shell words, Mermaid labels — each has its own rules. Sanitize identifiers too.
4. **Well-formed by construction.** Emit XML/RDF/JSON via a serializer or a validated template, not concatenation; use the standard namespaces.
5. **Match target idioms.** One public class per file in Java; type-safe numeric checks for int vs float; no unused imports (zero-warning builds apply to *generated* code too).
6. **Idempotent graph writes.** When emitting MERGE-style statements, MERGE parent nodes explicitly before relationships or you'll duplicate them; keep schema-level nodes separate from data instances.
7. **Deterministic.** Sorted keys and members, stable ids, no timestamps; then golden-file tests are meaningful.
8. **Templates live in files.** Archetype code goes in `templates/*.template` with parameter substitution — not multi-line heredocs inside scripts.
9. **Example corpus test.** Feed every real example through every emitter: zero lint errors and non-empty valid output.
10. **Property tests.** Round-trip and algebraic laws over 100+ random models.
11. **Clean exits.** Unknown target or invalid model → one-line diagnostic, nonzero exit.

## Test matrix

| Layer | Test |
|---|---|
| Parser/AST | unit + malformed-input negatives |
| IR build | property/round-trip |
| Each emitter | golden file + downstream tool check |
| CLI | subprocess: exit codes, files created |
| Examples | all examples × all emitters |

## Common mistakes

- Asserting on emitted text only.
- Escaping when parsing rather than when emitting.
- An emitter with its own copy of a validation rule.
- Hand-edited generated files (they get overwritten; see `engineering-for-determinism`).
