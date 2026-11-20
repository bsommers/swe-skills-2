---
trigger: model_decision
description: >-
  Require a collapsible live Gantt chart panel at the top of every web tracker UI
  built in or templated from this project, visualizing parallel subagent swimlanes,
  pipeline phases, elapsed time ruler, live NOW cursor, and interactive hover tooltips.
---

# Web Tracker UI Standard: Collapsible Live Gantt Chart

Every live web tracker (`tracker/index.html`, `dashboard/index.html`, or any future dashboard / template) **MUST** include a sleek, collapsible **Live Gantt Chart** panel placed directly at the **top of the dashboard** (immediately below the hero header, above the pipeline stages and subagent cards).

## Mandatory Requirements

1. **Collapsible Header Bar**:
   - Expanded by default with a smooth CSS collapse/expand transition.
   - Dedicated `Collapse` / `Expand` toggle button with rotating chevron icon and proper `aria-expanded` attribute.
   - Persist collapsed state in `localStorage` so user preference survives page reloads.
   - Always display live **total elapsed time** (updating every 1s) and **active parallel lane count** (plus completed phase count) right in the header bar so key telemetry remains visible even when collapsed.

2. **Live Gantt Timeline**:
   - **Time Ruler**: spans from project `started_at` to live current time (`Date.now()`) with adaptive clean ticks (`+0m`, `+1m`, `+2m`, etc. + `HH:MM:SS` sub-labels), subtle vertical gridlines across all lanes, and a glowing vertical **NOW** cursor line with a floating `NOW` badge.
   - **Parallel Subagent Swimlanes**: dedicated horizontal swimlane row for every entry in `agents[]`, showing agent name, model pill, status indicator, and live bar.
   - **Pipeline Phase Group**: compact horizontal row group for all entries in `pipeline_stages[]` / `phases[]` aligned to the exact same time ruler and NOW cursor.
   - **Accurate Real-Time Bar Positioning**:
     - `RUNNING` / `ACTIVE` bars pulse smoothly up to the live **NOW** cursor with live progress and elapsed duration.
     - `DONE` bars lock cleanly in emerald green with their exact duration label (e.g., `✓ 1m 42s`).
     - `QUEUED` / `PENDING` rows render a subtle dashed waiting bar.
   - **Interactive Hover Tooltip**: delegated mouseover tooltip (viewport-clamped, zero flicker during live refreshes) displaying exact start time, duration, model/phase, progress `%`, and current task.

3. **Reference Implementations**:
   - Python stdlib + 3D/Blender viewport: `~/src/tools/blender-swarm-kit/gantt_tracker/`
   - Node 18+ SSE swarm dashboard: `~/src/tools/swarm-tracker/dashboard/index.html`
   - Minimal Python build tracker: `~/src/tools/build-tracker/index.html`
