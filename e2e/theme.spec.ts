import { test, expect } from '@playwright/test'

test('light/dark theme toggle updates DOM and persists', async ({ page }) => {
  await page.goto('/index.html')

  const getTheme = async () => page.evaluate(() => document.documentElement.dataset.theme)

  // initial theme should be light or dark; normalize to setting known value first
  await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; localStorage.setItem('theme','light') })
  await page.reload()
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'light')

  await page.getByRole('button', { name: 'Toggle theme' }).click()
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark')

  // reload should keep dark
  await page.reload()
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark')
})

test('create page has toggle and editors render', async ({ page }) => {
  await page.goto('/create.html')
  await expect(page.getByRole('button', { name: 'Toggle theme' })).toBeVisible()
  await expect(page.locator('#input-yaml')).toBeVisible()
  await expect(page.locator('#output-text')).toBeVisible()
})

test('export page has toggle and input editor renders', async ({ page }) => {
  await page.goto('/export.html')
  await expect(page.getByRole('button', { name: 'Toggle theme' })).toBeVisible()
  await expect(page.locator('#input-yaml')).toBeVisible()
})

test('export page output editor theme follows toggle', async ({ page }) => {
  // Force light first
  await page.goto('/export.html')
  await page.evaluate(() => { document.documentElement.dataset.theme = 'light'; localStorage.setItem('theme','light') })
  await page.reload()
  const scroller = page.locator('#output-text .ace_scroller')
  await expect(scroller).toBeVisible()
  const before = await scroller.evaluate(el => getComputedStyle(el).backgroundColor)
  await page.getByRole('button', { name: 'Toggle theme' }).click()
  // wait a tick for Ace to apply theme
  await page.waitForTimeout(100)
  const after = await scroller.evaluate(el => getComputedStyle(el).backgroundColor)
  expect(before).not.toBe(after)
})



