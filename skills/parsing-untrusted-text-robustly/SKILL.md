---
name: parsing-untrusted-text-robustly
description: Use when parsing or scraping text, HTML/DOM, markdown, logs, or markup you do not control; when a scraper breaks after a site update; when a parser matches things inside code blocks; or when type-guessing gives wrong results.
---

# Parsing Untrusted Text Robustly

## Overview

Third-party formats change and users paste hostile edge cases. Parse structurally where you can, mask what must not match, escape on output, and test with adversarial fixtures.

## Rules

1. **Selector cascade for scraping.** Try primary selectors, then fallbacks, then a generic last resort. Document the DOM assumptions and the date they were last verified in the code and docs. Fail with a clear message naming which stage matched.
2. **Scope before scanning.** Limit to the container you care about (`chat-history`, not `body`), or you'll capture navigation and ads.
3. **Mask, don't skip.** To find markers in markdown while ignoring examples, mask fenced blocks (```` ``` ````, `~~~`) and inline code spans with same-length spaces so offsets stay valid. Bind to the *last* matching END marker, not the first.
4. **Don't let permissive parsers decide types.** `Date.parse("2020")` succeeds; test "is it a plain number?" first, then dates. Objects like `Date` have no enumerable entries — special-case them or they silently vanish.
5. **Escape at the emit boundary.** Table pipes in markdown cells, Mermaid edge labels, HTML entities, CSV quotes. A label with `(` or `:` can break a whole diagram.
6. **Convert nested structures correctly.** Nested lists and tables are where duplication bugs live; test depth ≥ 3.
7. **Bound concurrency and size** for fetches and images; scope titles/ids so retries don't collide.
8. **Idempotent injection.** Guard content scripts with a `window.__loaded` flag so re-injection doesn't double-register listeners.
9. **Least privilege for extensions.** Narrow host permissions; don't expose bundled libs as web-accessible resources; no telemetry; state permissions and why in a SECURITY note.
10. **Exported HTML reflects untrusted DOM.** Sanitize, or document the risk and forbid opening exports from untrusted sources.

## Test fixtures to always include

Empty input · huge input · nested depth 3+ · unicode/RTL/emoji · a marker inside a code fence · a marker inside inline code · unclosed fence · duplicate markers · pipes/backticks/brackets in cell text · year-like strings (`"2020"`) · null/undefined.

## Common mistakes

- Regex over HTML.
- Fixing a break by adding one more selector without a fallback order or a test fixture.
- Testing only on your own captured page.
- Treating "empty result" as success (see `hunting-silent-failures`).
