# Cross-Pipeline Desync & Parity Audit Checklist

Use this reference alongside `hunting-cross-pipeline-desync` to structure a full audit pass and track findings to regression tests.

## 1. Consumer-Parity Matrix Template

Fill one row per shared domain concept. Any cell that reads a hardcoded constant, duplicates a formula, or ignores a user setting is a desync bug.

| Shared Concept | UI / Preview | Export / Print / Render | Wire / API / Hardware | Save / Load | Undo / Redo | Single Source? |
|---|---|---|---|---|---|---|
| Example: Margin / inset | `cfg.inset_mm` | hardcoded `10.0` (BUG) | `cfg.inset_mm` | saved | tracked | No |
| Example: Coordinate units | logical px | physical mm | device steps | mm | mm | Check transforms |
| Example: Permissions / role | hides button | — | skips check (BUG) | persisted | — | No |

### Red flags to grep for
- Magic numbers repeated across modules (`10.0`, `15.0`, `72.0`, `96.0`, `300`, `25.4`, `1000`).
- Separate `to_*` or `compute_*` helpers in UI vs. exporter vs. backend that implement the same math.
- Config struct fields that are written by UI controls and serialized, but only read in one of three downstream consumers.

## 2. State Lifecycle Transition Matrix

Verify every parallel mutable store is handled on every transition.

| Transition | Primary Model | Derived / Layout Cache | GPU / Media Cache | Selection / Cursor | Undo Stack | Open Handles / Timers |
|---|---|---|---|---|---|---|
| `open(A) → open(B)` | replaced | cleared? | evicted? | cleared? | reset? | closed? |
| `new` | fresh | cleared? | evicted? | cleared? | reset? | closed? |
| `close` | dropped | cleared? | evicted? | cleared? | cleared? | closed? |
| `mode / tab switch` | preserved | invalidated? | preserved/rebound? | scoped? | scoped? | paused/rebound? |
| `undo / redo` | mutated | invalidated? | re-synced? | clamped? | updated | — |
| `device / env change` | preserved | recomputed? | resized? | valid? | — | reconnected? |

Rule: route every document/session replacement through one `reset_ephemeral_state()` helper so adding a new cache only requires updating one place.

## 3. Output & Wire Metadata Probes

| Output / Format | Metadata to Verify in Emitted Bytes | Silent Failure if Missing |
|---|---|---|
| PNG | `pHYs` chunk (pixels/meter + unit=1) | OS print dialogs and editors assume 72/96 DPI and mis-scale physical output |
| JPEG | JFIF density (`Xdensity`/`Ydensity`, units) or EXIF resolution | Printed/imported at wrong physical size |
| PDF | `MediaBox`, `CropBox`, `UserUnit`, embedded fonts | Viewer/printer clips or rescales page |
| SVG | Physical `width`/`height` (`mm`/`in`) + matching `viewBox` | Imported at 72/96 px-per-inch mismatch |
| HTTP / API | `Content-Type`, charset, `Cache-Control`, `ETag`, `Content-Disposition` | Browser sniffs wrong type, caches stale data, or mangles filename |
| Hardware / Binary wire | Framing/EOF bytes, endianness, unit scale, coordinate bounds clamping | Device stalls, cuts/plots out of bounds, or misinterprets coordinates |

## 4. Reference-Program Parity Probes

When auditing compatibility with a reference application or standard workflow:

1. **Non-output guides:** Do registration grids, rulers, bounding handles, or hidden/locked layers stay strictly out of exports and wire commands?
2. **Domain execution order:** Are dependent operations ordered safely (e.g., inner holes before outer perimeters, parent objects before children, setup headers before payload)?
3. **Physical vs. logical coordinates:** Are canvas zoom/pan, device DPI, and physical media dimensions kept cleanly separated with explicit conversion functions?
4. **Keepout & safety zones:** Are hardware margins, unprintable edges, or reserved protocol ranges enforced consistently in preview warnings AND output validation?
5. **Power-user ergonomics:** Do standard keyboard shortcuts (`Cmd/Ctrl+Z`, `Shift`-constrain, `Alt`-duplicate, arrow nudging, `Delete`/`Backspace`, `Escape` to cancel) behave consistently across modes?
