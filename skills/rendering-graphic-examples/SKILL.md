---
name: rendering-graphic-examples
description: Use when generating, rendering, or updating SVG and PNG visual diagrams, terminal captures, architecture schematics, or workflow illustrations to accompany code examples, recipes, and repository documentation.
---

# Rendering Graphic Examples

## Overview

Code recipes and architecture prose are faster to verify when paired with rendered visual examples. Generate deterministic **SVG** and **PNG** visuals from a repeatable script in `scripts/` so every major workflow recipe, CLI output example, and subsystem diagram has both a scalable vector asset and a raster fallback.

## Core Rules

1. **Deterministic generator script (`scripts/render-graphics.py` or `.sh`).**
   - Never hand-draw one-off binary images that cannot be updated when counts, flags, or module names change.
   - Keep a single generator script that emits `.svg` files into `docs/assets/` (and `docs/assets/examples/`) and rasterizes matching `.png` files.
2. **Dual-format output (`.svg` + `.png`).**
   - **SVG (`.svg`):** Primary format for Markdown, `README.md`, and web pages (`building-github-pages-sites`). Crisp at any DPI and diffable in git.
   - **PNG (`.png`):** Required alongside SVGs for OpenGraph social previews, PDF/LaTeX exports, and Markdown renderers that strip `<style>` or `<filter>` tags.
   - Rasterize SVGs deterministically via `inkscape --export-type=png --export-dpi=192`, `rsvg-convert`, `resvg`, or ImageMagick (`magick`).
3. **Self-contained, portable SVG structure.**
   - Always set explicit `xmlns="http://www.w3.org/2000/svg"`, `viewBox="0 0 W H"`, `width="100%"`, and `height="auto"` (or intrinsic pixel dimensions).
   - Use only system/web-safe font stacks (`ui-monospace, 'Cascadia Code', 'Fira Code', Menlo, Consolas, monospace` and `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`). Never link external Google Fonts or remote images inside SVGs—GitHub's `camo` proxy blocks external network requests inside `<img>` SVGs.
4. **Accompany concrete examples with visual walkthroughs.**
   - Pair key recipes in `docs/how-to.md`, `README.md`, and `docs/architecture.md` with a rendered diagram showing inputs, stage transitions, terminal telemetry, and verified outputs.
   - Keep visual styling cohesive across all generated graphics (see `showcasing-graphics-in-docs` and `designing-logos-and-icons`).
5. **Verify every rendered asset.**
   - Parse every `.svg` with `xml.etree.ElementTree` in tests to ensure well-formed XML.
   - Verify `.png` outputs are non-empty and match expected magic bytes (`\x89PNG\r\n\x1a\n`).
   - Re-run the generator whenever documented counts, commands, or capabilities change (`keeping-docs-in-sync`).

## Reference

- SVG/PNG rendering pipeline & converter fallbacks: `references/svg-png-pipeline.md`

## Common Mistakes

- **External font/asset URLs in SVG:** `<image href="https://...">` or `@import url(...)` fails silently inside GitHub `<img>` tags and offline viewers.
- **Clipped labels or overflow:** Text exceeding fixed box widths when rendered in fallback monospace fonts; size boxes with $\ge 20\%$ horizontal padding.
- **SVG-only without PNG:** Social cards (`og:image`) and strict sanitizers reject or break complex SVG filters without a `.png` counterpart.
- **Manual pixel edits:** Editing exported PNGs without updating the generator script guarantees the next run overwrites the fix.
