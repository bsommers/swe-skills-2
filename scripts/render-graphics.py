#!/usr/bin/env python3
"""Deterministic SVG + PNG graphics, logo, icon, and visual example generator for swe-skills.

Generates:
1. Hero Logo Banner:       docs/assets/logo.svg + docs/assets/logo.png (1200x380)
2. Square Plugin/App Icon: assets/logo.svg + assets/logo.png + docs/assets/icon.svg + docs/assets/icon.png (512x512)
3. Category Neon Icons:    docs/assets/icons/icon-{entry,plan,arch,build,verify,sustain}.{svg,png} (64x64 / 256px PNG)
4. Graphic Example Cards:  docs/assets/examples/*.{svg,png} (1200x620):
   - architecture-overview.{svg,png}
   - workflow-eng-routing.{svg,png}
   - workflow-subagent-isolation.{svg,png}
   - workflow-session-chaining.{svg,png}
   - workflow-browser-qa-tri-os.{svg,png}

Theme: Futuristic obsidian-black background (#050811) with light-blue neon cyber grid (#00e5ff / #38bdf8).
"""

from __future__ import annotations

import argparse
import html
import json
import math
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_ASSETS = ROOT / "docs" / "assets"
ROOT_ASSETS = ROOT / "assets"
ICONS_DIR = DOCS_ASSETS / "icons"
EXAMPLES_DIR = DOCS_ASSETS / "examples"


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def get_metadata() -> tuple[str, int]:
    plugin_json = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    version = plugin_json.get("version", "0.17.0")
    skills_dir = ROOT / "skills"
    skill_count = sum(1 for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    return version, skill_count


def hex_points(cx: float, cy: float, r: float, rotate_deg: float = -90.0) -> str:
    pts = []
    for i in range(6):
        ang = math.radians(rotate_deg + i * 60.0)
        pts.append(f"{cx + r * math.cos(ang):.1f},{cy + r * math.sin(ang):.1f}")
    return " ".join(pts)


def hex_vertices(cx: float, cy: float, r: float, rotate_deg: float = -90.0) -> list[tuple[float, float]]:
    verts = []
    for i in range(6):
        ang = math.radians(rotate_deg + i * 60.0)
        verts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return verts


def common_defs(width: int, height: int) -> str:
    return f"""  <defs>
    <linearGradient id="bg-void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#03060d" />
      <stop offset="45%" stop-color="#071022" />
      <stop offset="100%" stop-color="#030710" />
    </linearGradient>
    <radialGradient id="neon-aura" cx="50%" cy="42%" r="60%">
      <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.18" />
      <stop offset="45%" stop-color="#38bdf8" stop-opacity="0.07" />
      <stop offset="100%" stop-color="#03060d" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="cyan-beam" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.05" />
      <stop offset="50%" stop-color="#00e5ff" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.05" />
    </linearGradient>
    <linearGradient id="core-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00ff9d" />
      <stop offset="50%" stop-color="#00e5ff" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <linearGradient id="panel-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0b162c" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#060c1a" stop-opacity="0.95" />
    </linearGradient>
    <pattern id="minor-grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#38bdf8" stroke-width="0.6" stroke-opacity="0.09" />
    </pattern>
    <pattern id="major-grid" width="96" height="96" patternUnits="userSpaceOnUse">
      <rect width="96" height="96" fill="url(#minor-grid)" />
      <path d="M 96 0 L 0 0 0 96" fill="none" stroke="#00e5ff" stroke-width="1.0" stroke-opacity="0.20" />
      <circle cx="0" cy="0" r="1.6" fill="#00e5ff" fill-opacity="0.45" />
    </pattern>
    <filter id="glow-strong" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="b1" />
      <feGaussianBlur stdDeviation="2" result="b2" />
      <feMerge>
        <feMergeNode in="b1" />
        <feMergeNode in="b2" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="glow-soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <style>
      .f-mono {{ font-family: ui-monospace, 'Cascadia Code', 'Fira Code', 'JetBrains Mono', 'Source Code Pro', Menlo, Consolas, monospace; }}
      .f-sans {{ font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Ubuntu, sans-serif; }}
    </style>
  </defs>"""


def perspective_horizon(width: int, height: int, horizon_y: int) -> str:
    lines = []
    steps = [0.08, 0.18, 0.31, 0.47, 0.66, 0.88]
    for s in steps:
        y = int(horizon_y + (height - horizon_y) * s)
        op = 0.08 + s * 0.18
        lines.append(
            f'    <line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#00e5ff" stroke-width="1" stroke-opacity="{op:.2f}" />'
        )
    cx = width // 2
    for offset in range(-9, 10):
        x_bottom = cx + offset * 115
        x_top = cx + offset * 28
        op = max(0.06, 0.22 - abs(offset) * 0.015)
        lines.append(
            f'    <line x1="{x_top}" y1="{horizon_y}" x2="{x_bottom}" y2="{height}" stroke="#38bdf8" stroke-width="0.9" stroke-opacity="{op:.2f}" />'
        )
    return "\n".join(lines)


def hud_reticles(x: int, y: int, w: int, h: int, size: int = 14, color: str = "#00e5ff", sw: float = 2.2) -> str:
    return "\n".join(
        [
            f'  <path d="M {x} {y+size} L {x} {y} L {x+size} {y}" fill="none" stroke="{color}" stroke-width="{sw}" />',
            f'  <path d="M {x+w-size} {y} L {x+w} {y} L {x+w} {y+size}" fill="none" stroke="{color}" stroke-width="{sw}" />',
            f'  <path d="M {x} {y+h-size} L {x} {y+h} L {x+size} {y+h}" fill="none" stroke="{color}" stroke-width="{sw}" />',
            f'  <path d="M {x+w-size} {y+h} L {x+w} {y+h} L {x+w} {y+h-size}" fill="none" stroke="{color}" stroke-width="{sw}" />',
        ]
    )


def render_cyber_emblem(cx: float, cy: float, scale: float = 1.0) -> str:
    r_outer = 118 * scale
    r_mid = 88 * scale
    r_inner = 54 * scale
    r_core = 26 * scale

    outer_pts = hex_points(cx, cy, r_outer, -90)
    mid_pts = hex_points(cx, cy, r_mid, -60)
    inner_pts = hex_points(cx, cy, r_inner, -90)
    core_pts = hex_points(cx, cy, r_core, -90)

    spokes = []
    for vx, vy in hex_vertices(cx, cy, r_outer, -90):
        spokes.append(
            f'    <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{vx:.1f}" y2="{vy:.1f}" stroke="#00e5ff" stroke-width="{1.6*scale:.1f}" stroke-opacity="0.35" />'
        )
        spokes.append(
            f'    <circle cx="{vx:.1f}" cy="{vy:.1f}" r="{4.2*scale:.1f}" fill="#050811" stroke="#00e5ff" stroke-width="{2.2*scale:.1f}" />'
        )
        spokes.append(f'    <circle cx="{vx:.1f}" cy="{vy:.1f}" r="{1.8*scale:.1f}" fill="#00ff9d" />')

    mid_nodes = []
    for vx, vy in hex_vertices(cx, cy, r_mid, -60):
        mid_nodes.append(f'    <circle cx="{vx:.1f}" cy="{vy:.1f}" r="{3.0*scale:.1f}" fill="#38bdf8" />')

    v_core = hex_vertices(cx, cy, r_core, -90)
    iso_lines = [
        f'    <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{v_core[0][0]:.1f}" y2="{v_core[0][1]:.1f}" stroke="#050811" stroke-width="{2.0*scale:.1f}" />',
        f'    <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{v_core[2][0]:.1f}" y2="{v_core[2][1]:.1f}" stroke="#050811" stroke-width="{2.0*scale:.1f}" />',
        f'    <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{v_core[4][0]:.1f}" y2="{v_core[4][1]:.1f}" stroke="#050811" stroke-width="{2.0*scale:.1f}" />',
    ]

    return "\n".join(
        [
            '  <g id="cyber-emblem">',
            f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_outer*1.12:.1f}" fill="none" stroke="#0284c7" stroke-width="{1.2*scale:.1f}" stroke-dasharray="{6*scale:.1f} {6*scale:.1f}" stroke-opacity="0.55" />',
            f'    <polygon points="{outer_pts}" fill="#071226" fill-opacity="0.82" stroke="#00e5ff" stroke-width="{3.2*scale:.1f}" filter="url(#glow-soft)" />',
            *spokes,
            f'    <polygon points="{mid_pts}" fill="none" stroke="#38bdf8" stroke-width="{2.0*scale:.1f}" stroke-dasharray="{8*scale:.1f} {4*scale:.1f}" />',
            *mid_nodes,
            f'    <polygon points="{inner_pts}" fill="#0a1936" stroke="#00ff9d" stroke-width="{2.4*scale:.1f}" />',
            f'    <polygon points="{core_pts}" fill="url(#core-grad)" filter="url(#glow-soft)" />',
            *iso_lines,
            f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{4.5*scale:.1f}" fill="#f0f6fc" />',
            "  </g>",
        ]
    )


