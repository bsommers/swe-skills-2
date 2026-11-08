# GitHub Pages Neon-Grid Showcase Template & Verification

## 1. Relative Path Discipline in `docs/index.html`

Because GitHub Pages serves `docs/` as the site root (`https://<owner>.github.io/<repo>/`), all paths inside `docs/index.html` must be relative to `docs/`:

| Target File | Path from `README.md` | Path from `docs/index.html` |
|---|---|---|
| Hero Logo SVG | `docs/assets/logo.svg` | `assets/logo.svg` |
| Square Icon SVG | `docs/assets/icon.svg` | `assets/icon.svg` |
| Category Icons | `docs/assets/icons/icon-arch.svg` | `assets/icons/icon-arch.svg` |
| Graphic Examples | `docs/assets/examples/architecture-overview.svg` | `assets/examples/architecture-overview.svg` |
| Architecture Doc | `docs/architecture.md` | `architecture.md` |
| User Manual | `docs/usermanual/README.md` | `usermanual/README.md` |

## 2. CSS Futuristic Black + Light-Blue Neon Grid Background

```css
:root {
  --bg-void: #050811;
  --bg-panel: rgba(11, 20, 40, 0.88);
  --neon-cyan: #00e5ff;
  --neon-blue: #38bdf8;
  --neon-emerald: #00ff9d;
  --text-bright: #f0f6fc;
  --text-muted: #94a3b8;
}

body {
  background-color: var(--bg-void);
  background-image:
    radial-gradient(circle at 50% 0%, rgba(0, 229, 255, 0.14), transparent 55%),
    linear-gradient(rgba(0, 229, 255, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 229, 255, 0.07) 1px, transparent 1px),
    linear-gradient(rgba(56, 189, 248, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56, 189, 248, 0.035) 1px, transparent 1px);
  background-size: 100% 100%, 96px 96px, 96px 96px, 24px 24px, 24px 24px;
  color: var(--text-bright);
}
```

## 3. Automated HTML Asset Link Verification

Test in `tests/` that every local `src="..."` and `href="..."` in `docs/index.html` resolves on disk:

```python
import re
from pathlib import Path

def verify_pages_links(index_html: Path) -> None:
    html = index_html.read_text(encoding="utf-8")
    docs_dir = index_html.parent
    for attr in re.findall(r'(?:src|href)="([^"#]+)"', html):
        if attr.startswith(("http://", "https://", "mailto:", "javascript:")):
            continue
        target = (docs_dir / attr).resolve()
        assert target.exists(), f"Broken link in docs/index.html: {attr} -> {target}"
```
