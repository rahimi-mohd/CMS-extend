import { test, expect } from '@playwright/test';

const users = [
  // admin
  {
    username: "admin",
    password: "12",
  },
  // clinic staff
  {
    username: "sya",
    password: "bingo123#@!",
  },
  // doctor
  {
    username: "aira_aman",
    password: "bingo123#@!",
  }
]

// fake user
const fakeUser = {
  username: "fake",
  password: "fakePassword"
};

test.describe("Test login page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });
  users.forEach((user) => {
    test(`test ${user.username} account`, async ({ page }) => {

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
  });
  test("test for not-existed account", async ({ page }) => {
    // make sure the login page element is visible
    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();

    // fill in the username and password input
    await page.getByLabel('Username*').fill(fakeUser.username);
    await page.getByLabel('Password*').fill(fakeUser.password);

    // click the login button
    await page.getByRole('button', { name: 'Login' }).click();

    // make sure the alert work
    await expect(page.getByText('Please enter a correct')).toBeVisible();

  })

})
