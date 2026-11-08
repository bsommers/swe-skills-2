---
name: building-github-pages-sites
description: Use when creating, styling, or deploying an accompanying GitHub Pages showcase and documentation site for a repository, syncing it with README and docs/ content, or configuring GitHub Actions / docs/ publishing.
---

# Building GitHub Pages Sites

## Overview

An accompanying GitHub Pages site turns a repository's documentation, architecture diagrams, and interactive examples into a browsable web showcase. Build a fast, zero-dependency (or static-artifact) site in `docs/index.html` (with `docs/.nojekyll`) that stays synchronized with `README.md` and `docs/`.

## Core Rules

1. **Zero-friction publishing layout (`docs/index.html` + `docs/.nojekyll`).**
   - Place the landing page at `docs/index.html` and add an empty `docs/.nojekyll` file so GitHub Pages serves `docs/assets/`, `docs/diagrams/`, and underscored files directly without Jekyll preprocessing failures.
   - If a build step is used, add `.github/workflows/pages.yml` using `actions/upload-pages-artifact` and `actions/deploy-pages` pinned cleanly (`hardening-ci-workflows`).
2. **Cohesive visual design (`showcasing-graphics-in-docs` & `designing-logos-and-icons`).**
   - Default to a **futuristic obsidian-black background (`#050811`) with a light-blue neon cyber grid (`#00e5ff` / `#38bdf8`)** unless the user specifies another theme.
   - Include CSS grid background overlays, glowing HUD cards, high-contrast typography, responsive mobile/desktop breakpoints, and `prefers-reduced-motion` support.
3. **Required site sections:**
   - **Hero Header:** Brand logo (`assets/logo.svg`), concise value proposition, live version & capability counters, quick-install copy button, and direct links to the GitHub repo and User Manual.
   - **Visual Architecture & Graphic Examples Showcase:** Interactive gallery displaying the rendered SVG/PNG diagrams (`rendering-graphic-examples`) with zoom/preview and explanations.
   - **Interactive Capability / Skill Explorer:** Live search input and category filter pills so visitors can filter all skills, CLI commands, or `/eng` shortcuts instantly.
   - **Runnable Examples & Quickstart:** Copy-pasteable terminal recipes with one-click copy buttons.
   - **Documentation Hub Cards:** Direct links to `purpose.md`, `architecture.md`, `running.md`, `how-to.md`, `EVIDENCE.md`, `TESTING.md`, and `usermanual/`.
4. **Bidirectional linking & metadata.**
   - Link to the GitHub Pages site (`docs/index.html` / live Pages URL) from the root `README.md` and `docs/README.md`.
   - Include `<link rel="icon" type="image/svg+xml" href="assets/icon.svg">` and OpenGraph meta tags (`og:title`, `og:description`, `og:image` pointing to `assets/logo.png`).
5. **Single-source synchronization (`keeping-docs-in-sync`).**
   - Derive skill counts, version numbers, and catalog entries from the repository manifests and `skills/` directory, and verify in automated tests that `docs/index.html` has no broken relative asset links.

## Reference

- Complete HTML5/CSS/JS neon-grid GitHub Pages template and link-checker snippet: `references/github-pages-template.md`

## Common Mistakes

- **Missing `docs/.nojekyll`:** GitHub Pages runs Jekyll by default, which silently ignores directories or files starting with `_` and can break relative paths.
- **Broken relative asset paths:** Using `/docs/assets/logo.svg` instead of `assets/logo.svg` inside `docs/index.html` breaks when served from `https://<user>.github.io/<repo>/`.
- **Static wall of text:** Copying `README.md` verbatim without interactive search, category filters, or visual showcase cards.
