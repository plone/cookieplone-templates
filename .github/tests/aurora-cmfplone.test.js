const { test, expect } = require('@playwright/test');

test('Aurora renders content served by the Plone backend', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:3000/');

  expect(response).not.toBeNull();
  expect(response.ok()).toBeTruthy();
  await expect(
    page.getByText('Welcome to your new Plone site!').first(),
  ).toBeVisible({
    timeout: 30_000,
  });
});
