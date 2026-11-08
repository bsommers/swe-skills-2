#!/usr/bin/env python3
"""Deterministic GitHub Pages site generator (docs/index.html + docs/.nojekyll) for swe-skills.

Reads live skill metadata from skills/*/SKILL.md, shortcuts from skills/eng/SKILL.md,
and version from plugin.json to build a zero-dependency, interactive GitHub Pages
showcase styled with a futuristic obsidian-black background and light-blue neon cyber grid.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SKILLS_DIR = ROOT / "skills"

CATEGORY_MAP: dict[str, str] = {
    "using-swe-skills": "entry",
    "eng": "entry",
    "right-sizing-process": "plan",
    "writing-intent-briefs": "plan",
    "planning-with-contracts": "plan",
    "designing-exhaustive-test-cases": "plan",
    "sizing-limits-from-measurement": "plan",
    "token-finops": "plan",
    "choosing-tools-and-substrates": "plan",
    "using-local-tool-registry": "plan",
    "adaptive-model-routing": "plan",
    "architecture-best-practices": "arch",
    "designing-layered-pipelines": "arch",
    "designing-plugin-contracts": "arch",
    "designing-uniform-surfaces": "arch",
    "designing-testable-seams": "arch",
    "evolving-schemas-and-contracts": "arch",
    "defending-architecture-decisions": "arch",
    "managing-complexity-budgets": "arch",
    "designing-data-pipelines": "arch",
    "code-architecture-review": "arch",
    "api-contract-audit": "arch",
    "refactor-execute": "arch",
    "building-unattended-agent-loops": "build",
    "grounding-ai-outputs": "build",
    "scaffolding-new-projects": "build",
    "building-small-cli-tools": "build",
    "building-installers-and-onboarding": "build",
    "building-code-generators": "build",
    "parsing-untrusted-text-robustly": "build",
    "hardening-trust-boundaries": "build",
    "hardening-ci-workflows": "build",
    "running-local-ci": "build",
    "bounding-untrusted-resource-use": "build",
    "controlling-processes-safely": "build",
    "keeping-event-loops-responsive": "build",
    "security-best-practices": "build",
    "engineering-for-determinism": "build",
    "nix-environments": "build",
    "layered-verification-gates": "verify",
    "driving-browsers-for-qa": "verify",
    "hunting-silent-failures": "verify",
    "debugging-across-layers": "verify",
    "clustering-failures-by-root-cause": "verify",
    "building-trustworthy-benchmarks": "verify",
    "making-verifiable-claims": "verify",
    "test-coverage": "verify",
    "dependency-audit": "verify",
}

CATEGORY_META = {
    "entry": ("Entry & Routing", "assets/icons/icon-entry.svg", "#00ff9d"),
    "plan": ("Frame, Plan & FinOps", "assets/icons/icon-plan.svg", "#00e5ff"),
    "arch": ("Architecture & Drivers", "assets/icons/icon-arch.svg", "#38bdf8"),
    "build": ("Build, AI & Security", "assets/icons/icon-build.svg", "#00e5ff"),
    "verify": ("Verify, QA & Coverage", "assets/icons/icon-verify.svg", "#00ff9d"),
    "sustain": ("Collaborate, Docs & Release", "assets/icons/icon-sustain.svg", "#38bdf8"),
}


def parse_frontmatter(skill_md: Path) -> tuple[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return skill_md.parent.name, ""
    fm = m.group(1)
    name_m = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    desc_m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
    return (
        name_m.group(1).strip() if name_m else skill_md.parent.name,
        desc_m.group(1).strip() if desc_m else "",
    )


def parse_shortcuts() -> dict[str, list[str]]:
    eng_text = (SKILLS_DIR / "eng" / "SKILL.md").read_text(encoding="utf-8")
    mapping: dict[str, list[str]] = {}
    for line in eng_text.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*`([a-z0-9-]+)`\s*\|$", line.strip())
        if m:
            words = [w.strip(" `") for w in m.group(1).split(",")]
            skill = m.group(2)
            mapping.setdefault(skill, []).extend(words)
    return mapping


def build_html() -> str:
    plugin_json = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    version = plugin_json.get("version", "0.17.0")
    shortcuts = parse_shortcuts()

    skills = []
    for p in sorted(SKILLS_DIR.iterdir()):
        skill_md = p / "SKILL.md"
        if p.is_dir() and skill_md.exists():
            name, desc = parse_frontmatter(skill_md)
            cat = CATEGORY_MAP.get(name, "sustain")
            skills.append(
                {
                    "name": name,
                    "desc": desc,
                    "cat": cat,
                    "shortcuts": shortcuts.get(name, []),
                }
            )

    skill_count = len(skills)

    # Build skill cards HTML
    skill_cards_html = []
    for s in skills:
        cat_label, cat_icon, cat_color = CATEGORY_META[s["cat"]]
        sc_badges = "".join(
            f'<span class="sc-pill">/eng {html.escape(w)}</span>' for w in s["shortcuts"]
        )
        skill_cards_html.append(
            f"""      <article class="skill-card" data-category="{s['cat']}" data-search="{html.escape((s['name'] + ' ' + s['desc'] + ' ' + ' '.join(s['shortcuts'])).lower())}">
        <div class="skill-card-head">
          <img src="{cat_icon}" alt="{html.escape(cat_label)}" class="skill-cat-icon" width="28" height="28" />
          <div class="skill-title-wrap">
            <h3 class="skill-name"><code>{html.escape(s['name'])}</code></h3>
            <span class="skill-cat-tag" style="border-color:{cat_color};color:{cat_color}">{html.escape(cat_label)}</span>
          </div>
        </div>
        <p class="skill-desc">{html.escape(s['desc'])}</p>
        <div class="skill-footer">
          <div class="sc-wrap">{sc_badges if sc_badges else '<span class="sc-none">Router auto-selects</span>'}</div>
        </div>
      </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>swe-skills v{version} — Deterministic Engineering &amp; Architecture Skills for AI Coding Agents</title>
  <meta name="description" content="{skill_count} evidence-derived software engineering, planning, architecture, and verification skills for Claude Code, Antigravity (agy), and Cursor." />
  <meta property="og:title" content="swe-skills v{version} — {skill_count} Engineering Skills for AI Agents" />
  <meta property="og:description" content="Deterministic software engineering, architecture, Tri-OS drivers, 8-tier verification, and context-guard skills for Claude Code, Antigravity, and Cursor." />
  <meta property="og:image" content="assets/logo.png" />
  <link rel="icon" type="image/svg+xml" href="assets/icon.svg" />
  <link rel="alternate icon" type="image/png" href="assets/icon.png" />
  <style>
    :root {{
      --bg-void: #04070f;
      --bg-deep: #070d1c;
      --bg-panel: rgba(10, 20, 42, 0.88);
      --bg-panel-hover: rgba(14, 28, 58, 0.95);
      --neon-cyan: #00e5ff;
      --neon-blue: #38bdf8;
      --neon-deep: #0284c7;
      --neon-emerald: #00ff9d;
      --neon-purple: #a855f7;
      --neon-magenta: #ff2a85;
      --text-bright: #f0f6fc;
      --text-body: #cbd5e1;
      --text-muted: #94a3b8;
      --border-cyan: rgba(0, 229, 255, 0.35);
      --glow-cyan: 0 0 22px rgba(0, 229, 255, 0.22);
      --font-mono: ui-monospace, 'Cascadia Code', 'Fira Code', 'JetBrains Mono', 'Source Code Pro', Menlo, Consolas, monospace;
      --font-sans: system-ui, -apple-system, 'Segoe UI', Roboto, Ubuntu, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      background-color: var(--bg-void);
      background-image:
        radial-gradient(circle at 50% 0%, rgba(0, 229, 255, 0.16), transparent 52%),
        radial-gradient(circle at 85% 35%, rgba(56, 189, 248, 0.10), transparent 45%),
        linear-gradient(rgba(0, 229, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.08) 1px, transparent 1px),
        linear-gradient(rgba(56, 189, 248, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.035) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 96px 96px, 96px 96px, 24px 24px, 24px 24px;
      background-attachment: fixed;
      color: var(--text-bright);
      font-family: var(--font-sans);
      line-height: 1.6;
      min-height: 100vh;
    }}

    a {{
      color: var(--neon-cyan);
      text-decoration: none;
      transition: color 0.15s ease, text-shadow 0.15s ease;
    }}

    a:hover {{
      color: var(--neon-emerald);
      text-shadow: 0 0 10px rgba(0, 255, 157, 0.45);
    }}

    /* Top Cyber Navbar */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(4, 7, 15, 0.88);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-cyan);
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.6);
    }}

    .nav-inner {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 0.75rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-family: var(--font-mono);
      font-weight: 800;
      font-size: 1.15rem;
      letter-spacing: 1.5px;
      color: var(--text-bright);
    }}

    .brand-badge {{
      font-size: 0.75rem;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      background: rgba(0, 255, 157, 0.12);
      border: 1px solid var(--neon-emerald);
      color: var(--neon-emerald);
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 1.25rem;
      flex-wrap: wrap;
      font-family: var(--font-mono);
      font-size: 0.86rem;
    }}

    .container {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 2.5rem 1.5rem 5rem;
    }}

    /* Hero Section */
    .hero {{
      text-align: center;
      margin-bottom: 3.5rem;
    }}

    .hero-banner-wrap {{
      border-radius: 16px;
      overflow: hidden;
      border: 1.5px solid var(--border-cyan);
      box-shadow: var(--glow-cyan), 0 18px 50px rgba(0, 0, 0, 0.75);
      margin-bottom: 1.75rem;
      background: #04070f;
    }}

    .hero-banner-wrap img {{
      display: block;
      width: 100%;
      height: auto;
    }}

    .hero-lead {{
      max-width: 920px;
      margin: 0 auto 1.75rem;
      font-size: 1.12rem;
      color: var(--text-body);
    }}

    .hero-actions {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 2rem;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.72rem 1.35rem;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.18s ease;
    }}

    .btn-primary {{
      background: linear-gradient(135deg, rgba(0, 229, 255, 0.22), rgba(2, 132, 199, 0.35));
      border: 1.5px solid var(--neon-cyan);
      color: var(--text-bright);
      box-shadow: var(--glow-cyan);
    }}

    .btn-primary:hover {{
      background: linear-gradient(135deg, rgba(0, 255, 157, 0.25), rgba(0, 229, 255, 0.35));
      border-color: var(--neon-emerald);
      color: #fff;
      transform: translateY(-1px);
    }}

    .btn-secondary {{
      background: var(--bg-panel);
      border: 1.5px solid rgba(56, 189, 248, 0.45);
      color: var(--neon-blue);
    }}

    .btn-secondary:hover {{
      border-color: var(--neon-cyan);
      color: var(--text-bright);
    }}

    /* Telemetry Stat Strip */
    .telemetry-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 3.5rem;
    }}

    .stat-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border-cyan);
      border-radius: 10px;
      padding: 1.15rem 1.25rem;
      position: relative;
      overflow: hidden;
      box-shadow: var(--glow-cyan);
    }}

    .stat-card::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--neon-cyan);
    }}

    .stat-value {{
      font-family: var(--font-mono);
      font-size: 1.75rem;
      font-weight: 900;
      color: var(--neon-cyan);
      line-height: 1.2;
    }}

    .stat-label {{
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-top: 0.25rem;
    }}

    /* Section Headers */
    .section-head {{
      margin-bottom: 1.75rem;
      border-bottom: 1px solid rgba(0, 229, 255, 0.25);
      padding-bottom: 0.75rem;
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.75rem;
    }}

    .section-tag {{
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--neon-emerald);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      display: block;
      margin-bottom: 0.2rem;
    }}

    .section-title {{
      font-size: 1.75rem;
      font-weight: 800;
      color: var(--text-bright);
      letter-spacing: 0.5px;
    }}

    /* Visual Showcase Gallery */
    .showcase-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 2rem;
      margin-bottom: 4rem;
    }}

    .showcase-card {{
      background: var(--bg-panel);
      border: 1.5px solid var(--border-cyan);
      border-radius: 14px;
      padding: 1.25rem;
      box-shadow: var(--glow-cyan);
      transition: border-color 0.2s ease;
    }}

    .showcase-card:hover {{
      border-color: var(--neon-cyan);
    }}

    .showcase-img-wrap {{
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid rgba(56, 189, 248, 0.3);
      background: #03060d;
      margin-bottom: 1rem;
    }}

    .showcase-img-wrap img {{
      display: block;
      width: 100%;
      height: auto;
    }}

    .showcase-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .showcase-caption {{
      font-size: 0.95rem;
      color: var(--text-body);
    }}

    .format-links {{
      display: flex;
      gap: 0.6rem;
      font-family: var(--font-mono);
      font-size: 0.8rem;
    }}

    .format-pill {{
      padding: 0.25rem 0.65rem;
      border-radius: 5px;
      background: rgba(0, 229, 255, 0.1);
      border: 1px solid var(--border-cyan);
      color: var(--neon-cyan);
    }}

    /* Quickstart & Recipes Grid */
    .recipes-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 1.25rem;
      margin-bottom: 4rem;
    }}

    .recipe-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border-cyan);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .recipe-title {{
      font-family: var(--font-mono);
      font-size: 1rem;
      font-weight: 700;
      color: var(--neon-cyan);
      margin-bottom: 0.4rem;
    }}

    .recipe-desc {{
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 0.85rem;
    }}

    .code-block {{
      background: #03060d;
      border: 1px solid rgba(2, 132, 199, 0.5);
      border-radius: 8px;
      padding: 0.85rem 1rem;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: #e2e8f0;
      overflow-x: auto;
      position: relative;
      white-space: pre;
    }}

    .copy-btn {{
      position: absolute;
      top: 0.45rem;
      right: 0.45rem;
      background: rgba(0, 229, 255, 0.14);
      border: 1px solid var(--neon-cyan);
      color: var(--neon-cyan);
      font-family: var(--font-mono);
      font-size: 0.72rem;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      cursor: pointer;
    }}

    .copy-btn:hover {{
      background: var(--neon-cyan);
      color: #03060d;
    }}

    /* Interactive Skill Explorer */
    .explorer-controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.5rem;
      background: var(--bg-panel);
      padding: 1rem 1.25rem;
      border-radius: 12px;
      border: 1px solid var(--border-cyan);
    }}

    .search-input {{
      flex: 1 1 280px;
      background: #03060d;
      border: 1.5px solid var(--neon-deep);
      border-radius: 8px;
      padding: 0.65rem 1rem;
      color: var(--text-bright);
      font-family: var(--font-mono);
      font-size: 0.9rem;
      outline: none;
    }}

    .search-input:focus {{
      border-color: var(--neon-cyan);
      box-shadow: var(--glow-cyan);
    }}

    .filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
    }}

    .filter-btn {{
      background: #061024;
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: var(--text-body);
      font-family: var(--font-mono);
      font-size: 0.78rem;
      padding: 0.45rem 0.8rem;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .filter-btn.active,
    .filter-btn:hover {{
      background: rgba(0, 229, 255, 0.18);
      border-color: var(--neon-cyan);
      color: var(--neon-cyan);
      font-weight: 700;
    }}

    .skills-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1.1rem;
      margin-bottom: 4rem;
    }}

    .skill-card {{
      background: var(--bg-panel);
      border: 1px solid rgba(0, 229, 255, 0.25);
      border-radius: 11px;
      padding: 1.15rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.16s ease, border-color 0.16s ease, background 0.16s ease;
    }}

    .skill-card:hover {{
      transform: translateY(-2px);
      border-color: var(--neon-cyan);
      background: var(--bg-panel-hover);
      box-shadow: var(--glow-cyan);
    }}

    .skill-card-head {{
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      margin-bottom: 0.65rem;
    }}

    .skill-cat-icon {{
      flex-shrink: 0;
      margin-top: 2px;
    }}

    .skill-title-wrap {{
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}

    .skill-name code {{
      font-family: var(--font-mono);
      font-size: 0.96rem;
      font-weight: 700;
      color: var(--text-bright);
    }}

    .skill-cat-tag {{
      display: inline-block;
      align-self: flex-start;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      padding: 0.08rem 0.45rem;
      border-radius: 4px;
      border: 1px solid;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }}

    .skill-desc {{
      font-size: 0.86rem;
      color: var(--text-body);
      margin-bottom: 0.85rem;
      flex-grow: 1;
    }}

    .skill-footer {{
      border-top: 1px solid rgba(56, 189, 248, 0.16);
      padding-top: 0.55rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .sc-wrap {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
    }}

    .sc-pill {{
      font-family: var(--font-mono);
      font-size: 0.74rem;
      padding: 0.12rem 0.5rem;
      border-radius: 4px;
      background: rgba(0, 255, 157, 0.12);
      border: 1px solid rgba(0, 255, 157, 0.5);
      color: var(--neon-emerald);
    }}

    .sc-none {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-muted);
    }}

    /* Documentation Hub Cards */
    .docs-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.15rem;
      margin-bottom: 3rem;
    }}

    .doc-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border-cyan);
      border-radius: 11px;
      padding: 1.2rem;
      display: block;
      transition: all 0.18s ease;
    }}

    .doc-card:hover {{
      border-color: var(--neon-emerald);
      transform: translateY(-2px);
      box-shadow: 0 0 20px rgba(0, 255, 157, 0.18);
    }}

    .doc-card h3 {{
      font-family: var(--font-mono);
      font-size: 1rem;
      color: var(--neon-cyan);
      margin-bottom: 0.4rem;
    }}

    .doc-card p {{
      font-size: 0.86rem;
      color: var(--text-body);
    }}

    footer {{
      border-top: 1px solid var(--border-cyan);
      padding: 2rem 1.5rem;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: var(--text-muted);
      background: rgba(4, 7, 15, 0.9);
    }}
  </style>
