"""Tests for SVG/PNG graphic generation, logo/icons, GitHub Pages site, tool registry, and local CI skills."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
DOCS = ROOT / "docs"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


class TestGraphicsLogoAndPagesSkills(unittest.TestCase):
    def test_six_new_skills_and_references_exist(self) -> None:
        expected = {
            "rendering-graphic-examples": "svg-png-pipeline.md",
            "showcasing-graphics-in-docs": "futuristic-neon-grid-theme.md",
            "designing-logos-and-icons": "logo-and-icon-templates.md",
            "building-github-pages-sites": "github-pages-template.md",
            "using-local-tool-registry": "local-tools-and-vm-catalog.md",
            "running-local-ci": "local-ci-and-vm-runners.md",
        }
        for skill, ref in expected.items():
            skill_md = SKILLS / skill / "SKILL.md"
            ref_md = SKILLS / skill / "references" / ref
            self.assertTrue(skill_md.is_file(), f"Missing {skill_md}")
            self.assertTrue(ref_md.is_file(), f"Missing {ref_md}")

    def test_plugin_json_wires_logo_and_matches_manifests(self) -> None:
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin.get("logo"), "assets/logo.svg")
        logo_svg = ROOT / plugin["logo"]
        logo_png = ROOT / "assets" / "logo.png"
        self.assertTrue(logo_svg.is_file())
        self.assertTrue(logo_png.is_file())
        self.assertTrue(logo_png.read_bytes().startswith(PNG_MAGIC))

        claude_plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        cursor_plugin = json.loads((ROOT / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], claude_plugin["version"])
        self.assertEqual(plugin["version"], cursor_plugin["version"])

    def test_all_svg_and_png_assets_are_valid(self) -> None:
        pairs = [
            (ROOT / "assets" / "logo.svg", ROOT / "assets" / "logo.png"),
            (DOCS / "assets" / "logo.svg", DOCS / "assets" / "logo.png"),
            (DOCS / "assets" / "icon.svg", DOCS / "assets" / "icon.png"),
        ]
        for kind in ("entry", "plan", "arch", "build", "verify", "sustain"):
            pairs.append(
                (DOCS / "assets" / "icons" / f"icon-{kind}.svg", DOCS / "assets" / "icons" / f"icon-{kind}.png")
            )
        for ex in (
            "architecture-overview",
            "workflow-eng-routing",
            "workflow-subagent-isolation",
            "workflow-session-chaining",
            "workflow-browser-qa-tri-os",
            "workflow-local-tools-and-ci",
        ):
            pairs.append(
                (DOCS / "assets" / "examples" / f"{ex}.svg", DOCS / "assets" / "examples" / f"{ex}.png")
            )

        self.assertEqual(len(pairs), 15)
        for svg_path, png_path in pairs:
            self.assertTrue(svg_path.is_file(), f"Missing SVG: {svg_path}")
            self.assertTrue(png_path.is_file(), f"Missing PNG: {png_path}")
            root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
            self.assertTrue(root.tag.endswith("svg"), f"Invalid SVG root in {svg_path}")
            self.assertIn("viewBox", root.attrib, f"Missing viewBox in {svg_path}")
            png_bytes = png_path.read_bytes()
            self.assertTrue(png_bytes.startswith(PNG_MAGIC), f"Invalid PNG header in {png_path}")
            self.assertGreater(len(png_bytes), 512, f"PNG too small: {png_path}")

    def test_github_pages_index_and_nojekyll_and_links(self) -> None:
        nojekyll = DOCS / ".nojekyll"
        index_html = DOCS / "index.html"
        self.assertTrue(nojekyll.is_file(), "Missing docs/.nojekyll")
        self.assertTrue(index_html.is_file(), "Missing docs/index.html")

        html_text = index_html.read_text(encoding="utf-8")
        # Check futuristic neon-grid theme tokens
        self.assertIn("--bg-void: #04070f", html_text)
        self.assertIn("--neon-cyan: #00e5ff", html_text)
        # Check every skill is listed in docs/index.html
        for p in sorted(SKILLS.iterdir()):
            if p.is_dir() and (p / "SKILL.md").is_file():
                self.assertIn(f"<code>{p.name}</code>", html_text, f"Skill {p.name} missing from docs/index.html")

        # Verify all local src/href targets in docs/index.html exist on disk
        for attr in re.findall(r'(?:src|href)="([^"#]+)"', html_text):
            if attr.startswith(("http://", "https://", "mailto:", "javascript:")):
                continue
            target = (DOCS / attr).resolve()
            self.assertTrue(target.exists(), f"Broken relative link in docs/index.html: {attr} -> {target}")

    def test_refreshed_docs_embed_graphic_examples_and_current_counts(self) -> None:
        skill_count = sum(1 for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
        self.assertEqual(skill_count, 68)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/index.html", readme)
        self.assertIn("docs/assets/examples/architecture-overview.svg", readme)
        self.assertIn("docs/assets/examples/workflow-local-tools-and-ci.svg", readme)
        self.assertIn(f"## Skills ({skill_count})", readme)

        arch = (DOCS / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("assets/examples/architecture-overview.svg", arch)
        self.assertIn("assets/examples/workflow-subagent-isolation.svg", arch)

        howto = (DOCS / "how-to.md").read_text(encoding="utf-8")
        self.assertIn("assets/examples/workflow-eng-routing.svg", howto)
        self.assertIn("assets/examples/workflow-session-chaining.svg", howto)
        self.assertIn("assets/examples/workflow-browser-qa-tri-os.svg", howto)
        self.assertIn("assets/examples/workflow-local-tools-and-ci.svg", howto)

    def test_tool_registry_cli_search_recommend_and_update(self) -> None:
        script = ROOT / "scripts" / "tool-registry.py"
        seed = DOCS / "tool-registry.seed.json"
        self.assertTrue(script.is_file())
        self.assertTrue(seed.is_file())

        # Search for VM tools using seed fallback
        with tempfile.TemporaryDirectory() as tmp:
            reg_file = Path(tmp) / "registry.json"
            res = subprocess.run(
                [sys.executable, str(script), "--registry", str(reg_file), "--json", "search", "cvm vm"],
                capture_output=True,
                text=True,
                check=True,
            )
            items = json.loads(res.stdout)
            names = [it["name"] for it in items]
            self.assertIn("cvm", names)

            # Recommend for verify phase
            rec = subprocess.run(
                [sys.executable, str(script), "--registry", str(reg_file), "--json", "recommend", "--phase", "verify"],
                capture_output=True,
                text=True,
                check=True,
            )
            rec_items = json.loads(rec.stdout)
            rec_names = [it["tool"]["name"] for it in rec_items]
            self.assertIn("gha-vm-runners", rec_names)
            self.assertIn("cvm", rec_names)

            # Show single tool
            show = subprocess.run(
                [sys.executable, str(script), "--registry", str(reg_file), "--json", "show", "win-devvm"],
                capture_output=True,
                text=True,
                check=True,
            )
            tool = json.loads(show.stdout)
            self.assertEqual(tool["name"], "win-devvm")
            self.assertIn("windows", tool["platforms"])


if __name__ == "__main__":
    unittest.main()
