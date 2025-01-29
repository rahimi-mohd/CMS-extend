import { test, expect } from "../fixtures/cmsFixture.ts";
import { users } from "../data/users";

test.describe("Test user can see their username on the screen", () => {

    for (const role of Object.keys(users)) {
        test(`Verified that ${role} can see their username on dashboard`, async ({ loginAs, dashboardPage, page }) => {
            const user = users[role as keyof typeof users];
            await loginAs(role as keyof typeof users);
            await dashboardPage.navigateToAndVisible();
            await expect(page.getByText(`Hello, ${user.username} Good to see you!`)).toBeVisible();
        });
    };
})

test.describe("Test main menu items can be click", () => {
    test.beforeEach(async ({ loginAs }) => {
        await loginAs("admin");
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