</head>
<body>

  <nav class="navbar">
    <div class="nav-inner">
      <div class="brand">
        <img src="assets/icon.svg" alt="swe-skills icon" width="32" height="32" />
        <span>SWE-SKILLS</span>
        <span class="brand-badge">v{version} • {skill_count} SKILLS</span>
      </div>
      <div class="nav-links">
        <a href="#showcase">Visual Showcase</a>
        <a href="#quickstart">Quickstart &amp; Examples</a>
        <a href="#explorer">Skill Explorer ({skill_count})</a>
        <a href="#docs-hub">Documentation Hub</a>
        <a href="usermanual/README.md">User Manual</a>
        <a href="https://github.com/bsommers/swe-skills-2">GitHub</a>
      </div>
    </div>
  </nav>

  <main class="container">
    <!-- Hero Banner -->
    <section class="hero">
      <div class="hero-banner-wrap">
        <img src="assets/logo.svg" alt="swe-skills futuristic cyber-core banner" width="1200" height="380" />
      </div>
      <p class="hero-lead">
        A deterministic software engineering, planning, architecture, and multi-tier verification skill library for
        <strong>Claude Code</strong>, <strong>Antigravity (<code>agy</code>)</strong>, and <strong>Cursor</strong>.
        Distilled from real-world incidents across 20+ production repositories.
      </p>
      <div class="hero-actions">
        <a href="#explorer" class="btn btn-primary">Explore All {skill_count} Skills</a>
        <a href="#showcase" class="btn btn-secondary">View Graphic Examples</a>
        <a href="usermanual/README.md" class="btn btn-secondary">Read 7-Chapter User Manual</a>
      </div>
    </section>

    <!-- Telemetry Strip -->
    <section class="telemetry-grid">
      <div class="stat-card">
        <div class="stat-value">{skill_count}</div>
        <div class="stat-label">Verified Engineering Skills</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">1–3</div>
        <div class="stat-label">Bounded Active Skills / Turn</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">8 Tiers</div>
        <div class="stat-label">Smoke • Unit • Integr • Sys • Perf • Stress • Torture • Sec</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">Tri-OS</div>
        <div class="stat-label">Windows • macOS • Linux Parity</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">-85%</div>
        <div class="stat-label">Prompt Token Overhead via Profiles</div>
      </div>
    </section>

    <!-- Visual Architecture & Graphic Examples Showcase -->
    <section id="showcase">
      <div class="section-head">
        <div>
          <span class="section-tag">FUTURISTIC NEON-GRID TELEMETRY // SVG + PNG</span>
          <h2 class="section-title">Architecture &amp; Workflow Graphic Examples</h2>
        </div>
        <span style="font-family:var(--font-mono);font-size:0.82rem;color:var(--text-muted)">
          Generated deterministically by <code>scripts/render-graphics.py</code>
        </span>
      </div>

      <div class="showcase-grid">
        <div class="showcase-card">
          <div class="showcase-img-wrap">
            <img src="assets/examples/architecture-overview.svg" alt="5-Tier Runtime Engineering Governance Architecture" loading="lazy" />
          </div>
          <div class="showcase-meta">
            <p class="showcase-caption">
              <strong>5-Tier Runtime Governance Architecture:</strong> Multi-harness adapters, stdlib lifecycle hooks (<code>context_guard.py</code>, <code>model_router.py</code>), <code>/eng</code> task sizer, {skill_count}-skill taxonomy, and subagent log isolation.
            </p>
            <div class="format-links">
              <a class="format-pill" href="assets/examples/architecture-overview.svg">Vector SVG</a>
              <a class="format-pill" href="assets/examples/architecture-overview.png">Hi-DPI PNG</a>
            </div>
          </div>
        </div>

        <div class="showcase-card">
          <div class="showcase-img-wrap">
            <img src="assets/examples/workflow-eng-routing.svg" alt="/eng Dispatch, Bounded Skill Set and 8-Tier Verification Matrix" loading="lazy" />
          </div>
          <div class="showcase-meta">
            <p class="showcase-caption">
              <strong>Example 01 — <code>/eng</code> Routing &amp; Pre-Build Exhaustive Test Matrix:</strong> Sizing a feature, loading 1–3 skills, writing the 6-dimension RED test matrix, and gating completion with <code>scripts/verify.sh --quick</code>.
            </p>
            <div class="format-links">
              <a class="format-pill" href="assets/examples/workflow-eng-routing.svg">Vector SVG</a>
              <a class="format-pill" href="assets/examples/workflow-eng-routing.png">Hi-DPI PNG</a>
            </div>
          </div>
        </div>

        <div class="showcase-card">
          <div class="showcase-img-wrap">
            <img src="assets/examples/workflow-subagent-isolation.svg" alt="Subagent Log Isolation and Adaptive Model Routing" loading="lazy" />
          </div>
          <div class="showcase-meta">
            <p class="showcase-caption">
              <strong>Example 02 — Subagent Log Isolation &amp; FinOps:</strong> Quarantining noisy compiler/test retry loops inside ephemeral <code>flash</code> / Haiku worker subagents so the primary <code>pro</code> session stays crystal-clear.
            </p>
            <div class="format-links">
              <a class="format-pill" href="assets/examples/workflow-subagent-isolation.svg">Vector SVG</a>
              <a class="format-pill" href="assets/examples/workflow-subagent-isolation.png">Hi-DPI PNG</a>
            </div>
          </div>
        </div>

        <div class="showcase-card">
          <div class="showcase-img-wrap">
            <img src="assets/examples/workflow-session-chaining.svg" alt="Periodic Cadence Hooks and 5-Step Lossless Session Chaining" loading="lazy" />
          </div>
          <div class="showcase-meta">
            <p class="showcase-caption">
              <strong>Example 03 — Periodic Cadence Hooks &amp; 5-Step Session Chaining:</strong> Automated 12-turn / 25-step checkpoint reminders, <code>PreCompact</code> blocking, and zero-loss chaining via <code>scripts/chain-session.sh</code>.
            </p>
            <div class="format-links">
              <a class="format-pill" href="assets/examples/workflow-session-chaining.svg">Vector SVG</a>
              <a class="format-pill" href="assets/examples/workflow-session-chaining.png">Hi-DPI PNG</a>
            </div>
          </div>
        </div>

        <div class="showcase-card">
          <div class="showcase-img-wrap">
            <img src="assets/examples/workflow-browser-qa-tri-os.svg" alt="Browser QA Automation and Cross-Platform Tri-OS Driver Architecture" loading="lazy" />
          </div>
          <div class="showcase-meta">
            <p class="showcase-caption">
              <strong>Example 04 — Browser QA Automation &amp; Tri-OS Driver Architecture:</strong> Live Playwright/WebDriver BiDi verification with recorded traces alongside Windows, macOS, and Linux driver contracts.
            </p>
            <div class="format-links">
              <a class="format-pill" href="assets/examples/workflow-browser-qa-tri-os.svg">Vector SVG</a>
              <a class="format-pill" href="assets/examples/workflow-browser-qa-tri-os.png">Hi-DPI PNG</a>
            </div>
          </div>
        </div>

        <div class="showcase-card">
          <div class="showcase-img-wrap">
            <img src="assets/examples/workflow-local-tools-and-ci.svg" alt="Searchable Local Tool Registry, VM Sandboxes and Zero-Minute Local CI" loading="lazy" />
          </div>
          <div class="showcase-meta">
            <p class="showcase-caption">
              <strong>Example 05 — Local Tool Registry, VM Sandboxes &amp; Local-First CI:</strong> Discovering <code>~/src</code> VMs (<code>cvm</code>, <code>win-devvm</code>, <code>gha-vm-runners</code>, <code>fedora-vms</code>, <code>freebsd-kvm</code>) and executing CI locally to conserve hosted GitHub Actions minutes.
            </p>
            <div class="format-links">
              <a class="format-pill" href="assets/examples/workflow-local-tools-and-ci.svg">Vector SVG</a>
              <a class="format-pill" href="assets/examples/workflow-local-tools-and-ci.png">Hi-DPI PNG</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Quickstart & Runnable Recipes -->
    <section id="quickstart">
      <div class="section-head">
        <div>
          <span class="section-tag">COPY-PASTEABLE WORKFLOWS</span>
          <h2 class="section-title">Quickstart &amp; Operational Recipes</h2>
        </div>
      </div>

      <div class="recipes-grid">
        <div class="recipe-card">
          <div>
            <div class="recipe-title">1. Multi-Harness Install &amp; Profiles</div>
            <p class="recipe-desc">Install all {skill_count} skills across Claude Code, Antigravity, and Cursor, or mount a focused profile to save ~85% prompt tokens.</p>
          </div>
          <div class="code-block"><button class="copy-btn" onclick="copyCode(this)">Copy</button>scripts/install.sh --all
