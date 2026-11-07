---
name: bounding-untrusted-resource-use
description: Use when code allocates memory, buffers, or retained history based on sizes or counts that arrive in untrusted input (image or file headers, protocol lengths, escape sequences, notifications, events, links), or when a list that grows from external input has no cap.
---

# Bounding Untrusted Resource Use

## Overview

Attackers don't need an exploit when your parser trusts a number. A 12-byte header declaring a huge width and height can demand gigabytes before a single pixel is decoded. Every size, count, and retained collection fed by untrusted input needs an explicit bound.

## Rules

1. **Never allocate from declared dimensions or lengths.** Cap each dimension separately, compute the product with checked arithmetic, and reject before decoding or allocating.
2. **Cap the encoded payload too**, not just the decoded size. Both ends of the pipeline need limits.
3. **Every retained list needs a cap with drop-oldest** when untrusted input feeds it: links, notifications, placements, events, history.
4. **Audit consumers of a capped list.** Code that used `len()` as a "new items since last time" cursor breaks silently once the cap is reached (length stops growing). Replace with a monotonic received-counter.
5. **One shared constant** across sibling decoders. Duplicated magic numbers diverge.
6. **Choose the number from measurement** and a stated worst case (`sizing-limits-from-measurement`), not a guess.

## Tests (always three)

- Oversized input is rejected (and nothing large was allocated).
- Exactly-max input is accepted (off-by-one check).
- Cap behavior: after exceeding it, the newest entries are retained, the oldest dropped, and cursor consumers still see new items.

## Common mistakes

- Checking `w * h` after multiplying in a type that already overflowed.
- Capping the decoded image but allowing an unbounded compressed stream.
- Bounding the list but leaving a per-entry field (URL, title, body) unbounded.
- Cap added, cursor logic never revisited.
- Rejecting oversized input with a panic instead of a clean error.

Related: `hardening-trust-boundaries` (other boundaries), `parsing-untrusted-text-robustly`, `hunting-silent-failures` (cursor breakage is a silent failure).