def build_square_icon_svg() -> str:
    w, h = 512, 512
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
{common_defs(w, h)}
  <rect width="{w}" height="{h}" rx="72" fill="url(#bg-void)" />
  <rect width="{w}" height="{h}" rx="72" fill="url(#major-grid)" />
  <rect width="{w}" height="{h}" rx="72" fill="url(#neon-aura)" />
  <rect x="18" y="18" width="{w-36}" height="{h-36}" rx="56" fill="none" stroke="#00e5ff" stroke-width="3" stroke-opacity="0.55" />
{hud_reticles(38, 38, w-76, h-76, size=28, color="#00e5ff", sw=3.5)}
{render_cyber_emblem(256, 256, scale=1.75)}
</svg>
"""


def build_hero_logo_svg(version: str, skill_count: int) -> str:
    w, h = 1200, 380
    badges = [
        (360, 286, 188, "#00ff9d", f"{skill_count} SKILLS VERIFIED"),
        (560, 286, 184, "#00e5ff", "8-TIER TEST MATRIX"),
        (756, 286, 218, "#38bdf8", "TRI-OS: WIN • MAC • LINUX"),
        (986, 286, 162, "#a855f7", f"RELEASE v{version}"),
    ]
    badge_svg = []
    for bx, by, bw, color, label in badges:
        badge_svg.append(
            f'  <rect x="{bx}" y="{by}" width="{bw}" height="34" rx="6" fill="#071328" stroke="{color}" stroke-width="1.5" />'
            f'  <circle cx="{bx+15}" cy="{by+17}" r="4.2" fill="{color}" />'
            f'  <text x="{bx+27}" y="{by+22}" class="f-mono" font-size="11.5" font-weight="700" fill="#f0f6fc">{esc(label)}</text>'
        )

    subtitle = esc("ENGINEERING, ARCHITECTURE & VERIFICATION SKILLS FOR AI CODING AGENTS")
    cmd_bar = esc("/eng <task | shortcut>   |   scripts/install.sh --all   |   scripts/verify.sh --quick")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
{common_defs(w, h)}
  <rect width="{w}" height="{h}" rx="16" fill="url(#bg-void)" />
  <rect width="{w}" height="{h}" rx="16" fill="url(#major-grid)" />
  <g id="perspective-floor">
{perspective_horizon(w, h, 240)}
  </g>
  <rect width="{w}" height="{h}" rx="16" fill="url(#neon-aura)" />
  <rect x="12" y="12" width="{w-24}" height="{h-24}" rx="12" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-opacity="0.65" />
{hud_reticles(22, 22, w-44, h-44, size=22, color="#00e5ff", sw=2.5)}

  <!-- Top Telemetry Bar -->
  <text x="44" y="46" class="f-mono" font-size="12" fill="#38bdf8" letter-spacing="2">SYS.GOVERNANCE // DETERMINISTIC AI SOFTWARE ENGINEERING</text>
  <text x="{w-44}" y="46" text-anchor="end" class="f-mono" font-size="12" fill="#00ff9d" letter-spacing="1.5">STATUS: ONLINE • {skill_count} ACTIVE MODULES</text>
  <line x1="44" y1="58" x2="{w-44}" y2="58" stroke="url(#cyan-beam)" stroke-width="1.5" />

  <!-- Cyber Emblem -->
{render_cyber_emblem(188, 196, scale=1.08)}

  <!-- Title & Subtitle Block -->
  <text x="360" y="146" class="f-mono" font-size="72" font-weight="900" fill="#f0f6fc" letter-spacing="5" filter="url(#glow-soft)">SWE-SKILLS</text>
  <text x="360" y="146" class="f-mono" font-size="72" font-weight="900" fill="none" stroke="#00e5ff" stroke-width="1.5" letter-spacing="5">SWE-SKILLS</text>

  <text x="362" y="185" class="f-sans" font-size="18.2" font-weight="700" fill="#00e5ff" letter-spacing="0.7">{subtitle}</text>
  <text x="362" y="216" class="f-mono" font-size="14.5" fill="#94a3b8">Claude Code  •  Antigravity (agy)  •  Cursor  •  Open Agent Harnesses (~/.agents/skills)</text>

  <!-- Command Quick-Dispatch Bar -->
  <rect x="360" y="234" width="788" height="38" rx="6" fill="#060e1f" stroke="#0284c7" stroke-width="1.2" />
  <text x="378" y="258" class="f-mono" font-size="13.5" fill="#00ff9d">$</text>
  <text x="396" y="258" class="f-mono" font-size="13.5" fill="#e2e8f0">{cmd_bar}</text>

  <!-- Telemetry Badges -->
{chr(10).join(badge_svg)}
</svg>
"""


