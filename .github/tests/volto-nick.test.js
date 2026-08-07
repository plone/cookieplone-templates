const { test, expect } = require('@playwright/test');

test('Volto renders content served by Nick', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:3000/');

  expect(response).not.toBeNull();
  expect(response.ok()).toBeTruthy();
  await expect(
    page.getByRole('heading', { name: 'Welcome to Nick!' }),
  ).toBeVisible({ timeout: 30_000 });
});
