import { test, expect } from '@playwright/test';

const admin = {
    username: "admin",
    password: "12",
};

test.describe("Test login page", () => {
    test.beforeEach(async ({ page }) => {
        await page.goto("/");
    })
    test('test admin account', async ({ page }) => {

        // make sure the login page element is visible
        await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();

        // fill in the username and password input
        await page.getByLabel('Username*').fill(admin.username);
        await page.getByLabel('Password*').fill(admin.password);

        // click the login button
        await page.getByRole('button', { name: 'Login' }).click();

        // make sure the dashboard is visible
        await expect(page.getByRole('heading', { name: 'Hello, Admin' })).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Clinic Management System' })).toBeVisible();
    });

})