def build_category_icon_svg(kind: str) -> str:
    glyphs = {
        "entry": """
    <circle cx="18" cy="32" r="5" fill="#00ff9d" stroke="#00e5ff" stroke-width="2" />
    <path d="M 23 32 L 33 32 L 45 18 M 33 32 L 47 32 M 33 32 L 45 46" fill="none" stroke="#00e5ff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" />
    <circle cx="47" cy="18" r="3.5" fill="#38bdf8" />
    <circle cx="49" cy="32" r="3.5" fill="#00ff9d" />
    <circle cx="47" cy="46" r="3.5" fill="#38bdf8" />""",
        "plan": """
    <rect x="15" y="14" width="34" height="36" rx="4" fill="#09152b" stroke="#00e5ff" stroke-width="2.2" />
    <line x1="22" y1="23" x2="42" y2="23" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round" />
    <line x1="22" y1="32" x2="36" y2="32" stroke="#00e5ff" stroke-width="2.2" stroke-linecap="round" />
    <path d="M 22 41 L 26 44 L 33 37" fill="none" stroke="#00ff9d" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />""",
        "arch": """
    <polygon points="32,12 49,22 49,42 32,52 15,42 15,22" fill="#09152b" stroke="#00e5ff" stroke-width="2.4" />
    <polygon points="32,21 41,26.5 41,37.5 32,43 23,37.5 23,26.5" fill="none" stroke="#38bdf8" stroke-width="1.8" />
    <circle cx="32" cy="32" r="4" fill="#00ff9d" />""",
        "build": """
    <path d="M 32 12 L 48 19 L 48 33 C 48 43 40 49 32 52 C 24 49 16 43 16 33 L 16 19 Z" fill="#09152b" stroke="#00e5ff" stroke-width="2.4" />
    <path d="M 24 29 L 29 34 L 24 39 M 32 39 L 40 39" fill="none" stroke="#00ff9d" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />""",
        "verify": """
    <circle cx="32" cy="32" r="19" fill="#09152b" stroke="#00e5ff" stroke-width="2.4" />
    <circle cx="32" cy="32" r="12" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4 3" />
    <path d="M 24 32 L 30 38 L 41 25" fill="none" stroke="#00ff9d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />""",
        "sustain": """
    <path d="M 20 26 A 14 14 0 1 1 19 38" fill="none" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round" />
    <polyline points="15,25 20,26 22,20" fill="none" stroke="#00ff9d" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
    <polygon points="32,24 39,32 32,40 25,32" fill="#00ff9d" fill-opacity="0.25" stroke="#00ff9d" stroke-width="2" />""",
    }
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <pattern id="g" width="16" height="16" patternUnits="userSpaceOnUse">
      <path d="M 16 0 L 0 0 0 16" fill="none" stroke="#00e5ff" stroke-width="0.6" stroke-opacity="0.16" />
    </pattern>
  </defs>
  <rect x="3" y="3" width="58" height="58" rx="14" fill="#050914" stroke="#00e5ff" stroke-width="2" />
  <rect x="3" y="3" width="58" height="58" rx="14" fill="url(#g)" />
  {glyphs[kind]}
</svg>
"""


def card_frame(
    w: int,
    h: int,
    tag: str,
    title: str,
    subtitle: str,
    body_svg: str,
    footer_left: str,
    footer_right: str,
) -> str:
    tag_w = max(170, int(len(tag) * 8.6) + 28)
    tag_cx = 42 + tag_w // 2
    title_x = 42 + tag_w + 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
{common_defs(w, h)}
  <rect width="{w}" height="{h}" rx="16" fill="url(#bg-void)" />
  <rect width="{w}" height="{h}" rx="16" fill="url(#major-grid)" />
  <g id="perspective-grid">
{perspective_horizon(w, h, h - 135)}
  </g>
  <rect width="{w}" height="{h}" rx="16" fill="url(#neon-aura)" />
  <rect x="12" y="12" width="{w-24}" height="{h-24}" rx="12" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-opacity="0.65" />
{hud_reticles(22, 22, w-44, h-44, size=20, color="#00e5ff", sw=2.4)}

  <!-- Header -->
  <rect x="42" y="30" width="{tag_w}" height="26" rx="5" fill="#071936" stroke="#00e5ff" stroke-width="1.3" />
  <text x="{tag_cx}" y="47" text-anchor="middle" class="f-mono" font-size="11.5" font-weight="700" fill="#00e5ff" letter-spacing="1.2">{esc(tag)}</text>
  <text x="{title_x}" y="49" class="f-sans" font-size="22.5" font-weight="800" fill="#f0f6fc" letter-spacing="0.4">{esc(title)}</text>
  <text x="42" y="77" class="f-mono" font-size="13" fill="#94a3b8">{esc(subtitle)}</text>
  <line x1="42" y1="92" x2="{w-42}" y2="92" stroke="url(#cyan-beam)" stroke-width="1.5" />

  <!-- Body Content -->
{body_svg}

  <!-- Footer Telemetry -->
  <line x1="42" y1="{h-54}" x2="{w-42}" y2="{h-54}" stroke="#0284c7" stroke-width="1" stroke-opacity="0.5" />
  <text x="42" y="{h-30}" class="f-mono" font-size="11.5" fill="#38bdf8">{esc(footer_left)}</text>
  <text x="{w-42}" y="{h-30}" text-anchor="end" class="f-mono" font-size="11.5" fill="#00ff9d">{esc(footer_right)}</text>
</svg>
"""


def build_architecture_overview_svg(skill_count: int) -> str:
    w, h = 1200, 620
    tiers = [
        (
            110,
            "#00e5ff",
            "TIER 1 // HARNESS INTEGRATION LAYER",
            "Claude Code (~/.claude/skills)   •   Antigravity (plugin.json + hooks.json)   •   Cursor (~/.cursor/skills + .mdc)   •   ~/.agents/skills",
            "Zero-fork multi-runtime adapters & profile-based surfacing (--profile core|build|review|ship|all)",
        ),
        (
            198,
            "#38bdf8",
            "TIER 2 // LIFECYCLE HOOKS & CONTEXT GUARDS (scripts/hooks/)",
            "context_guard.py (70% / 50-step / 12-turn cadence / 30m idle cache / PreCompact block)   •   model_router.py   •   git_pre_commit.py",
            "Deterministic Python stdlib interceptors protecting context windows, model budgets & git history",
        ),
        (
            286,
            "#00ff9d",
            "TIER 3 // TASK SIZING & /eng ROUTING ENGINE",
            "Scale Classifier (Tool <=1d  |  App days  |  System multi-service)   ->   Bounded Active Set (1-3 skills max, phase eviction)",
            "Eliminates prompt replay bloat by loading only active-phase domain judgment",
        ),
        (
            374,
            "#00e5ff",
            f"TIER 4 // EVIDENCE-DERIVED DOMAIN SKILL LIBRARY ({skill_count} SKILLS)",
            "Frame & Plan (9)  •  Architecture & Tri-OS Drivers (12)  •  AI Loops (2)  •  Build & Local CI (14)  •  Verify & Browser QA (9)  •  Sustain & Docs (20)",
            "Distilled from concrete post-mortems across 20+ production repositories (<=500-word target per skill)",
        ),
        (
            462,
            "#a855f7",
            "TIER 5 // SUBAGENT LOG ISOLATION & HIERARCHICAL VERIFICATION",
            "Primary Orchestrator (pro / Sonnet)  --delegates noisy build/test loops-->  Ephemeral Worker (flash / Haiku)  +  scripts/verify.sh (8 tiers)",
            "Quarantines compiler/test stdout inside throwaway workers; returns <=10-line verified diff summary",
        ),
    ]
    boxes = []
    for idx, (y, color, heading, line1, line2) in enumerate(tiers):
        boxes.append(
            f'  <rect x="64" y="{y}" width="1072" height="72" rx="8" fill="url(#panel-grad)" stroke="{color}" stroke-width="1.8" />'
            f'  <rect x="64" y="{y}" width="8" height="72" rx="4" fill="{color}" />'
            f'  <text x="90" y="{y+24}" class="f-mono" font-size="14" font-weight="700" fill="{color}">{esc(heading)}</text>'
            f'  <text x="90" y="{y+45}" class="f-mono" font-size="12.5" fill="#f0f6fc">{esc(line1)}</text>'
            f'  <text x="90" y="{y+63}" class="f-sans" font-size="12.5" fill="#94a3b8">{esc(line2)}</text>'
        )
        if idx < len(tiers) - 1:
            ny = y + 72
            boxes.append(
                f'  <line x1="600" y1="{ny}" x2="600" y2="{ny+16}" stroke="#00e5ff" stroke-width="2" />'
                f'  <polygon points="594,{ny+11} 606,{ny+11} 600,{ny+17}" fill="#00ff9d" />'
            )

    return card_frame(
        w,
        h,
        "ARCHITECTURE",
        "5-Tier Runtime Engineering Governance Architecture",
        f"Ambient control plane across Claude Code, Antigravity (agy), and Cursor — {skill_count} modular skills + lifecycle guards",
        "\n".join(boxes),
        "SOURCE: docs/architecture.md  •  scripts/hooks/context_guard.py",
        "VERIFIED: agy plugin validate . -> PASS",
    )


