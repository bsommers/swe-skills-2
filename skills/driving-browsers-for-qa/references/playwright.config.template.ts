import { defineConfig } from '@playwright/test';

const baseURL = process.env.QA_BASE_URL ?? 'http://localhost:3000';

export default defineConfig({
  testDir: './e2e',
  testMatch: '**/*.e2e.ts', // keeps vitest/jest from collecting these
  outputDir: './test-results',
  workers: 1,
  fullyParallel: false,
  retries: 0,
  timeout: 45_000,
  expect: { timeout: 10_000 },
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'playwright-report' }]],
  use: {
    baseURL,
    channel: 'chrome', // system Chrome; remove if only a cached Playwright browser matches
    viewport: { width: 1440, height: 900 },
    video: 'on',
    screenshot: 'on',
    trace: 'retain-on-failure',
    actionTimeout: 8_000,
  },
});
