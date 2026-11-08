# Browser driver choice

| Need | Pick | Why |
|---|---|---|
| Default web-app QA with evidence | Playwright Test | Auto-waiting, web-first assertions, video, trace, HTML report, one runner |
| Real Chrome with the user's profile or codecs | Playwright `channel: 'chrome'` | No browser download, matches what testers use |
| Mandated grid, vendor or legacy browser, existing Selenium suite | Selenium / WebDriver | Broadest driver ecosystem; accept manual waits and no built-in video |
| Standards-based bidirectional protocol across browsers | WebDriver BiDi | W3C direction; events and network interception without CDP; tooling is younger |
| Chrome-only script, no test runner, scraping or PDF | Puppeteer | Small API; you build reporting yourself |

Switch away from Playwright only for a stated constraint, and record it (`defending-architecture-decisions`).

## Browser acquisition order

1. System Chrome: `channel: 'chrome'`.
2. Cached browsers: `ls ~/.cache/ms-playwright`. A cached build only matches the Playwright version that expects it; pin a version that does, or use the system Chrome.
3. Download (`npx playwright install chromium`) last, and say so.

## Reading results

- HTML report: `npx playwright show-report <dir>`; the config writes it to `qa/playwright-report/`.
- Video, screenshots and traces land under `qa/test-results/`; open a trace with `npx playwright show-trace <trace.zip>`.
- Traces record network bodies and typed text. Treat them as sensitive; do not attach them where credentials could leak.