def build_workflow_eng_routing_svg() -> str:
    w, h = 1200, 620
    body = f"""
  <!-- Step 1: User Input -->
  <rect x="52" y="116" width="330" height="175" rx="10" fill="url(#panel-grad)" stroke="#00e5ff" stroke-width="1.8" />
  <text x="72" y="144" class="f-mono" font-size="13" font-weight="700" fill="#00e5ff">{esc("1. /ENG ENTRY & SIZING")}</text>
  <rect x="72" y="158" width="290" height="44" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1" />
  <text x="84" y="177" class="f-mono" font-size="12" fill="#00ff9d">$ /eng add rate-limiter to</text>
  <text x="84" y="194" class="f-mono" font-size="12" fill="#f0f6fc">  POST /v1/auth/tokens</text>
  <text x="72" y="226" class="f-mono" font-size="12.5" fill="#38bdf8">• Scale Detected: APP (multi-module)</text>
  <text x="72" y="248" class="f-mono" font-size="12.5" fill="#f0f6fc">• Active Set Cap: 3 skills loaded</text>
  <text x="72" y="270" class="f-mono" font-size="12" fill="#94a3b8">• Token Overhead: ~420 tok (vs 3,050)</text>

  <!-- Arrow 1->2 -->
  <path d="M 382 203 L 430 203" stroke="#00e5ff" stroke-width="2.5" />
  <polygon points="426,197 438,203 426,209" fill="#00ff9d" />

  <!-- Step 2: Selected Skills -->
  <rect x="440" y="116" width="330" height="175" rx="10" fill="url(#panel-grad)" stroke="#00ff9d" stroke-width="1.8" />
  <text x="460" y="144" class="f-mono" font-size="13" font-weight="700" fill="#00ff9d">2. BOUNDED SKILL DISPATCH</text>
  <rect x="460" y="160" width="290" height="32" rx="5" fill="#071936" stroke="#00e5ff" stroke-width="1.2" />
  <text x="474" y="181" class="f-mono" font-size="12.5" fill="#f0f6fc">1. planning-with-contracts</text>
  <rect x="460" y="200" width="290" height="32" rx="5" fill="#071936" stroke="#00ff9d" stroke-width="1.2" />
  <text x="474" y="221" class="f-mono" font-size="12.5" fill="#f0f6fc">2. designing-exhaustive-test-cases</text>
  <rect x="460" y="240" width="290" height="32" rx="5" fill="#071936" stroke="#38bdf8" stroke-width="1.2" />
  <text x="474" y="261" class="f-mono" font-size="12.5" fill="#f0f6fc">3. security-best-practices</text>

  <!-- Arrow 2->3 -->
  <path d="M 770 203 L 818 203" stroke="#00e5ff" stroke-width="2.5" />
  <polygon points="814,197 826,203 814,209" fill="#00ff9d" />

  <!-- Step 3: Pre-Build RED Matrix -->
  <rect x="828" y="116" width="320" height="175" rx="10" fill="url(#panel-grad)" stroke="#38bdf8" stroke-width="1.8" />
  <text x="848" y="144" class="f-mono" font-size="13" font-weight="700" fill="#38bdf8">3. 6-DIM PRE-BUILD MATRIX</text>
  <text x="848" y="170" class="f-mono" font-size="12" fill="#f0f6fc">{esc("[✓] D1 Happy Path & Contract")}</text>
  <text x="848" y="190" class="f-mono" font-size="12" fill="#f0f6fc">{esc("[✓] D2 Boundary (0, 1, N, N+1)")}</text>
  <text x="848" y="210" class="f-mono" font-size="12" fill="#f0f6fc">{esc("[✓] D3 Malformed & Adversarial")}</text>
  <text x="848" y="230" class="f-mono" font-size="12" fill="#f0f6fc">{esc("[✓] D4 Concurrency & Idempotency")}</text>
  <text x="848" y="250" class="f-mono" font-size="12" fill="#f0f6fc">{esc("[✓] D5 Dependency Timeout Fakes")}</text>
  <text x="848" y="270" class="f-mono" font-size="12" fill="#00ff9d">{esc("[✓] D6 Wired into scripts/verify.sh")}</text>

  <!-- Bottom Wide Panel: 8-Tier Verification Runner -->
  <rect x="52" y="322" width="1096" height="218" rx="10" fill="url(#panel-grad)" stroke="#00e5ff" stroke-width="1.8" />
  <text x="76" y="352" class="f-mono" font-size="14" font-weight="700" fill="#00e5ff">4. HIERARCHICAL POST-BUILD VERIFICATION GATE (scripts/verify.sh --quick / --tier)</text>

  <g class="f-mono" font-size="11.5">
    <rect x="76"  y="370" width="122" height="58" rx="6" fill="#06152d" stroke="#00ff9d" stroke-width="1.4" />
    <text x="137" y="394" text-anchor="middle" fill="#00ff9d" font-weight="700">1. SMOKE</text>
    <text x="137" y="414" text-anchor="middle" fill="#94a3b8">{esc("<10s sanity")}</text>

    <rect x="210" y="370" width="122" height="58" rx="6" fill="#06152d" stroke="#00ff9d" stroke-width="1.4" />
    <text x="271" y="394" text-anchor="middle" fill="#00ff9d" font-weight="700">2. UNIT</text>
    <text x="271" y="414" text-anchor="middle" fill="#94a3b8">Pure logic</text>

    <rect x="344" y="370" width="122" height="58" rx="6" fill="#06152d" stroke="#00ff9d" stroke-width="1.4" />
    <text x="405" y="394" text-anchor="middle" fill="#00ff9d" font-weight="700">3. INTEGR.</text>
    <text x="405" y="414" text-anchor="middle" fill="#94a3b8">DB / IPC seams</text>

    <rect x="478" y="370" width="122" height="58" rx="6" fill="#06152d" stroke="#00e5ff" stroke-width="1.4" />
    <text x="539" y="394" text-anchor="middle" fill="#00e5ff" font-weight="700">4. SYSTEM</text>
    <text x="539" y="414" text-anchor="middle" fill="#94a3b8">Full E2E CLI/UI</text>

    <rect x="612" y="370" width="122" height="58" rx="6" fill="#06152d" stroke="#38bdf8" stroke-width="1.4" />
    <text x="673" y="394" text-anchor="middle" fill="#38bdf8" font-weight="700">5. PERF</text>
    <text x="673" y="414" text-anchor="middle" fill="#94a3b8">{esc("p95 & allocs")}</text>

    <rect x="746" y="370" width="122" height="58" rx="6" fill="#06152d" stroke="#38bdf8" stroke-width="1.4" />
    <text x="807" y="394" text-anchor="middle" fill="#38bdf8" font-weight="700">6. STRESS</text>
    <text x="807" y="414" text-anchor="middle" fill="#94a3b8">Contention</text>

    <rect x="880" y="370" width="122" height="58" rx="6" fill="#06152d" stroke="#a855f7" stroke-width="1.4" />
    <text x="941" y="394" text-anchor="middle" fill="#a855f7" font-weight="700">7. TORTURE</text>
    <text x="941" y="414" text-anchor="middle" fill="#94a3b8">Kill -9 / fault</text>

    <rect x="1014" y="370" width="112" height="58" rx="6" fill="#06152d" stroke="#00ff9d" stroke-width="1.4" />
    <text x="1070" y="394" text-anchor="middle" fill="#00ff9d" font-weight="700">8. SECURITY</text>
    <text x="1070" y="414" text-anchor="middle" fill="#94a3b8">OWASP / CVE</text>
  </g>

  <!-- Terminal Output Strip -->
  <rect x="76" y="446" width="1050" height="72" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="96" y="472" class="f-mono" font-size="13" fill="#00e5ff">$ scripts/verify.sh --quick</text>
  <text x="96" y="498" class="f-mono" font-size="13" fill="#00ff9d">PASS  smoke(0.4s)  unit(1.2s)  integration(2.1s)  security(0.8s)  |  0 failed  |  report: target/verify/report.md</text>
"""
    return card_frame(
        w,
        h,
        "EXAMPLE 01 // ROUTING & TDD",
        "/eng Dispatch, Bounded Skill Set & 8-Tier Verification Matrix",
        "How /eng sizes a task, loads 1-3 skills, designs pre-build RED tests, and gates post-build completion",
        body,
        "SKILLS: using-swe-skills • designing-exhaustive-test-cases • layered-verification-gates",
        "TOKEN SAVINGS: -85% CATALOG OVERHEAD",
    )


