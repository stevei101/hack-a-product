import { test, expect } from '@playwright/test';

test('should display the main heading', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Welcome to the Future' })).toBeVisible();
});
