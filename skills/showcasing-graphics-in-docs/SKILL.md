---
name: showcasing-graphics-in-docs
description: Use when styling documentation visuals, embedding showcase graphics and rich visual examples into README or docs pages, or applying a cohesive visual theme such as a futuristic obsidian-black background with a light-blue neon grid (or a user-specified palette).
---

# Showcasing Graphics in Docs

## Overview

Documentation that pairs sharp visual telemetry with runnable examples communicates architecture and workflows in seconds. Apply a cohesive visual language across every diagram, example card, and documentation page—defaulting to a **futuristic obsidian-black background with a light-blue neon cyber grid** unless the user specifies a custom palette.

## Core Rules

1. **Theme selection (Default: Futuristic Black + Light-Blue Neon Grid, or User Override).**
   - If the user specifies a palette, brand colors, or light/dark theme, follow their exact specification.
   - Otherwise, default to the **Futuristic Neon Grid** aesthetic:
     - **Canvas Background:** Deep obsidian black (`#050811` to `#0a0f1d` radial/linear gradient).
     - **Neon Cyber Grid:** Orthogonal 32px/64px grid lines and perspective horizon accents in electric light blue (`#00e5ff` and `#38bdf8` at `0.08–0.18` stroke opacity) with subtle cyan intersection nodes.
     - **Primary Neon Accents:** Electric cyan (`#00e5ff`), sky neon (`#38bdf8`), plasma blue (`#0284c7`), with status highlights in neon emerald (`#00ff9d`), amber (`#ffb800`), and magenta (`#ff2a85`).
     - **Panel Surfaces:** Translucent dark slate (`#0b1326` at `0.90` opacity) with `1.5px` glowing cyan borders (`#00e5ff`) and corner HUD brackets.
     - **Typography:** High-contrast ice white (`#f0f6fc`) for headings, cool slate (`#94a3b8`) for secondary labels, and neon cyan (`#5eead4` / `#00e5ff`) for monospace commands and metrics.
2. **Showcase graphics at key entrypoints.**
   - **Root `README.md`:** Open with the hero banner (`docs/assets/logo.svg`), followed by a **Visual Architecture & Workflow Showcase** gallery embedding rendered graphic examples (`rendering-graphic-examples`) before dense reference tables.
   - **`docs/architecture.md` & `docs/purpose.md`:** Embed the system architecture and threat/governance visuals alongside Mermaid/ASCII models.
   - **`docs/how-to.md` & `docs/usermanual/`:** Pair major step-by-step recipes with rendered workflow cards showing command input, internal routing/isolation, and verified output.
3. **Every graphic must carry real engineering signal.**
   - Never embed decorative filler. Every card or node in a graphic must depict actual commands (`/eng ...`, `scripts/verify.sh`), real module paths, concrete thresholds (`70%`, `12 turns`, `8 tiers`), and genuine data flow.
4. **Accessible, portable Markdown embedding.**
   - Use relative paths (`docs/assets/examples/<name>.svg`) so graphics render identically in GitHub web views, local IDE previews, and GitHub Pages (`building-github-pages-sites`).
   - Always include descriptive `alt` text and a concise caption or surrounding prose explaining what the graphic demonstrates.

## Reference

- SVG pattern definitions, glow filters, HUD frames, and CSS variables for the futuristic neon grid theme: `references/futuristic-neon-grid-theme.md`

## Common Mistakes

- **Low-contrast dark-on-dark text:** Using dark gray text on a black canvas; body text must be $\ge 7:1$ contrast (`#e2e8f0` / `#f0f6fc`).
- **Overpowering background grid:** Grid opacity above `0.25` competes with foreground text; keep grid lines subtle (`0.08–0.16`) and panel fills opaque (`0.88–0.94`).
- **Orphaned assets:** Generating `.svg`/`.png` files in `docs/assets/` without embedding them in `README.md`, `docs/`, and the GitHub Pages showcase.
