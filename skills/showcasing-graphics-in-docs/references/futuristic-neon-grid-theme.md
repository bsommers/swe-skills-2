# Futuristic Obsidian-Black & Light-Blue Neon Grid Theme Reference

## 1. Color Tokens

| Token | Hex | Usage |
|---|---|---|
| `--bg-void` | `#050811` | Outer canvas & deep background |
| `--bg-core` | `#080e1e` | Radial center gradient & card base |
| `--bg-panel` | `#0b1428` | Inner HUD panel fill (`opacity="0.92"`) |
| `--neon-cyan` | `#00e5ff` | Primary neon grid, active borders, HUD reticles, highlights |
| `--neon-blue` | `#38bdf8` | Secondary grid, accents, badges, connectors |
| `--neon-deep` | `#0284c7` | Outer glow, structural dividers, secondary frames |
| `--neon-emerald` | `#00ff9d` | Verification PASS badges, green test gates |
| `--neon-amber` | `#ffb800` | Cadence nudges, warning thresholds |
| `--neon-magenta` | `#ff2a85` | Blocked gates, security boundary alerts |
| `--text-bright` | `#f0f6fc` | Primary titles and node headers |
| `--text-muted` | `#94a3b8` | Subtitles, annotations, axis labels |

## 2. Reusable SVG `<defs>` Block (Neon Grid + Glow Filters)

Include this `<defs>` block in generated SVGs (`rendering-graphic-examples`, `designing-logos-and-icons`) to render the obsidian canvas, dual-scale light-blue neon grid, and cyan glow:

```xml
<defs>
  <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#04070f" />
    <stop offset="50%" stop-color="#081022" />
    <stop offset="100%" stop-color="#040814" />
  </linearGradient>
  <radialGradient id="core-glow" cx="50%" cy="45%" r="55%">
    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.16" />
    <stop offset="60%" stop-color="#0284c7" stop-opacity="0.05" />
    <stop offset="100%" stop-color="#050811" stop-opacity="0" />
  </radialGradient>
  <pattern id="minor-grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#38bdf8" stroke-width="0.5" stroke-opacity="0.08" />
  </pattern>
  <pattern id="major-grid" width="96" height="96" patternUnits="userSpaceOnUse">
    <rect width="96" height="96" fill="url(#minor-grid)" />
    <path d="M 96 0 L 0 0 0 96" fill="none" stroke="#00e5ff" stroke-width="0.9" stroke-opacity="0.18" />
    <circle cx="0" cy="0" r="1.5" fill="#00e5ff" fill-opacity="0.35" />
  </pattern>
  <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3.5" result="blur" />
    <feMerge>
      <feMergeNode in="blur" />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>
</defs>
```

## 3. HUD Corner Reticle Macro

Add crisp corner reticles to cards and frames:

```python
def hud_reticles(x: int, y: int, w: int, h: int, size: int = 12, color: str = "#00e5ff") -> str:
    return "\n".join([
        f'<path d="M {x} {y+size} L {x} {y} L {x+size} {y}" fill="none" stroke="{color}" stroke-width="2"/>',
        f'<path d="M {x+w-size} {y} L {x+w} {y} L {x+w} {y+size}" fill="none" stroke="{color}" stroke-width="2"/>',
        f'<path d="M {x} {y+h-size} L {x} {y+h} L {x+size} {y+h}" fill="none" stroke="{color}" stroke-width="2"/>',
        f'<path d="M {x+w-size} {y+h} L {x+w} {y+h} L {x+w} {y+h-size}" fill="none" stroke="{color}" stroke-width="2"/>',
    ])
```
