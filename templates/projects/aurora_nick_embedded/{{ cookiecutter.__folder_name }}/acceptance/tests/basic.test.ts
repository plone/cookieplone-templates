import { expect, test } from '../../core/packages/tooling/playwright/test';

test('renders Plone 7 on the homepage', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('Plone 7')).toBeVisible();
});
