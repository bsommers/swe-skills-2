# Architecture Diagrams Catalog

This directory contains visual models for the `swe-skills` architecture, lifecycle hooks, and subagent execution patterns across three supported mediums:

1. **ASCII Schematics (`.txt`)**: Terminal-ready, zero-dependency box drawings viewable directly in any shell (`cat` or text editor).
2. **Mermaid Diagrams (`.mmd`)**: Plain text diagram specifications renderable in GitHub, Mermaid Live Editor, or markdown previews.
3. **Native draw.io Vector XML (`.drawio`)**: Full visual diagrams editable with [diagrams.net](https://app.diagrams.net), the draw.io desktop app, or the VSCode Draw.io integration.

---

## Catalog

| Diagram | Formats | Purpose |
|---|---|---|
| **System Architecture** | [`ascii_architecture.txt`](ascii_architecture.txt)<br>[`architecture.mmd`](architecture.mmd)<br>[`architecture.drawio`](architecture.drawio) | Complete layered view: Harnesses (Claude, agy, Cursor) → Lifecycle Hooks → Discovery Router → 54 Skills Taxonomy → Isolated Subagents. |
| **Execution Flow** | [`execution_flow.mmd`](execution_flow.mmd)<br>[`execution_flow.drawio`](execution_flow.drawio) | End-to-end task journey from `/eng` invocation, through context guards, planning, subagent build/test isolation, to layered verification gates. |
| **Context & Cache Lifecycle** | [`context_lifecycle.mmd`](context_lifecycle.mmd) | State machine for Anthropic 5-minute cache TTL, agy 50-step thresholds, checkpointing, and compaction recovery. |

---

## How to View & Edit

### 1. ASCII Diagrams
View directly from terminal:
```bash
cat docs/diagrams/ascii_architecture.txt
```

### 2. Mermaid Diagrams
Preview with the Mermaid CLI or paste into [mermaid.live](https://mermaid.live):
```bash
# If mmdc (mermaid-cli) is installed:
mmdc -i docs/diagrams/architecture.mmd -o docs/diagrams/architecture.png
```

### 3. draw.io Diagrams
1. Open [app.diagrams.net](https://app.diagrams.net) in your browser.
2. Select **Open Existing Diagram** and upload any `.drawio` file from this folder.
3. Or install the `Hediet.vscode-drawio` extension in VS Code / Cursor to edit in-place.