def build_workflow_subagent_isolation_svg() -> str:
    w, h = 1200, 620
    body = f"""
  <!-- Left: Primary Orchestrator -->
  <rect x="52" y="118" width="480" height="418" rx="10" fill="url(#panel-grad)" stroke="#00e5ff" stroke-width="1.8" />
  <text x="76" y="148" class="f-mono" font-size="14" font-weight="700" fill="#00e5ff">PRIMARY ORCHESTRATOR SESSION (pro / Sonnet)</text>
  <text x="76" y="172" class="f-sans" font-size="13" fill="#94a3b8">{esc("Holds architectural invariants, contracts & user intent only")}</text>

  <rect x="76" y="192" width="432" height="96" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="92" y="216" class="f-mono" font-size="12" fill="#38bdf8">{esc("// PreToolUse Hook -> model_router.py")}</text>
  <text x="92" y="238" class="f-mono" font-size="12.5" fill="#f0f6fc">invoke_subagent({{</text>
  <text x="92" y="258" class="f-mono" font-size="12.5" fill="#00ff9d">  Role: "Test Runner", Model: "flash",</text>
  <text x="92" y="276" class="f-mono" font-size="12.5" fill="#f0f6fc">{esc('  Prompt: "Run cargo test -q & fix limiter.rs"')}</text>

  <rect x="76" y="310" width="432" height="110" rx="6" fill="#06192e" stroke="#00ff9d" stroke-width="1.5" />
  <text x="92" y="335" class="f-mono" font-size="12.5" font-weight="700" fill="#00ff9d">{esc("RETURNED TO PRIMARY CONTEXT (<=10 LINES):")}</text>
  <text x="92" y="360" class="f-mono" font-size="12.5" fill="#f0f6fc">Status: PASS (74/74 tests, 0 warnings in 1.8s)</text>
  <text x="92" y="382" class="f-mono" font-size="12.5" fill="#38bdf8">Modified: src/limiter.rs (+6, -2)</text>
  <text x="92" y="404" class="f-mono" font-size="12" fill="#94a3b8">Context Growth: +180 tokens (vs +18,400 raw stdout)</text>

  <rect x="76" y="440" width="432" height="72" rx="6" fill="#071328" stroke="#00e5ff" stroke-width="1.2" />
  <text x="92" y="466" class="f-mono" font-size="12.5" font-weight="700" fill="#00e5ff">FINOPS IMPACT (token-finops):</text>
  <text x="92" y="492" class="f-mono" font-size="12" fill="#00ff9d">• 0 KB compiler noise replayed across subsequent turns</text>

  <!-- Center Quarantine Firewall -->
  <line x1="598" y1="120" x2="598" y2="534" stroke="#ff2a85" stroke-width="2" stroke-dasharray="8 6" />
  <rect x="556" y="294" width="84" height="56" rx="6" fill="#1a081e" stroke="#ff2a85" stroke-width="1.6" />
  <text x="598" y="318" text-anchor="middle" class="f-mono" font-size="11" font-weight="700" fill="#ff2a85">LOG</text>
  <text x="598" y="336" text-anchor="middle" class="f-mono" font-size="11" font-weight="700" fill="#ff2a85">FIREWALL</text>

  <!-- Right: Ephemeral Worker Subagent -->
  <rect x="664" y="118" width="484" height="418" rx="10" fill="url(#panel-grad)" stroke="#38bdf8" stroke-width="1.8" />
  <text x="688" y="148" class="f-mono" font-size="14" font-weight="700" fill="#38bdf8">EPHEMERAL WORKER SUBAGENT (flash / Haiku)</text>
  <text x="688" y="172" class="f-sans" font-size="13" fill="#94a3b8">{esc("Absorbs verbose compiler & test retry loops in isolated scratch context")}</text>

  <rect x="688" y="192" width="436" height="228" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="704" y="218" class="f-mono" font-size="12" fill="#94a3b8">$ cargo test -q</text>
  <text x="704" y="240" class="f-mono" font-size="12" fill="#ff2a85">error[E0308]: mismatched types in src/limiter.rs:42</text>
  <text x="704" y="262" class="f-mono" font-size="12" fill="#94a3b8">{esc("  --> [420 lines of rustc backtrace quarantined here]")}</text>
  <text x="704" y="290" class="f-mono" font-size="12" fill="#38bdf8">{esc("// Worker applies atomic fix & re-runs gate")}</text>
  <text x="704" y="314" class="f-mono" font-size="12" fill="#94a3b8">$ cargo test -q</text>
  <text x="704" y="336" class="f-mono" font-size="12" fill="#00ff9d">running 74 tests ... test result: ok. 74 passed; 0 failed</text>
  <text x="704" y="366" class="f-mono" font-size="12" fill="#ffb800">[Scratch context discarded upon subagent completion]</text>
  <text x="704" y="392" class="f-mono" font-size="12" fill="#00e5ff">{esc("-> Emits compact 4-line summary across boundary")}</text>

  <rect x="688" y="440" width="436" height="72" rx="6" fill="#071328" stroke="#38bdf8" stroke-width="1.2" />
  <text x="704" y="466" class="f-mono" font-size="12.5" font-weight="700" fill="#38bdf8">ADAPTIVE MODEL ROUTING (model_router.py):</text>
  <text x="704" y="492" class="f-mono" font-size="11.5" fill="#f0f6fc">{esc("• Mechanical test/lint loops -> flash  |  Security/Arch -> pro")}</text>
"""
    return card_frame(
        w,
        h,
        "EXAMPLE 02 // LOG ISOLATION",
        "Subagent Log Isolation & Adaptive Model Routing",
        "Quarantining noisy compiler/test loops inside cheap worker subagents to keep the primary context crystal-clear",
        body,
        "SKILLS: orchestrating-subagents • adaptive-model-routing • token-finops",
        "REPLAY REDUCTION: -99% LOG TOKENS",
    )


