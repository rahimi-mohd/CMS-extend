import { test, expect } from '@playwright/test';

const users = [
  {
    username: "admin",
    password: "12",
    roleName: "Admin",
  },
  {
    username: "clinic_staff",
    password: "bingo123#@!",
    roleName: "Clinic Staff",
  }
]

test.describe("Test login page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });
  users.forEach((user) => {
    test(`test ${user.roleName} account`, async ({ page }) => {

      // make sure the login page element is visible
      await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
      await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();

      // fill in the username and password input
      await page.getByLabel('Username*').fill(user.username);
      await page.getByLabel('Password*').fill(user.password);

      // click the login button
      await page.getByRole('button', { name: 'Login' }).click();

      // make sure the dashboard is visible
      // await expect(page.getByRole('heading', { name: `Hello, ${user.username}` })).toBeVisible();
      await expect(page.getByRole('link', { name: 'Patient List' })).toBeVisible();
      await expect(page.getByRole('link', { name: 'Appointment List' })).toBeVisible();
      await expect(page.getByRole('heading', { name: 'Clinic Management System' })).toBeVisible();
    });

  })

})
