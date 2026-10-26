# swe-skills Documentation Hub

Welcome to the comprehensive documentation suite for **swe-skills** — the engineering, architecture, and verification skill library designed for autonomous and paired AI coding agents (**Claude Code**, **Antigravity (`agy`)**, and **Cursor**).

---

## Documentation Navigation

```
docs/
├── README.md               # You are here: central navigational index
├── purpose.md              # Problem statement, threat model, token economics, principles
├── architecture.md         # Subsystems, lifecycle hooks, routing engine, subagent isolation
├── running.md              # Installation guide, profile management, environment variables, CLI
├── how-to.md               # Step-by-step recipes, CI integration, troubleshooting matrix
├── HOOKS.md                # Context guard hooks, PreInvocation, and model routing
├── EVIDENCE.md             # Empirical provenance and incident history across 20+ codebases
├── TESTING.md              # Pressure testing scenarios and benchmark evaluation
├── CHANGELOG.md            # Semantic version history and release ledger
├── diagrams/               # Multi-format architectural visual models
│   ├── README.md           # Diagram viewing & editing guide
│   ├── ascii_architecture.txt # Terminal-friendly ASCII schematics
│   ├── *.mmd               # Standalone Mermaid diagrams (flowcharts, sequence, state)
│   └── *.drawio            # Native draw.io XML vector diagrams
└── usermanual/             # 7-chapter comprehensive user guide
    ├── 01-getting-started.md
    ├── 02-skills-catalog.md
    ├── 03-hooks-and-context-guards.md
    ├── 04-workflows-and-recipes.md
    ├── 05-authoring-skills.md
    ├── 06-reference-and-cli.md
    └── 07-troubleshooting-and-faq.md
```

---

## Core Reading Order

1. **New to swe-skills?** Read [Purpose & Motivation](purpose.md) to understand the failure modes that LLM agents encounter without software engineering discipline.
2. **Installation & Profiles:** Follow [Running & Installation](running.md) to install skills with targeted profiles (`core`, `build`, `review`, `ship`) to save context tokens.
3. **Architecture & Internal Design:** Study [Architecture](architecture.md) and explore the visual models in [Diagrams](diagrams/README.md).
4. **Hands-On Recipes:** Follow [How-To Guides](how-to.md) for concrete recipes covering refactoring, PR review, subagent log isolation, and emergency context recovery.
5. **Detailed User Manual:** Dive into the [User Manual](usermanual/README.md) for exhaustive chapter-by-chapter reference material.
