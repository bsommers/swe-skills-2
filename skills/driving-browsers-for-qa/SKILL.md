---
name: driving-browsers-for-qa
description: Use when automating a web app's manual QA plan or UI checklist with a browser driver (Playwright, Selenium, Puppeteer), recording video, screenshot or trace evidence, running against an already-running dev stack, or reporting per-step pass/fail results.
---

# Driving Browsers for QA

## Overview

A manual QA plan becomes repeatable evidence when each step is a test that asserts a real outcome and leaves a video, screenshot and report behind. The driver is a QA tool, so it must not disturb the app it checks.

## Tool choice

Default to **Playwright**: auto-waiting, one-install runner, built-in video, trace and HTML report, `channel: 'chrome'`. Use Selenium/WebDriver when a grid, a non-Chromium vendor driver, or an existing suite is mandated; WebDriver BiDi when a standards-based cross-browser protocol is required; Puppeteer for a Chrome-only script with no runner needs. Details: `references/tool-choice.md`.

## Layout

- **Self-contained `qa/`** with its own `package.json`, lockfile and `tsconfig`; never add driver deps to the app.
- **Name specs `*.e2e.ts`** and set `testMatch: '**/*.e2e.ts'` so vitest/jest never collect them.
- **Browser:** reuse a system Chrome (`channel: 'chrome'`) or the cache (`~/.cache/ms-playwright`) first; download only when neither works.
- **Config:** `video: 'on'`, `screenshot: 'on'`, `trace: 'retain-on-failure'`, fixed `viewport`, `workers: 1`, `retries: 0`, HTML reporter with `open: 'never'`.
- **One serial spec** covering the plan gives one continuous session video. Wrap each plan step in `test.step`, record its result, screenshot it, and keep going after a failure; fail the test at the end if any step failed.

Starters: `references/playwright.config.template.ts`, `references/plan-steps.e2e.template.ts`, `references/QA-REPORT.template.md`.

## Rules

1. **Live stack is not yours.** Take URLs from env (`QA_BASE_URL`), preflight them, never start, stop or restart servers, and never touch other ports or processes.
2. **Clean up only what you made.** Give every created resource a prefix (`qa-e2e-`), sweep stale prefixed leftovers at start and end, and match by exact prefix.
3. **One plan step, one test step,** same numbering. Anything that cannot be automated safely (stopping the gateway, real credentials) is `test.fixme('<id>. <title>')` with the reason in the body.
4. **Assert outcomes,** not presence: read terminal text (xterm rows) and match the output, check counts, state attributes and absence of side effects. "Element visible" alone is not a pass.
5. **Driver bug vs app bug.** Selector, timing or setup failure: fix the driver. Behavior contradicts the plan: leave the test failing, quote the evidence, report it. Never loosen an assertion or add `fixme` to turn red green (`layered-verification-gates`).
6. **No secrets in evidence.** Keep tokens and passwords out of fixtures, typed text, screenshots and traces; read them from env and mask or avoid recording the field.
7. **Wait on conditions** (`expect.poll`, web-first assertions), not fixed sleeps, except to prove a negative (`engineering-for-determinism`).

## Commands

`/eng qa-drive <plan-file>`: read the plan, create or extend `qa/` from the templates, map every step to a test or `fixme`, run it, and fix driver faults until only app bugs remain.

`/eng qa-report`: read `qa/test-results/step-results.json` and the Playwright output, fill `qa/QA-REPORT.md` from the template (per-step PASS/FAIL/FIXME, evidence paths, bugs), and show `npx playwright show-report qa/playwright-report` plus the video path. Report only numbers you just read (`making-verifiable-claims`).

## Mistakes

- Installing Playwright into the app and bloating its lockfile.
- Spec named `*.spec.ts` or `*.test.ts` and picked up by the unit runner.
- Killing all `tmux`, node or browser processes instead of prefixed ones.
- Green test that only checked a button existed.
- Retrying or `.skip`-ing a real app failure.