def build_workflow_session_chaining_svg() -> str:
    w, h = 1200, 620
    steps = [
        (56, "STEP 1", "CHECKPOINT", "#00e5ff", ["Write verified state", "to docs/CHECKPOINT.md", "every 12 turns / 25 steps", "or at 70% context cap"]),
        (276, "STEP 2", "PRECOMPACT", "#00ff9d", ["context_guard.py checks", "checkpoint age < 20m;", "blocks unsafe /compact", "(exit code 2 if stale)"]),
        (496, "STEP 3", "COMPACT", "#38bdf8", ["Run /compact with", "focus notes keeping", "goal, decisions, diffs", "& next verify command"]),
        (716, "STEP 4", "HANDOFF", "#a855f7", ["Write docs/HANDOFF.md", "with dead-ends, lessons", "& exact next command", "then /clear or /exit"]),
        (936, "STEP 5", "AUTO-RESUME", "#00ff9d", ["SessionStart hook or", "chain-session.sh injects", "checkpoint & verifies", "git status before edits"]),
    ]
    cards = []
    for idx, (x, badge, title, color, lines) in enumerate(steps):
        t_lines = "\n".join(
            f'  <text x="{x+18}" y="{220 + i*22}" class="f-mono" font-size="11.8" fill="#e2e8f0">{esc(line)}</text>'
            for i, line in enumerate(lines)
        )
        cards.append(
            f'  <rect x="{x}" y="122" width="204" height="196" rx="10" fill="url(#panel-grad)" stroke="{color}" stroke-width="1.8" />\n'
            f'  <text x="{x+18}" y="150" class="f-mono" font-size="11.5" font-weight="700" fill="{color}">{esc(badge)}</text>\n'
            f'  <text x="{x+18}" y="176" class="f-sans" font-size="17" font-weight="800" fill="#f0f6fc">{esc(title)}</text>\n'
            f'  <line x1="{x+18}" y1="190" x2="{x+186}" y2="190" stroke="{color}" stroke-width="1" stroke-opacity="0.5" />\n'
            f"{t_lines}"
        )
        if idx < len(steps) - 1:
            ax = x + 204
            cards.append(
                f'  <line x1="{ax}" y1="220" x2="{ax+16}" y2="220" stroke="#00e5ff" stroke-width="2.2" />\n'
                f'  <polygon points="{ax+11},215 {ax+18},220 {ax+11},225" fill="#00ff9d" />'
            )

    bottom = f"""
  <!-- Dual Trigger Telemetry Panel -->
  <rect x="56" y="346" width="1084" height="190" rx="10" fill="url(#panel-grad)" stroke="#00e5ff" stroke-width="1.8" />
  <text x="80" y="376" class="f-mono" font-size="14" font-weight="700" fill="#00e5ff">{esc("DUAL-TRIGGER CADENCE & CLI DIAGNOSTIC (context_guard.py report & scripts/chain-session.sh)")}</text>

  <rect x="80" y="394" width="505" height="122" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="98" y="418" class="f-mono" font-size="12" fill="#00ff9d">$ python3 scripts/hooks/context_guard.py report</text>
  <text x="98" y="440" class="f-mono" font-size="12" fill="#f0f6fc">context: 42.1% (~84,200 / 200,000 tokens) · turns: 12</text>
  <text x="98" y="462" class="f-mono" font-size="12" fill="#ffb800">recommendation: CHECKPOINT_DUE (cadence: 12 turns reached)</text>
  <text x="98" y="484" class="f-mono" font-size="12" fill="#38bdf8">hooks: claude=installed · agy=installed</text>
  <text x="98" y="504" class="f-mono" font-size="12" fill="#00ff9d">checkpoint: docs/CHECKPOINT.md (fresh, 2m ago)</text>

  <rect x="610" y="394" width="506" height="122" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="628" y="418" class="f-mono" font-size="12" fill="#00e5ff">$ scripts/chain-session.sh --claude</text>
  <text x="628" y="440" class="f-mono" font-size="12" fill="#f0f6fc">[chain] Iteration 1/5 — resuming from docs/HANDOFF.md</text>
  <text x="628" y="462" class="f-mono" font-size="12" fill="#94a3b8">{esc("[chain] Verifying git status & baseline tests...")}</text>
  <text x="628" y="484" class="f-mono" font-size="12" fill="#00ff9d">[chain] Status: COMPLETE detected in docs/CHECKPOINT.md</text>
  <text x="628" y="504" class="f-mono" font-size="12" fill="#00ff9d">{esc("[chain] All phases verified & committed cleanly.")}</text>
"""
    return card_frame(
        w,
        h,
        "EXAMPLE 03 // CONTEXT GUARD",
        "Periodic Cadence Hooks & 5-Step Lossless Session Chaining",
        "Automated turn/step cadence reminders, PreCompact blocking, and zero-loss multi-session chaining",
        "\n".join(cards) + bottom,
        "SKILLS: compacting-context-safely • handing-off-sessions",
        "HOOKS: UserPromptSubmit • PreInvocation • PreCompact • SessionStart",
    )


