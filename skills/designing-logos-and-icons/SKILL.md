---
name: designing-logos-and-icons
description: Use when designing, generating, or refreshing a project logo, hero banner, square plugin icon, favicon set, or domain category icons in SVG and PNG formats for a repository, CLI, plugin manifest, or documentation site.
---

# Designing Logos and Icons

## Overview

A sharp visual identity anchors a repository across GitHub, plugin marketplaces, documentation hubs, and GitHub Pages. Build a cohesive, programmatically generated SVG + PNG brand and icon kit so the hero banner, square plugin icon, and subsystem badges share identical geometry, palette, and crispness at every scale.

## Core Rules

1. **Generate the complete brand & icon kit (`rendering-graphic-examples`).**
   - **Wide Hero Banner (`docs/assets/logo.svg` + `docs/assets/logo.png`, ~`1200x360`):** Displays the core emblem, geometric wordmark or high-impact title, subtitle, and status telemetry on the project's signature canvas (default: futuristic obsidian-black with light-blue neon grid; see `showcasing-graphics-in-docs`).
   - **Square Plugin / App Icon (`assets/logo.svg` + `assets/logo.png` and `docs/assets/icon.svg`, `512x512`):** Centered emblem without tiny text so it remains unmistakable at `24px`, `64px`, and `512px`.
   - **Category / Subsystem Icons (`docs/assets/icons/icon-<name>.svg`, `64x64`):** Cohesive vector badges for each architectural layer or skill group.
2. **Wire the square icon into manifests and pages.**
   - Set `"logo": "assets/logo.svg"` in `plugin.json` (eliminates Antigravity `no logo` validation notices) and reference `docs/assets/icon.svg` as `<link rel="icon" type="image/svg+xml">` and `docs/assets/logo.png` as `og:image` in GitHub Pages (`building-github-pages-sites`).
3. **Geometric precision over generic clip-art.**
   - Construct emblems from exact mathematical primitives: concentric hexagonal/octagonal shields, circuit traces, isometric cubes, routing nodes, and precision reticles with layered neon glow (`#00e5ff`, `#38bdf8`, `#00ff9d`).
   - Render primary wordmarks using either custom geometric vector paths/pixel matrices or bold, wide-tracked monospace/display typography with layered neon stroke/glow so rendering never shifts across OSes.
4. **Multi-scale legibility gate.**
   - Test the square icon at `512x512` and `32x32`: stroke widths in a `64x64` viewBox must be $\ge 2\text{px}$ (or $\ge 12\text{px}$ in a `512x512` viewBox) so lines do not vanish when downscaled.
5. **Zero external dependencies inside SVGs.**
   - Never embed external `<image>` URLs or webfont `@import` directives inside logo or icon SVGs.

## Reference

- SVG geometry recipes for hexagonal cyber cores, isometric nodes, and category icons: `references/logo-and-icon-templates.md`

## Common Mistakes

- **Tiny text inside square icons:** Putting a 40-character tagline inside `assets/logo.svg` turns into illegible noise at plugin-icon size (`32x32`). Keep text in the wide hero banner only.
- **Forgetting `plugin.json` `"logo"`:** Leaving `plugin.json` without `"logo": "assets/logo.svg"` causes plugin validators (`agy plugin validate .`) to show a generic fallback icon.
- **Mismatched icon styles:** Mixing flat pastel icons with a futuristic neon hero banner; generate all icons from the same palette and stroke system.
