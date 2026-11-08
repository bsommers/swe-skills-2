# Logo & Icon Geometry Templates

## 1. Hexagonal Cyber-Core Emblem (Python SVG Helper)

Generates a precision multi-ring hexagonal emblem with circuit spokes and glowing core:

```python
import math

def hex_points(cx: float, cy: float, r: float, rotate_deg: float = -90.0) -> str:
    pts = []
    for i in range(6):
        ang = math.radians(rotate_deg + i * 60.0)
        pts.append(f"{cx + r * math.cos(ang):.1f},{cy + r * math.sin(ang):.1f}")
    return " ".join(pts)
```

- **Outer Shield:** Regular hexagon ($R = 190$ in `512x512`) with `#00e5ff` `4px` stroke and corner vertex nodes.
- **Inner Circuit Ring:** Rotated $30^\circ$ hexagon ($R = 135$) with dashed `#38bdf8` trace lines and 6 radial synaptic spokes connecting to the central core.
- **Central Routing Core:** Glowing isometric cube / diamond node (`#00ff9d` + `#00e5ff`) representing deterministic verification and skill routing.

## 2. Category Icon Grid (`64x64` `viewBox="0 0 64 64"`)

Every category icon shares:
- Rounded dark obsidian frame (`x="4" y="4" width="56" height="56" rx="12"` fill `#070d1c`, stroke `#00e5ff` `1.75px`).
- Subtle internal 16px neon grid.
- Distinct foreground glyph (`stroke-width="2.5"` `stroke-linecap="round"` `stroke-linejoin="round"`):
  1. `icon-entry.svg` — Compass / routing prism splitting 1 input beam into 3 targeted skill beams.
  2. `icon-plan.svg` — Architectural blueprint matrix with 8-tier verification checkmarks.
  3. `icon-arch.svg` — Hexagonal modular nodes with clean pluggable contract seams.
  4. `icon-build.svg` — Hardened terminal anvil / shield with lock & deterministic gear.
  5. `icon-verify.svg` — Multi-layer radar scope / verification gate with neon emerald pulse.
  6. `icon-sustain.svg` — Infinite session-chain loop with checkpoint crystal node.
