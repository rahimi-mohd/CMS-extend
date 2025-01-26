import { test, expect } from "../fixtures/cmsFixture.ts";
import { users } from "../data/users";

test.describe("Test user can see their username on the screen", () => {

    for (const [role, { username, password }] of Object.entries(users)) {
        test(`Verified that ${username} can see their username on dashboard`, async ({ loginPage, dashboardPage, page }) => {
            await loginPage.navigateToAndVisible();
            await loginPage.startLogin(username, password);
            await dashboardPage.navigateToAndVisible();
            await expect(page.getByText(`Hello, ${username} Good to see you!`)).toBeVisible();
        });
    };
})

test.describe("Test main menu items can be click", () => {
    test.beforeEach(async ({ loginPage }) => {
        loginPage.navigateToAndVisible();
        loginPage.startLogin(users.admin.username, users.admin.password);
    })

    test("can click Patient List", async ({ dashboardPage, page }) => {
        await dashboardPage.clickPatientList();
        await expect(page.getByRole('heading', { name: 'Patient List' })).toBeVisible();
    });

    test("can click Appointment List", async ({ dashboardPage, page }) => {
        await dashboardPage.clickAppointmentList();
        await expect(page.getByRole('heading', { name: 'Future\'s Appointment' })).toBeVisible();
    });

    test("can click Check-In List", async ({ dashboardPage, page }) => {
        await dashboardPage.clickCheckInList();
        await expect(page.getByRole('heading', { name: 'Check In List' })).toBeVisible();
    });


})