scripts/install.sh --claude --profile core
python3 scripts/hooks/install-hooks.py --claude --agy</div>
        </div>

        <div class="recipe-card">
          <div>
            <div class="recipe-title">2. /eng Unified Router &amp; Shortcuts</div>
            <p class="recipe-desc">Type <code>/eng</code> with free text to size &amp; route automatically, or invoke an exact shortcut word.</p>
          </div>
          <div class="code-block"><button class="copy-btn" onclick="copyCode(this)">Copy</button>/eng add retry logic across API modules
/eng tdd        # designing-exhaustive-test-cases
/eng qa-drive   # driving-browsers-for-qa
/eng chain      # 5-step lossless session chain</div>
        </div>

        <div class="recipe-card">
          <div>
            <div class="recipe-title">3. Render SVG/PNG Graphics &amp; Verify Suite</div>
            <p class="recipe-desc">Re-render all 13 SVG + 13 PNG neon-grid visuals, rebuild GitHub Pages, and run the verification suite.</p>
          </div>
          <div class="code-block"><button class="copy-btn" onclick="copyCode(this)">Copy</button>python3 scripts/render-graphics.py
python3 scripts/build-pages.py
python3 scripts/lint-skills.py --words
python3 -m unittest discover tests -q</div>
        </div>
      </div>
    </section>

    <!-- Interactive Skill Explorer -->
    <section id="explorer">
      <div class="section-head">
        <div>
          <span class="section-tag">INTERACTIVE CATALOG</span>
          <h2 class="section-title">Skill &amp; Shortcut Explorer (<span id="visible-count">{skill_count}</span> / {skill_count})</h2>
        </div>
      </div>

      <div class="explorer-controls">
        <input
          type="search"
          id="skill-search"
          class="search-input"
          placeholder="Search {skill_count} skills by name, trigger keyword, or /eng shortcut..."
          oninput="filterSkills()"
        />
        <div class="filter-tabs">
          <button class="filter-btn active" data-cat="all" onclick="setCategory('all', this)">All ({skill_count})</button>
          <button class="filter-btn" data-cat="entry" onclick="setCategory('entry', this)">Entry</button>
          <button class="filter-btn" data-cat="plan" onclick="setCategory('plan', this)">Frame &amp; Plan</button>
          <button class="filter-btn" data-cat="arch" onclick="setCategory('arch', this)">Architecture</button>
          <button class="filter-btn" data-cat="build" onclick="setCategory('build', this)">Build &amp; Security</button>
          <button class="filter-btn" data-cat="verify" onclick="setCategory('verify', this)">Verify &amp; QA</button>
          <button class="filter-btn" data-cat="sustain" onclick="setCategory('sustain', this)">Sustain &amp; Docs</button>
        </div>
      </div>

      <div class="skills-grid" id="skills-grid">
{chr(10).join(skill_cards_html)}
      </div>
    </section>

    <!-- Documentation Hub -->
    <section id="docs-hub">
      <div class="section-head">
        <div>
          <span class="section-tag">COMPLETE REFERENCE SUITE</span>
          <h2 class="section-title">Documentation Hub</h2>
        </div>
      </div>

      <div class="docs-grid">
        <a class="doc-card" href="README.md">
          <h3>Documentation Index</h3>
          <p>Central navigational map and recommended reading order across all guides and visual diagrams.</p>
        </a>
        <a class="doc-card" href="purpose.md">
          <h3>Purpose &amp; Threat Model</h3>
          <p>Systemic LLM failure modes, defense-in-depth security boundaries, and token economics.</p>
        </a>
        <a class="doc-card" href="architecture.md">
          <h3>System Architecture</h3>
          <p>5-tier runtime governance, multi-harness integration, lifecycle hooks, and subagent log isolation.</p>
        </a>
        <a class="doc-card" href="running.md">
          <h3>Running &amp; Configuration</h3>
          <p>Installation targets, token-saving skill profiles, CLI tools, environment variables, and exit codes.</p>
        </a>
        <a class="doc-card" href="how-to.md">
          <h3>How-To Recipes &amp; Examples</h3>
          <p>Step-by-step operational recipes paired with rendered SVG/PNG visual walkthroughs.</p>
        </a>
        <a class="doc-card" href="usermanual/README.md">
          <h3>7-Chapter User Manual</h3>
          <p>Exhaustive reference covering getting started, full catalog, hooks, workflows, skill authoring, and FAQ.</p>
        </a>
        <a class="doc-card" href="HOOKS.md">
          <h3>Lifecycle Hooks &amp; Cadence</h3>
          <p>Periodic turn/step checkpoint cadence, PreCompact guards, cold-cache detection, and model routing.</p>
        </a>
        <a class="doc-card" href="EVIDENCE.md">
          <h3>Empirical Provenance</h3>
          <p>Concrete post-mortems, commit histories, and incident sources across 20+ repositories.</p>
        </a>
      </div>
    </section>
  </main>

  <footer>
    <p>swe-skills v{version} • {skill_count} Evidence-Derived Engineering Skills • Apache-2.0 License</p>
  </footer>

  <script>
    let activeCategory = 'all';

    function setCategory(cat, btn) {{
      activeCategory = cat;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterSkills();
    }}

    function filterSkills() {{
      const query = (document.getElementById('skill-search').value || '').trim().toLowerCase();
      const cards = document.querySelectorAll('.skill-card');
      let shown = 0;
      cards.forEach(card => {{
        const catMatch = activeCategory === 'all' || card.dataset.category === activeCategory;
        const searchMatch = !query || card.dataset.search.includes(query);
        if (catMatch && searchMatch) {{
          card.style.display = 'flex';
          shown++;
        }} else {{
          card.style.display = 'none';
        }}
      }});
      document.getElementById('visible-count').textContent = shown;
    }}

    function copyCode(btn) {{
      const block = btn.parentElement;
      const text = block.textContent.replace(/^Copy/, '').trim();
      navigator.clipboard.writeText(text).then(() => {{
        const orig = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => {{ btn.textContent = orig; }}, 1400);
      }});
    }}
  </script>
</body>
</html>
"""


def main() -> int:
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    out = DOCS / "index.html"
    out.write_text(build_html(), encoding="utf-8")
    print(f"Generated {out.relative_to(ROOT)} and docs/.nojekyll.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
