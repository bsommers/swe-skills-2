# QA Report: <app> <plan name>

- Date: <YYYY-MM-DD>
- Target: <base URL>, <commit or build>
- Driver: Playwright <version>, <browser>, viewport <WxH>, workers 1
- Command: `cd qa && npx playwright test`
- Totals: <n> PASS, <n> FAIL, <n> FIXME (copied from step-results.json)

## Steps

| Step | Plan item | Result | Evidence | Notes |
|---|---|---|---|---|
| 0 | <title> | PASS | qa/test-results/steps/0.png | |
| 1 | <title> | FAIL | qa/test-results/steps/1.png, trace | see Bug 1 |
| 2 | <title> | FIXME | none | cannot automate: <reason> |

## Evidence

- HTML report: `qa/playwright-report/index.html` (`npx playwright show-report qa/playwright-report`)
- Session video: `qa/test-results/<test-dir>/video.webm`
- Step screenshots: `qa/test-results/steps/`
- Traces (failures only): `qa/test-results/<test-dir>/trace.zip`

## Bugs found in the app

### Bug 1: <short title> (step <id>)
- Expected (plan): <quote>
- Actual: <observed output or text>
- Evidence: <paths>

## Driver fixes made this run

- <selector or timing fix, with the step id>

## Not automated (FIXME)

- <id>: <reason>
