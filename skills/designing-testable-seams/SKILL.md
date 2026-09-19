---
name: designing-testable-seams
description: Use when writing code that talks to databases, HTTP, the clock, containers, LLMs, or the filesystem; when tests need live services; or when error handling swallows failures with broad excepts.
---

# Designing Testable Seams

## Overview

Every external dependency enters through a **constructor or parameter with a config-driven default**. Then the whole system tests with fakes and no live services, and failure handling becomes explicit and typed.

## Rules

1. **Inject, don't import-and-call.** `Orchestrator(llm=..., store=..., sandbox=..., clock=...)`. Defaults come from settings; tests pass fakes. Module-level singletons only for immutable settings.
2. **Fakes over mocks.** A small in-memory fake with the real interface beats a mock that records calls; assert on outcomes.
3. **Unit suite runs with nothing running.** No Docker, DB, or network. Integration tests that need services are marked and skip *loudly* (see `layered-verification-gates`).
4. **Typed exception hierarchy** rooted at one base. Chain with `raise X from exc`. No bare `except:`. Catch the narrowest type (validation errors, not `Exception`).
5. **Classify outcomes distinctly.** "Retries exhausted", "stopped making progress", and "infrastructure error" are different terminal states with different remedies.
6. **Best-effort side paths.** Scoring, telemetry, lesson distillation, notifications: wrap, log, and continue. They must never take down the main path. Return `None`/skip, don't raise.
7. **Cheap retries only at flaky edges** with capped exponential backoff; a persistent failure must still surface as the caller's typed error.
8. **No hidden globals for time and randomness.** Inject the clock and seed the RNG so tests are deterministic.

## Example

```python
class Orchestrator:
    def __init__(self, llm=None, store=None, sandbox=None, settings=settings):
        self.llm = llm or LLMClient(settings.llm_base_url, settings.llm_timeout)
        self.store = store or MemoryStore(settings.qdrant_url)
        self.sandbox = sandbox or SandboxExecutor(settings)

    def distill_lesson(self, record):
        try:
            record.lesson = self.llm.summarize(record)      # best-effort
        except AgentFrameworkError as exc:
            log.warning("lesson distillation failed: %s", exc)  # never fatal
```

## Common mistakes

- `except Exception: pass` around the thing that matters.
- Tests that pass only when a local service happens to be up.
- A fake that is more forgiving than the real dependency (hides real failure modes).
- Retrying non-idempotent operations.
- Broad catches that convert a bug into a "handled" error and a wrong answer.