def build_workflow_browser_qa_tri_os_svg() -> str:
    w, h = 1200, 620
    body = f"""
  <!-- Left Panel: Browser QA Driver -->
  <rect x="52" y="118" width="532" height="418" rx="10" fill="url(#panel-grad)" stroke="#00e5ff" stroke-width="1.8" />
  <text x="76" y="148" class="f-mono" font-size="14" font-weight="700" fill="#00e5ff">AUTOMATED BROWSER QA (driving-browsers-for-qa)</text>
  <text x="76" y="172" class="f-sans" font-size="13" fill="#94a3b8">Playwright / WebDriver BiDi against live stack with zero-tolerance listeners</text>

  <rect x="76" y="192" width="484" height="145" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="94" y="216" class="f-mono" font-size="12" fill="#00ff9d">// Attached to every QA plan step (plan-steps.e2e.ts)</text>
  <text x="94" y="238" class="f-mono" font-size="12" fill="#f0f6fc">{esc("page.on('pageerror', err => failures.push(err));")}</text>
  <text x="94" y="260" class="f-mono" font-size="12" fill="#f0f6fc">{esc("page.on('console', msg => msg.type()==='error' && ...);")}</text>
  <text x="94" y="282" class="f-mono" font-size="12" fill="#f0f6fc">{esc("page.on('response', r => r.status()>=500 && ...);")}</text>
  <text x="94" y="306" class="f-mono" font-size="12" fill="#38bdf8">trace: 'retain-on-failure'  |  screenshot: 'on'</text>
  <text x="94" y="325" class="f-mono" font-size="12" fill="#00ff9d">output: QA-REPORT.md + trace.zip + step screenshots</text>

  <rect x="76" y="355" width="484" height="158" rx="6" fill="#06152d" stroke="#00ff9d" stroke-width="1.4" />
  <text x="94" y="382" class="f-mono" font-size="12.5" font-weight="700" fill="#00ff9d">LIVE QA VERIFICATION REPORT SUMMARY:</text>
  <text x="94" y="406" class="f-mono" font-size="12" fill="#f0f6fc">{esc("Step 01: Auth Login & Session Cookie    [PASS] 180ms")}</text>
  <text x="94" y="428" class="f-mono" font-size="12" fill="#f0f6fc">Step 02: Create Rate-Limited API Key    [PASS] 240ms</text>
  <text x="94" y="450" class="f-mono" font-size="12" fill="#f0f6fc">Step 03: Console/PageError/5xx Gate     [0 ERRORS]</text>
  <text x="94" y="472" class="f-mono" font-size="12" fill="#38bdf8">Evidence: test-results/step-02/trace.zip</text>
  <text x="94" y="496" class="f-mono" font-size="12" fill="#00e5ff">Shortcut: /eng qa-drive  |  /eng qa-report</text>

  <!-- Right Panel: Tri-OS Driver Architecture -->
  <rect x="616" y="118" width="532" height="418" rx="10" fill="url(#panel-grad)" stroke="#38bdf8" stroke-width="1.8" />
  <text x="640" y="148" class="f-mono" font-size="14" font-weight="700" fill="#38bdf8">TRI-OS DRIVER CONTRACTS (designing-plugin-contracts)</text>
  <text x="640" y="172" class="f-sans" font-size="13" fill="#94a3b8">Host code speaks one OS-agnostic trait; platform seams isolate syscalls</text>

  <g class="f-mono" font-size="12">
    <rect x="640" y="192" width="152" height="136" rx="6" fill="#06152d" stroke="#00e5ff" stroke-width="1.4" />
    <text x="716" y="216" text-anchor="middle" font-weight="700" fill="#00e5ff">WINDOWS</text>
    <text x="652" y="240" fill="#e2e8f0">• ConPTY</text>
    <text x="652" y="260" fill="#e2e8f0">• Job Objects</text>
    <text x="652" y="280" fill="#e2e8f0">• Named Pipes</text>
    <text x="652" y="300" fill="#e2e8f0">• MoveFileExW</text>
    <text x="652" y="318" fill="#94a3b8">• %APPDATA%</text>

    <rect x="806" y="192" width="152" height="136" rx="6" fill="#06152d" stroke="#00ff9d" stroke-width="1.4" />
    <text x="882" y="216" text-anchor="middle" font-weight="700" fill="#00ff9d">macOS</text>
    <text x="818" y="240" fill="#e2e8f0">• POSIX openpty</text>
    <text x="818" y="260" fill="#e2e8f0">• killpg / kqueue</text>
    <text x="818" y="280" fill="#e2e8f0">{esc("• Unix Sock <104B")}</text>
    <text x="818" y="300" fill="#e2e8f0">• FSEvents</text>
    <text x="818" y="318" fill="#94a3b8">• ~/Library/...</text>

    <rect x="972" y="192" width="152" height="136" rx="6" fill="#06152d" stroke="#38bdf8" stroke-width="1.4" />
    <text x="1048" y="216" text-anchor="middle" font-weight="700" fill="#38bdf8">LINUX</text>
    <text x="984" y="240" fill="#e2e8f0">• openpty / epoll</text>
    <text x="984" y="260" fill="#e2e8f0">• PR_SET_PDEATHSIG</text>
    <text x="984" y="280" fill="#e2e8f0">{esc("• Unix Sock <108B")}</text>
    <text x="984" y="300" fill="#e2e8f0">• inotify / rename</text>
    <text x="984" y="318" fill="#94a3b8">• $XDG_STATE_HOME</text>
  </g>

  <rect x="640" y="355" width="484" height="158" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="658" y="382" class="f-mono" font-size="12.5" font-weight="700" fill="#00e5ff">SHARED CONTRACT SUITE + INJECTED SYSCALL FAKES:</text>
  <text x="658" y="406" class="f-mono" font-size="12" fill="#f0f6fc">{esc("run_driver_contract_suite(driver) -> runs on all 3 OSes")}</text>
  <text x="658" y="428" class="f-mono" font-size="12" fill="#f0f6fc">test-coverage audits #[cfg(windows/macos/linux)] branches</text>
  <text x="658" y="450" class="f-mono" font-size="12" fill="#00ff9d">verify.sh.template: Bash 3.2 + Git Bash + macOS + Linux</text>
  <text x="658" y="472" class="f-mono" font-size="12" fill="#38bdf8">llvm-cov / pytest-cov / vitest / coverlet merged reports</text>
  <text x="658" y="496" class="f-mono" font-size="12" fill="#00e5ff">Shortcut: /eng driver  |  /eng cov</text>
"""
    return card_frame(
        w,
        h,
        "EXAMPLE 04 // QA & TRI-OS DRIVERS",
        "Browser QA Automation & Cross-Platform Tri-OS Driver Architecture",
        "End-to-end browser verification with recorded evidence alongside Windows, macOS, and Linux driver parity",
        body,
        "SKILLS: driving-browsers-for-qa • designing-plugin-contracts • test-coverage",
        "PLATFORMS: WINDOWS • MACOS • LINUX • CHROMIUM/WEBKIT/FIREFOX",
    )


