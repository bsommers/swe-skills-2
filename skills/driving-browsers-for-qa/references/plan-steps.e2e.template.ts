import { test, expect, type Page, type TestInfo } from '@playwright/test';
import * as fs from 'node:fs';
import * as path from 'node:path';

const PREFIX = 'qa-e2e-'; // every resource this driver creates starts with this
const OUT = path.resolve(__dirname, '../test-results');

type Result = { id: string; title: string; status: 'PASS' | 'FAIL'; error?: string; screenshot?: string };
const results: Result[] = [];
let page: Page;
let info: TestInfo;

/** Run one plan step; record the outcome and keep going on failure. */
async function step(id: string, title: string, fn: () => Promise<void>) {
  let err: unknown;
  await test.step(`${id}. ${title}`, async () => {
    try { await fn(); } catch (e) { err = e; }
  });
  const shot = path.join(OUT, 'steps', `${id}.png`);
  await page.screenshot({ path: shot }).catch(() => {});
  await info.attach(`step ${id}`, { path: shot, contentType: 'image/png' }).catch(() => {});
  const error = err ? String((err as Error).message ?? err).split('\n').slice(0, 8).join('\n') : undefined;
  results.push({ id, title, status: err ? 'FAIL' : 'PASS', error, screenshot: shot });
}

// Real-outcome helper: read what the terminal actually shows, not whether it exists.
const termText = (name: string) =>
  page.locator(`[data-pane="${name}"] .xterm-rows`).first().innerText().catch(() => '');

test.afterAll(async () => {
  // Remove only resources named with PREFIX; never touch anything else.
});

test('Manual QA plan against the live stack (one continuous session)', async ({ page: p }, testInfo) => {
  test.setTimeout(8 * 60_000);
  page = p;
  info = testInfo;
  fs.mkdirSync(path.join(OUT, 'steps'), { recursive: true });
  await page.goto('/');

  await step('0', 'Preflight: app reachable and connected', async () => {
    await expect(page.getByTestId('connection-chip')).toContainText('Connected');
  });

  await step('1', 'Send a command: its output appears in the terminal', async () => {
    await page.getByPlaceholder('Command').fill(`echo ${PREFIX}ok`);
    await page.keyboard.press('Enter');
    await expect.poll(() => termText(`${PREFIX}a`), { timeout: 15_000 }).toMatch(new RegExp(`^${PREFIX}ok\\s*$`, 'm'));
  });

  fs.writeFileSync(path.join(OUT, 'step-results.json'), JSON.stringify(results, null, 2));
  const failed = results.filter((r) => r.status === 'FAIL');
  expect(failed.map((f) => `${f.id}: ${f.title}`), `${failed.length} QA step(s) failed`).toEqual([]);
});

// Steps that cannot be automated safely; the reason is the point.
test.fixme('2. Backend stopped: UI shows a notice', async () => {
  // Needs stopping the shared backend; this driver never starts or stops servers.
});
