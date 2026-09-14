import { expect, test } from './test';
import { expectNoAccessibilityViolations } from './accessibility';

test.describe('Homepage', () => {
  test('renders with no automatic accessibility violations', async ({
    page,
  }) => {
    const response = await page.goto('/', { waitUntil: 'networkidle' });

    expect(response?.ok()).toBeTruthy();

    await expectNoAccessibilityViolations(page, {
      // Baseline exceptions for the stock Aurora app shell: the default site
      // root omits an h1 and a top-level <main> landmark. Everything else
      // (contrast, labels, ARIA, …) is still asserted.
      disabledRules: ['page-has-heading-one', 'landmark-one-main'],
    });
  });
});