def build_workflow_local_tools_and_ci_svg() -> str:
    w, h = 1200, 620
    body = f"""
  <!-- Left Panel: Local Tool Registry & VMs -->
  <rect x="52" y="118" width="532" height="418" rx="10" fill="url(#panel-grad)" stroke="#00e5ff" stroke-width="1.8" />
  <text x="76" y="148" class="f-mono" font-size="14" font-weight="700" fill="#00e5ff">LOCAL TOOL REGISTRY (using-local-tool-registry)</text>
  <text x="76" y="172" class="f-sans" font-size="13" fill="#94a3b8">Centralized ~/src scanner, updater &amp; lifecycle recommender (111+ local tools)</text>

  <rect x="76" y="190" width="484" height="92" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="94" y="214" class="f-mono" font-size="12" fill="#00ff9d">$ python3 scripts/tool-registry.py update</text>
  <text x="94" y="236" class="f-mono" font-size="12" fill="#00e5ff">$ python3 scripts/tool-registry.py recommend --task "windows + ci"</text>
  <text x="94" y="258" class="f-mono" font-size="12" fill="#f0f6fc">• gha-vm-runners [READY]  • win-devvm [READY]  • cvm [READY]</text>

  <g class="f-mono" font-size="11.2">
    <rect x="76" y="298" width="484" height="52" rx="6" fill="#06152d" stroke="#00ff9d" stroke-width="1.3" />
    <text x="92" y="320" font-weight="700" fill="#00ff9d">cvm (~/src/ai/projects/cvm)</text>
    <text x="92" y="339" fill="#cbd5e1">13 VM/container backends (KVM, Firecracker, Apple VZ) + COW snapshots</text>

    <rect x="76" y="360" width="484" height="52" rx="6" fill="#06152d" stroke="#00e5ff" stroke-width="1.3" />
    <text x="92" y="382" font-weight="700" fill="#00e5ff">win-devvm (~/src/infra/win-devvm)</text>
    <text x="92" y="401" fill="#cbd5e1">{esc("Unattended Windows 11 x64 (KVM) & ARM64 (Parallels) + MSVC & SSH")}</text>

    <rect x="76" y="422" width="484" height="52" rx="6" fill="#06152d" stroke="#38bdf8" stroke-width="1.3" />
    <text x="92" y="444" font-weight="700" fill="#38bdf8">{esc("fedora-vms & freebsd-kvm (~/src/infra/fedora-vms · ~/src/vms)")}</text>
    <text x="92" y="463" fill="#cbd5e1">{esc("Fedora RPM/SELinux & FreeBSD 15.x kqueue/bhyve KVM guest verification")}</text>

    <text x="76" y="502" fill="#00e5ff">Shortcuts: /eng tools  |  /eng vms  |  /eng registry</text>
  </g>

  <!-- Right Panel: Local-First CI & Quota Conservation -->
  <rect x="616" y="118" width="532" height="418" rx="10" fill="url(#panel-grad)" stroke="#00ff9d" stroke-width="1.8" />
  <text x="640" y="148" class="f-mono" font-size="14" font-weight="700" fill="#00ff9d">STANDING RULE: LOCAL CI FIRST (running-local-ci)</text>
  <text x="640" y="172" class="f-sans" font-size="13" fill="#94a3b8">Conserve hosted GitHub Actions minutes unless explicitly overridden by user</text>

  <rect x="640" y="190" width="484" height="154" rx="6" fill="#040812" stroke="#0284c7" stroke-width="1.2" />
  <text x="658" y="214" class="f-mono" font-size="12" fill="#00ff9d">$ ~/src/gha-vm-runners/local-ci.sh ~/src/flowscope</text>
  <text x="658" y="236" class="f-mono" font-size="11.5" fill="#f0f6fc">[local-ci] Running workflow mirror on workstation (0 GHA min)...</text>
  <text x="658" y="258" class="f-mono" font-size="11.5" fill="#00ff9d">[local-ci] fmt: PASS  clippy: PASS  test: PASS  sarif: PASS</text>
  <text x="658" y="284" class="f-mono" font-size="12" fill="#38bdf8">$ ~/src/gha-vm-runners/gha-vm-runners.sh start</text>
  <text x="658" y="306" class="f-mono" font-size="11.5" fill="#cbd5e1">[kvm-runner] Disposable Ubuntu 24.04 KVM runner online</text>
  <text x="658" y="328" class="f-mono" font-size="12" fill="#00ff9d">Hosted GitHub Actions Minutes Burned: 0.0 min</text>

  <rect x="640" y="360" width="484" height="152" rx="6" fill="#06152d" stroke="#00e5ff" stroke-width="1.4" />
  <text x="658" y="386" class="f-mono" font-size="12.5" font-weight="700" fill="#00e5ff">QUOTA-CONSERVING WORKFLOW DISCIPLINE:</text>
  <text x="658" y="410" class="f-mono" font-size="12" fill="#f0f6fc">1. Run scripts/verify.sh + local-ci.sh + local VMs before push</text>
  <text x="658" y="432" class="f-mono" font-size="12" fill="#f0f6fc">2. Never push WIP commits just to test in remote GitHub Actions</text>
  <text x="658" y="454" class="f-mono" font-size="12" fill="#f0f6fc">3. Set concurrency cancel-in-progress: true &amp; timeout-minutes</text>
  <text x="658" y="476" class="f-mono" font-size="12" fill="#00ff9d">4. Gate heavy multi-OS matrices to release tags (v*) or dispatch</text>
  <text x="658" y="498" class="f-mono" font-size="12" fill="#00e5ff">Shortcuts: /eng local-ci  |  /eng ci</text>
"""
    return card_frame(
        w,
        h,
        "EXAMPLE 05 // TOOLS & LOCAL CI",
        "Searchable Local Tool Registry, VM Sandboxes & Zero-Minute Local CI",
        "Discovering ~/src VMs (cvm, win-devvm, gha-vm-runners) and enforcing local-first CI to conserve GitHub Actions quota",
        body,
        "SKILLS: using-local-tool-registry • running-local-ci • hardening-ci-workflows",
        "HOSTED GHA MINUTES SAVED: 100% ON ROUTINE DEV",
    )


def svg_to_png(svg_path: Path, png_path: Path, width: int) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("inkscape"):
        subprocess.run(
            [
                "inkscape",
                str(svg_path),
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-width={width}",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return
    if shutil.which("rsvg-convert"):
        subprocess.run(
            ["rsvg-convert", "-w", str(width), "-o", str(png_path), str(svg_path)],
            check=True,
        )
        return
    if shutil.which("magick"):
        subprocess.run(
            ["magick", "-background", "none", str(svg_path), "-resize", f"{width}x", str(png_path)],
            check=True,
        )
        return
    raise RuntimeError("No SVG-to-PNG converter found (inkscape, rsvg-convert, or magick required)")


def write_and_render(svg_path: Path, png_path: Path, content: str, png_width: int) -> None:
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(content, encoding="utf-8")
    svg_to_png(svg_path, png_path, png_width)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render deterministic SVG and PNG graphics for swe-skills.")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress per-file progress output")
    args = parser.parse_args()

    version, skill_count = get_metadata()

    # 1. Square icon (assets/logo.{svg,png} and docs/assets/icon.{svg,png})
    square_svg = build_square_icon_svg()
    write_and_render(ROOT_ASSETS / "logo.svg", ROOT_ASSETS / "logo.png", square_svg, 512)
    write_and_render(DOCS_ASSETS / "icon.svg", DOCS_ASSETS / "icon.png", square_svg, 512)

    # 2. Wide Hero Logo Banner (docs/assets/logo.{svg,png})
    hero_svg = build_hero_logo_svg(version, skill_count)
    write_and_render(DOCS_ASSETS / "logo.svg", DOCS_ASSETS / "logo.png", hero_svg, 1600)

    # 3. Category Icons (docs/assets/icons/icon-*.{svg,png})
    for kind in ("entry", "plan", "arch", "build", "verify", "sustain"):
        icon_svg = build_category_icon_svg(kind)
        write_and_render(ICONS_DIR / f"icon-{kind}.svg", ICONS_DIR / f"icon-{kind}.png", icon_svg, 256)

    # 4. Graphic Examples (docs/assets/examples/*.{svg,png})
    examples = {
        "architecture-overview": build_architecture_overview_svg(skill_count),
        "workflow-eng-routing": build_workflow_eng_routing_svg(),
        "workflow-subagent-isolation": build_workflow_subagent_isolation_svg(),
        "workflow-session-chaining": build_workflow_session_chaining_svg(),
        "workflow-browser-qa-tri-os": build_workflow_browser_qa_tri_os_svg(),
        "workflow-local-tools-and-ci": build_workflow_local_tools_and_ci_svg(),
    }
    for name, content in examples.items():
        write_and_render(EXAMPLES_DIR / f"{name}.svg", EXAMPLES_DIR / f"{name}.png", content, 1600)

    if not args.quiet:
        print(f"Rendered 15 SVG + 15 PNG assets for swe-skills v{version} ({skill_count} skills).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
