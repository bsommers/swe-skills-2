#!/usr/bin/env python3
"""Centralized searchable tool registry and ~/src scanner for swe-skills.

Discovers, indexes, searches, and recommends local engineering tools, VM/sandbox
runners (cvm, win-devvm, gha-vm-runners, fedora-vms, freebsd-kvm), local CI harnesses,
static analyzers, benchmark suites, and CLI utilities across ~/src and $PATH.

Commands:
  python3 scripts/tool-registry.py update [--root ~/src]
  python3 scripts/tool-registry.py search <query> [--phase <phase>] [--category <cat>] [--json]
  python3 scripts/tool-registry.py list [--phase <phase>] [--category <cat>] [--available-only] [--json]
  python3 scripts/tool-registry.py show <name> [--json]
  python3 scripts/tool-registry.py recommend --task "<task>" [--phase <phase>] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = ROOT / "docs" / "tool-registry.seed.json"

LIFECYCLE_PHASES = ("plan", "build", "execute", "test", "verify", "ci", "release")
CATEGORIES = (
    "vm-sandbox",
    "cross-platform-vm",
    "local-ci",
    "static-analysis",
    "benchmark-eval",
    "code-intelligence",
    "cli-automation",
    "security",
    "release-packaging",
    "general-dev",
)

# Curated high-signal definitions for primary tools in ~/src (portable ~ paths)
CURATED_TOOLS: list[dict[str, Any]] = [
    {
        "name": "cvm",
        "path": "~/src/ai/projects/cvm",
        "category": "vm-sandbox",
        "lifecycle_phases": ["plan", "build", "execute", "test", "ci", "release"],
        "platforms": ["linux", "macos", "windows", "freebsd"],
        "summary": "Code Virtual Machine (v1.2.0): automated VM & container sandbox runner across 13 backends (KVM/QEMU, Firecracker, Cloud Hypervisor, Apple VZ/Tart, macOS Seatbelt, Docker, Podman, VirtualBox, VMware, Hyper-V, Proxmox, bhyve) with COW snapshots, branching, multi-agent mesh, and MCP server.",
        "entrypoints": [
            "~/src/ai/projects/cvm/bin/cvm run --backend kvm -- <cmd>",
            "~/src/ai/projects/cvm/bin/cvm snapshot <workspace>",
            "~/src/ai/projects/cvm/bin/cvm branch <workspace> <branch-name>",
            "~/src/ai/projects/cvm/bin/cvm restore <workspace> <snapshot>",
            "~/src/ai/projects/cvm/bin/cvm serve-mcp",
        ],
        "tags": [
            "vm",
            "sandbox",
            "kvm",
            "qemu",
            "firecracker",
            "microvm",
            "apple-vz",
            "seatbelt",
            "docker",
            "podman",
            "bhyve",
            "snapshot",
            "branch",
            "agent",
            "isolation",
            "cvm",
            "mcp",
        ],
    },
    {
        "name": "win-devvm",
        "path": "~/src/infra/win-devvm",
        "category": "cross-platform-vm",
        "lifecycle_phases": ["build", "test", "ci", "release"],
        "platforms": ["linux", "macos", "windows"],
        "summary": "Unattended Windows 11 dev VM (rootless KVM/libvirt x64 on Linux; Parallels ARM64 on macOS) pre-provisioned with MSVC Build Tools (x64 + ARM64), rustup, Python, Node, CMake, Git, and key-based SSH/RDP for local Windows build, driver, and release testing.",
        "entrypoints": [
            "cd ~/src/infra/win-devvm && ./provision.sh",
            "cd ~/src/infra/win-devvm && ./vm.sh start",
            "cd ~/src/infra/win-devvm && ./vm.sh ssh",
            "cd ~/src/infra/win-devvm && ./vm.sh status",
            "cd ~/src/infra/win-devvm && ./vm.sh stop",
        ],
        "tags": [
            "windows",
            "windows-11",
            "vm",
            "kvm",
            "libvirt",
            "parallels",
            "msvc",
            "rust",
            "cross-platform",
            "driver",
            "binaries",
            "ssh",
            "rdp",
            "win-devvm",
        ],
    },
    {
        "name": "gha-vm-runners",
        "path": "~/src/gha-vm-runners",
        "category": "local-ci",
        "lifecycle_phases": ["test", "ci", "release"],
        "platforms": ["linux"],
        "summary": "Local CI runner (local-ci.sh) and disposable Ubuntu 24.04 KVM self-hosted GitHub Actions VM runner (gha-vm-runners.sh) that executes full repository CI pipelines locally without spending hosted GitHub Actions minutes.",
        "entrypoints": [
            "~/src/gha-vm-runners/local-ci.sh <repo-path>",
            "~/src/gha-vm-runners/local-ci.sh --full <repo-path>",
            "~/src/gha-vm-runners/gha-vm-runners.sh status",
            "~/src/gha-vm-runners/gha-vm-runners.sh start",
            "~/src/gha-vm-runners/gha-vm-runners.sh stop",
        ],
        "tags": [
            "ci",
            "local-ci",
            "github-actions",
            "runner",
            "vm",
            "kvm",
            "ubuntu",
            "minutes",
            "finops",
            "verification",
            "gha-vm-runners",
        ],
    },
    {
        "name": "fedora-vms",
        "path": "~/src/infra/fedora-vms",
        "category": "cross-platform-vm",
        "lifecycle_phases": ["build", "test", "ci"],
        "platforms": ["linux"],
        "summary": "Fedora Linux KVM/QEMU guest launcher (cr-fedora-latest.sh) for testing RPM packaging, systemd services, SELinux policies, and Linux distribution portability.",
        "entrypoints": [
            "cd ~/src/infra/fedora-vms && ./cr-fedora-latest.sh",
        ],
        "tags": ["fedora", "vm", "kvm", "linux", "rpm", "systemd", "distro", "portability"],
    },
    {
        "name": "freebsd-kvm",
        "path": "~/src/vms/scripts",
        "category": "cross-platform-vm",
        "lifecycle_phases": ["build", "test", "ci", "release"],
        "platforms": ["freebsd", "linux"],
        "summary": "FreeBSD 15.x KVM/QEMU virtual machine scripts and QCOW2 disk images (run-fbsd.sh, kvm-freebsd-15.2.sh) for BSD portability, kqueue/jail driver testing, and release binary verification.",
        "entrypoints": [
            "cd ~/src/vms/scripts && ./run-fbsd.sh",
            "cd ~/src/vms/scripts && ./run-kvm-freebsd15.2.sh",
        ],
        "tags": ["freebsd", "bsd", "vm", "kvm", "qemu", "qcow2", "kqueue", "portability"],
    },
    {
        "name": "flowscope",
        "path": "~/src/flowscope",
        "category": "static-analysis",
        "lifecycle_phases": ["build", "test", "ci", "release"],
        "platforms": ["linux", "macos", "windows"],
        "summary": "High-speed static analysis and taint/flow scanner outputting SARIF and HTML security reports for pre-commit and local CI security gates.",
        "entrypoints": [
            "flowscope scan . --format sarif -o report.sarif",
            "flowscope scan . --format html -o report.html",
        ],
        "tags": ["sast", "security", "static-analysis", "sarif", "taint", "scanner", "flowscope"],
    },
    {
        "name": "synth",
        "path": "~/src/synth",
        "category": "benchmark-eval",
        "lifecycle_phases": ["test", "ci"],
        "platforms": ["linux", "macos", "windows"],
        "summary": "Synthetic vulnerability corpus and gold-standard SARIF evaluation harness for benchmarking SAST scanners reproducibly against ground truth.",
        "entrypoints": [
            "cd ~/src/synth && pytest -q",
        ],
        "tags": ["benchmark", "sast", "sarif", "corpus", "security", "evaluation", "synth"],
    },
    {
        "name": "eval",
        "path": "~/src/eval",
        "category": "benchmark-eval",
        "lifecycle_phases": ["plan", "test", "release"],
        "platforms": ["linux", "macos", "windows"],
        "summary": "Academic Evaluation & Benchmark Auditing Suite (OmniReview Academic) for statistical reproducibility, AST cyclomatic complexity, layer boundary checks, and Toulmin claim verification.",
        "entrypoints": [
            "cd ~/src/eval && python3 -m unittest",
        ],
        "tags": ["benchmark", "audit", "statistics", "complexity", "ast", "evaluation", "omnireview"],
    },
    {
        "name": "gitnexus",
        "path": "~/src/coding/GitNexus",
        "category": "code-intelligence",
        "lifecycle_phases": ["plan", "build", "test"],
        "platforms": ["linux", "macos", "windows"],
        "summary": "Repository structural graph and code intelligence analyzer for mapping cross-file dependencies and call graphs before refactoring.",
        "entrypoints": [
            "cd ~/src/coding/GitNexus",
        ],
        "tags": ["graph", "ast", "architecture", "dependencies", "code-intelligence", "gitnexus"],
    },
    {
        "name": "ontologic",
        "path": "~/src/ontology/OntoLogic",
        "category": "code-intelligence",
        "lifecycle_phases": ["plan", "build", "test"],
        "platforms": ["linux", "macos"],
        "summary": "Ontology-driven knowledge graph and reasoning engine with multi-substrate toolchains and local CI integration.",
        "entrypoints": [
            "~/src/gha-vm-runners/local-ci.sh ~/src/ontology/OntoLogic",
        ],
        "tags": ["ontology", "knowledge-graph", "reasoning", "ontologic"],
    },
    {
        "name": "cli-anything",
        "path": "~/src/utilities/CLI-Anything",
        "category": "cli-automation",
        "lifecycle_phases": ["build", "execute", "test"],
        "platforms": ["linux", "macos", "windows"],
        "summary": "Collection of 50+ scriptable CLI adapters and agent skills for desktop and developer applications (Inkscape, GIMP, Blender, Audacity, OBS, Draw.io, Mermaid, LibreOffice, LLDB, WireMock).",
        "entrypoints": [
            "ls ~/src/utilities/CLI-Anything",
        ],
        "tags": ["cli", "automation", "adapters", "inkscape", "drawio", "mermaid", "lldb", "wiremock"],
    },
    {
        "name": "bilterm",
        "path": "~/src/ai/bilterm",
        "category": "cli-automation",
        "lifecycle_phases": ["execute", "test"],
        "platforms": ["linux", "macos"],
        "summary": "Terminal emulator and PTY session harness for interactive CLI and TUI verification.",
        "entrypoints": [
            "cd ~/src/ai/bilterm",
        ],
        "tags": ["terminal", "pty", "tui", "cli", "bilterm"],
    },
    {
        "name": "feed-brain-gh",
        "path": "~/src/meta/feed-brain-gh",
        "category": "code-intelligence",
        "lifecycle_phases": ["plan", "release"],
        "platforms": ["linux", "macos"],
        "summary": "Multi-repository knowledge extraction and pattern harvesting engine.",
        "entrypoints": [
            "cd ~/src/meta/feed-brain-gh",
        ],
        "tags": ["knowledge", "meta", "mining", "patterns", "feed-brain-gh"],
    },
    {
        "name": "seed-brain-gh",
        "path": "~/src/meta/seed-brain-gh",
        "category": "code-intelligence",
        "lifecycle_phases": ["plan", "build"],
        "platforms": ["linux", "macos"],
        "summary": "Non-destructive engineering standards and skill seeding engine across repositories.",
        "entrypoints": [
            "cd ~/src/meta/seed-brain-gh",
        ],
        "tags": ["seeding", "standards", "templates", "meta", "seed-brain-gh"],
    },
]


def default_user_registry_path() -> Path:
    override = os.environ.get("SWE_SKILLS_TOOL_REGISTRY_PATH")
    if override:
        return Path(override).expanduser()
    sys_name = platform.system().lower()
    if sys_name == "windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "swe-skills" / "tool-registry.json"
    if sys_name == "darwin":
        return Path.home() / "Library" / "Application Support" / "swe-skills" / "tool-registry.json"
    xdg = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return xdg / "swe-skills" / "tool-registry.json"


def to_tilde_path(p: Path) -> str:
    home = str(Path.home())
    s = str(p.resolve())
    if s == home:
        return "~"
    if s.startswith(home + os.sep):
        return "~/" + s[len(home) + 1 :].replace("\\", "/")
    return s.replace("\\", "/")


def expand_tilde_path(p_str: str) -> Path:
    return Path(os.path.expanduser(p_str))


def extract_readme_summary(repo_dir: Path) -> str:
    for name in ("README.md", "readme.md", "README.txt", "README"):
        f = repo_dir / name
        if f.is_file():
            try:
                lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            para: list[str] = []
            for raw in lines:
                line = raw.strip()
                if not line:
                    if para:
                        break
                    continue
                if (
                    line.startswith("#")
                    or line.startswith("![")
                    or line.startswith("[![")
                    or line.startswith("<")
                    or line.startswith("```")
                    or line.startswith("---")
                    or line.startswith("|")
                ):
                    continue
                # Strip markdown bold/code markers for clean summary
                clean = re.sub(r"[*_`]", "", line)
                para.append(clean)
                if sum(len(x) for x in para) >= 160:
                    break
            if para:
                summary = " ".join(para)
                return summary[:240] + ("…" if len(summary) > 240 else "")
    return f"Local engineering repository at {to_tilde_path(repo_dir)}."


def infer_category_and_phases(name: str, rel_path: str, summary: str) -> tuple[str, list[str], list[str]]:
    blob = f"{name} {rel_path} {summary}".lower()
    tags = sorted(set(re.findall(r"[a-z0-9]{3,}", blob)) - {"the", "and", "for", "with", "from", "this", "that", "into", "src"})[:18]
    if any(k in blob for k in ("cvm", "sandbox", "microvm", "firecracker", "hypervisor")):
        return "vm-sandbox", ["plan", "build", "execute", "test", "ci", "release"], tags
    if any(k in blob for k in ("win-devvm", "fedora-vm", "freebsd", "parallels", "libvirt", "qcow2", "vms")):
        return "cross-platform-vm", ["build", "test", "ci", "release"], tags
    if any(k in blob for k in ("local-ci", "gha-vm", "runner", "github-actions", "workflow")):
        return "local-ci", ["test", "ci", "release"], tags
    if any(k in blob for k in ("sast", "sarif", "flowscope", "vulnerability", "security-skills", "scanner")):
        return "security", ["build", "test", "ci"], tags
    if any(k in blob for k in ("benchmark", "eval", "corpus", "omnireview", "synth")):
        return "benchmark-eval", ["plan", "test", "release"], tags
    if any(k in blob for k in ("ontology", "graph", "gitnexus", "brain", "kg", "kuzu")):
        return "code-intelligence", ["plan", "build", "test"], tags
    if any(k in blob for k in ("cli", "term", "pty", "shell")):
        return "cli-automation", ["build", "execute", "test"], tags
    return "general-dev", ["build", "test"], tags


def detect_entrypoints(repo_dir: Path, tilde_path: str) -> list[str]:
    eps: list[str] = []
    for script in ("local-ci.sh", "provision.sh", "vm.sh", "gha-vm-runners.sh", "scripts/verify.sh", "scripts/install.sh"):
        if (repo_dir / script).is_file():
            eps.append(f"{tilde_path}/{script}")
    if (repo_dir / "Cargo.toml").is_file():
        eps.append(f"cd {tilde_path} && cargo test -q")
    elif (repo_dir / "pyproject.toml").is_file() or (repo_dir / "setup.py").is_file():
        eps.append(f"cd {tilde_path} && pytest -q")
    elif (repo_dir / "package.json").is_file():
        eps.append(f"cd {tilde_path} && npm test -s")
    if not eps:
        eps.append(f"cd {tilde_path}")
    return eps[:5]


def scan_roots(roots: list[Path], max_depth: int = 3) -> dict[str, dict[str, Any]]:
    by_name: dict[str, dict[str, Any]] = {}

    # 1. Load curated catalog first
    for item in CURATED_TOOLS:
        entry = dict(item)
        expanded = expand_tilde_path(entry["path"])
        entry["available"] = expanded.exists()
        entry["source"] = "curated"
        by_name[entry["name"]] = entry

    # 2. Walk roots up to max_depth for git/package/script directories
    markers = (".git", "Cargo.toml", "pyproject.toml", "package.json", "flake.nix", "provision.sh", "local-ci.sh")
    skip_dirs = {
        ".git",
        "node_modules",
        "target",
        ".venv",
        "venv",
        "__pycache__",
        ".ruff_cache",
        ".mypy_cache",
        ".pytest_cache",
        "dist",
        "build",
    }

    for root in roots:
        if not root.is_dir():
            continue
        root_resolved = root.resolve()
        for dirpath, dirnames, filenames in os.walk(root_resolved):
            dirnames[:] = [d for d in sorted(dirnames) if d not in skip_dirs and not d.startswith(".")]
            cur = Path(dirpath)
            rel_parts = cur.relative_to(root_resolved).parts
            if len(rel_parts) > max_depth:
                dirnames[:] = []
                continue
            if len(rel_parts) == 0:
                continue

            has_marker = any((cur / m).exists() for m in markers)
            if not has_marker:
                continue

            tilde = to_tilde_path(cur)
            slug = cur.name.lower().replace("_", "-")
            # Avoid overwriting curated tools; only update availability
            if slug in by_name and by_name[slug].get("source") == "curated":
                by_name[slug]["available"] = True
                continue
            # Also check if any curated tool has this exact tilde path
            if any(t.get("path") == tilde for t in by_name.values()):
                continue

            summary = extract_readme_summary(cur)
            cat, phases, tags = infer_category_and_phases(slug, tilde, summary)
            by_name[slug] = {
                "name": slug,
                "path": tilde,
                "category": cat,
                "lifecycle_phases": phases,
                "platforms": ["linux", "macos", "windows"],
                "summary": summary,
                "entrypoints": detect_entrypoints(cur, tilde),
                "tags": tags,
                "available": True,
                "source": "discovered",
            }
            # Don't recurse deeper inside a discovered repo unless it's a container category dir
            if (cur / ".git").exists():
                dirnames[:] = []

    return by_name


def load_registry(registry_override: str | None = None) -> dict[str, Any]:
    user_path = Path(registry_override).expanduser() if registry_override else default_user_registry_path()
    if user_path.is_file():
        try:
            data = json.loads(user_path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "tools" in data:
                for t in data["tools"]:
                    t["available"] = expand_tilde_path(t["path"]).exists()
                return data
        except (OSError, json.JSONDecodeError):
            pass
    if SEED_PATH.is_file():
        data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
        for t in data.get("tools", []):
            t["available"] = expand_tilde_path(t["path"]).exists()
        return data
    tools = list(scan_roots([Path.home() / "src"]).values())
    return {"version": 1, "tools": sorted(tools, key=lambda x: x["name"])}


def _phase_matches(phase: str | None, tool_phases: list[str]) -> bool:
    if not phase:
        return True
    if phase == "verify":
        return any(p in tool_phases for p in ("verify", "test", "ci"))
    return phase in tool_phases


def score_tool(tool: dict[str, Any], query_terms: list[str], phase: str | None, category: str | None) -> int:
    if category and tool.get("category") != category:
        return 0
    if not _phase_matches(phase, tool.get("lifecycle_phases", [])):
        return 0
    if not query_terms:
        return 100 if tool.get("source") == "curated" else 50

    score = 0
    name_l = tool["name"].lower()
    cat_l = tool.get("category", "").lower()
    summary_l = tool.get("summary", "").lower()
    tags_set = {t.lower() for t in tool.get("tags", [])}
    eps_l = " ".join(tool.get("entrypoints", [])).lower()
    phases_set = {p.lower() for p in tool.get("lifecycle_phases", [])}

    for term in query_terms:
        matched = False
        if term == name_l:
            score += 60
            matched = True
        elif term in name_l:
            score += 35
            matched = True
        if term in tags_set:
            score += 25
            matched = True
        elif any(term in tg for tg in tags_set):
            score += 12
            matched = True
        if term == cat_l or term in cat_l:
            score += 20
            matched = True
        if term in phases_set:
            score += 15
            matched = True
        if term in summary_l:
            score += 10
            matched = True
        if term in eps_l:
            score += 8
            matched = True
        if not matched:
            return 0

    if tool.get("source") == "curated":
        score += 10
    if tool.get("available"):
        score += 5
    return score


def cmd_update(args: argparse.Namespace) -> int:
    roots = [Path(r).expanduser() for r in (args.root or ["~/src"])]
    discovered = scan_roots(roots, max_depth=args.max_depth)
    tools_sorted = sorted(
        discovered.values(),
        key=lambda t: (0 if t.get("source") == "curated" else 1, t["name"]),
    )

    payload = {
        "schema_version": "1.0",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "roots": [to_tilde_path(r) if r.exists() else str(r) for r in roots],
        "tool_count": len(tools_sorted),
        "tools": tools_sorted,
    }

    user_path = default_user_registry_path()
    user_path.parent.mkdir(parents=True, exist_ok=True)
    user_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if args.write_seed:
        # Seed file keeps only portable curated entries + deterministic fields
        seed_tools = []
        for item in CURATED_TOOLS:
            entry = dict(item)
            entry["source"] = "curated"
            seed_tools.append(entry)
        seed_payload = {
            "schema_version": "1.0",
            "description": "Portable seed catalog of local engineering, VM, sandbox, and CI tools in ~/src.",
            "tool_count": len(seed_tools),
            "tools": seed_tools,
        }
        SEED_PATH.write_text(json.dumps(seed_payload, indent=2) + "\n", encoding="utf-8")

    avail = sum(1 for t in tools_sorted if t.get("available"))
    if args.json:
        print(json.dumps({"registry_path": to_tilde_path(user_path), "tool_count": len(tools_sorted), "available": avail}))
    else:
        print(f"Updated tool registry: {len(tools_sorted)} tools indexed ({avail} available locally) -> {to_tilde_path(user_path)}")
    return 0


def cmd_search_or_list(args: argparse.Namespace, is_search: bool) -> int:
    reg = load_registry(getattr(args, "registry", None))
    tools = reg.get("tools", [])
    raw_query = " ".join(args.query) if is_search else ""
    terms = [t.lower() for t in re.findall(r"[a-zA-Z0-9_-]+", raw_query)]

    results: list[tuple[int, dict[str, Any]]] = []
    for t in tools:
        if getattr(args, "available_only", False) and not t.get("available"):
            continue
        sc = score_tool(t, terms, args.phase, args.category)
        if sc > 0:
            results.append((sc, t))

    results.sort(key=lambda pair: (-pair[0], pair[1]["name"]))
    limit = getattr(args, "limit", 25) or 25
    matched = [t for _, t in results[:limit]]

    if args.json:
        print(json.dumps(matched, indent=2))
        return 0

    if not matched:
        print("No matching tools found.")
        return 1

    for t in matched:
        status = "READY" if t.get("available") else "SEED"
        phases = ",".join(t.get("lifecycle_phases", []))
        ep = t.get("entrypoints", [""])[0]
        print(f"{t['name']:<20} [{status:<5}] ({t['category']} | {phases}) -> {t['path']}")
        print(f"  {t['summary']}")
        if ep:
            print(f"  cmd: {ep}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    reg = load_registry(getattr(args, "registry", None))
    target = args.name.lower()
    for t in reg.get("tools", []):
        if t["name"].lower() == target:
            if args.json:
                print(json.dumps(t, indent=2))
                return 0
            status = "AVAILABLE" if t.get("available") else "NOT FOUND ON THIS HOST"
            print(f"Tool:        {t['name']} ({status})")
            print(f"Path:        {t['path']}")
            print(f"Category:    {t['category']}")
            print(f"Phases:      {', '.join(t.get('lifecycle_phases', []))}")
            print(f"Platforms:   {', '.join(t.get('platforms', []))}")
            print(f"Summary:     {t['summary']}")
            print("Entrypoints:")
            for ep in t.get("entrypoints", []):
                print(f"  $ {ep}")
            print(f"Tags:        {', '.join(t.get('tags', []))}")
            return 0
    print(f"Tool '{args.name}' not found in registry.", file=sys.stderr)
    return 1


def cmd_recommend(args: argparse.Namespace) -> int:
    reg = load_registry(getattr(args, "registry", None))
    task_l = (args.task or args.phase or "ci verify vm").lower()
    terms = set(re.findall(r"[a-z0-9_-]{2,}", task_l))

    recs: list[tuple[int, str, dict[str, Any]]] = []
    for t in reg.get("tools", []):
        if not _phase_matches(args.phase, t.get("lifecycle_phases", [])):
            continue
        score = 0
        reason = []
        t_tags = {tg.lower() for tg in t.get("tags", [])}
        overlap = sorted(terms & t_tags)
        if overlap:
            score += 20 * len(overlap)
            reason.append(f"matches {', '.join(overlap[:4])}")
        if t["name"].lower() in terms:
            score += 50
            reason.append(f"explicitly names {t['name']}")

        # Heuristic boosts for common engineering needs
        if any(w in task_l for w in ("ci", "github", "actions", "push", "pr", "verify", "test", "workflow")) and t["name"] == "gha-vm-runners":
            score += 45
            reason.append("runs CI locally without spending GitHub Actions minutes")
        if any(w in task_l for w in ("windows", "msvc", "win32", "conpty", "cross-platform", "tri-os", "binaries")) and t["name"] == "win-devvm":
            score += 45
            reason.append("provides unattended Windows 11 x64/ARM64 VM with MSVC & SSH")
        if any(w in task_l for w in ("sandbox", "untrusted", "vm", "isolate", "agent", "parallel", "snapshot", "branch", "macos", "kvm", "verify", "test")) and t["name"] == "cvm":
            score += 40
            reason.append("provides isolated 13-backend VM/container sandboxes with COW snapshots")
        if any(w in task_l for w in ("freebsd", "bsd", "kqueue", "jail")) and t["name"] == "freebsd-kvm":
            score += 45
            reason.append("provides FreeBSD 15.x KVM guest for BSD testing")
        if any(w in task_l for w in ("fedora", "rpm", "selinux", "systemd")) and t["name"] == "fedora-vms":
            score += 45
            reason.append("provides Fedora KVM guest for Linux distro testing")
        if any(w in task_l for w in ("security", "sast", "audit", "taint", "sarif", "vulnerability")) and t["name"] in ("flowscope", "synth"):
            score += 35
            reason.append("provides local SAST scanning & SARIF verification")

        if score > 0:
            recs.append((score, "; ".join(reason) or t["summary"], t))

    recs.sort(key=lambda item: (-item[0], item[2]["name"]))
    top = recs[: args.limit]

    if args.json:
        print(
            json.dumps(
                [{"score": sc, "why": why, "tool": t} for sc, why, t in top],
                indent=2,
            )
        )
        return 0

    if not top:
        print("No specific local tool matched; run `python3 scripts/tool-registry.py list` to browse.")
        return 0

    for sc, why, t in top:
        status = "READY" if t.get("available") else "SEED"
        ep = t.get("entrypoints", [""])[0]
        print(f"• {t['name']} [{status}] ({t['path']}) — {why}")
        if ep:
            print(f"  run: {ep}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Searchable local tool & VM registry for swe-skills.")
    p.add_argument("--registry", help="Optional override path to registry JSON file")
    p.add_argument("--json", action="store_true", help="Emit JSON output")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_up = sub.add_parser("update", help="Scan ~/src and update the centralized tool registry")
    p_up.add_argument("--root", action="append", help="Root directory to scan (default: ~/src)")
    p_up.add_argument("--max-depth", type=int, default=3, help="Max directory recursion depth (default: 3)")
    p_up.add_argument("--write-seed", action="store_true", help="Also refresh docs/tool-registry.seed.json")
    p_up.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Emit JSON output")

    p_sr = sub.add_parser("search", help="Search tools by keyword, lifecycle phase, or category")
    p_sr.add_argument("query", nargs="+", help="Search terms")
    p_sr.add_argument("--phase", choices=LIFECYCLE_PHASES, help="Filter by lifecycle phase")
    p_sr.add_argument("--category", choices=CATEGORIES, help="Filter by category")
    p_sr.add_argument("--available-only", action="store_true", help="Only show tools present on this host")
    p_sr.add_argument("--limit", type=int, default=20, help="Max results")
    p_sr.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Emit JSON output")

    p_ls = sub.add_parser("list", help="List registered tools")
    p_ls.add_argument("--phase", choices=LIFECYCLE_PHASES, help="Filter by lifecycle phase")
    p_ls.add_argument("--category", choices=CATEGORIES, help="Filter by category")
    p_ls.add_argument("--available-only", action="store_true", help="Only show tools present on this host")
    p_ls.add_argument("--limit", type=int, default=50, help="Max results")
    p_ls.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Emit JSON output")

    p_sh = sub.add_parser("show", help="Show detailed metadata and entrypoints for one tool")
    p_sh.add_argument("name", help="Tool name (e.g. cvm, win-devvm, gha-vm-runners)")
    p_sh.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Emit JSON output")

    p_rc = sub.add_parser("recommend", help="Recommend local tools for a task description")
    p_rc.add_argument("--task", help="Task description")
    p_rc.add_argument("--phase", choices=LIFECYCLE_PHASES, help="Current lifecycle phase")
    p_rc.add_argument("--limit", type=int, default=5, help="Max recommendations")
    p_rc.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Emit JSON output")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "update":
        return cmd_update(args)
    if args.cmd == "search":
        return cmd_search_or_list(args, is_search=True)
    if args.cmd == "list":
        return cmd_search_or_list(args, is_search=False)
    if args.cmd == "show":
        return cmd_show(args)
    if args.cmd == "recommend":
        return cmd_recommend(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
