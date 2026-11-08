# Deterministic SVG & PNG Rendering Pipeline

## 1. Directory Layout

```text
assets/
├── logo.svg                        # Square plugin/app icon (512x512)
└── logo.png                        # Rasterized square icon
docs/assets/
├── logo.svg                        # Wide hero banner (1200x360)
├── logo.png                        # Rasterized hero banner / OpenGraph image
├── icons/
│   └── icon-<category>.svg         # Subsystem / category vector badges
└── examples/
    ├── architecture-overview.svg   # High-level system architecture
    ├── architecture-overview.png
    ├── workflow-<name>.svg         # Step-by-step recipe visual
    └── workflow-<name>.png
```

## 2. Multi-Tool SVG-to-PNG Rasterization Fallback (Python)

Use a deterministic converter helper that prefers `inkscape` or `rsvg-convert` (which support full SVG 1.1/2.0 filters, gradients, and glow effects) before falling back to `resvg` or ImageMagick:

```python
import shutil
import subprocess
from pathlib import Path

def svg_to_png(svg_path: Path, png_path: Path, width: int = 1600) -> bool:
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
        return True
    if shutil.which("rsvg-convert"):
        subprocess.run(
            ["rsvg-convert", "-w", str(width), "-o", str(png_path), str(svg_path)],
            check=True,
        )
        return True
    if shutil.which("resvg"):
        subprocess.run(
            ["resvg", "-w", str(width), str(svg_path), str(png_path)],
            check=True,
        )
        return True
    if shutil.which("magick"):
        subprocess.run(
            ["magick", "-background", "none", str(svg_path), "-resize", f"{width}x", str(png_path)],
            check=True,
        )
        return True
    return False
```

## 3. Automated Integrity Test

Wire an integrity test into `tests/` so CI catches malformed XML or missing PNGs:

```python
import xml.etree.ElementTree as ET
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

def assert_valid_svg_and_png(svg_path: Path, png_path: Path) -> None:
    root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
    assert root.tag.endswith("svg"), f"Invalid root tag in {svg_path}"
    assert "viewBox" in root.attrib, f"Missing viewBox in {svg_path}"
    data = png_path.read_bytes()
    assert data.startswith(PNG_MAGIC) and len(data) > 512, f"Invalid PNG: {png_path}"
```
