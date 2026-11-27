import { expect, test } from '@playwright/test';

test('renders Plone Aurora on the homepage', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('Plone Aurora')).toBeVisible();
});
