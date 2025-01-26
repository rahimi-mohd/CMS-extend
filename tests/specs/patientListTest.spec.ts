import { expect, test } from "../fixtures/cmsFixture";
import { users } from "../data/users";
import { patients } from "../data/patients";

test.describe("Test patient list page", () => {
    test.beforeEach(async ({ loginPage }) => {
        await loginPage.navigateToAndVisible();
        await loginPage.startLogin(users.admin.username, users.admin.password);
    })

    test("Verified page visible", async ({ loginPage, patientListPage }) => {
        await patientListPage.navigateToAndVisible();
    });

    // for (const { firstName, lastName } of patients) {
    //     test(`Verify ${firstName} can click on view button and redirect to patient profile page`, async ({ patientListPage, page }) => {
    //         const patientName = `${firstName} ${lastName}`;
    //         const patientNameRegex = new RegExp(patientName, "i");

    //         await page.getByRole("row", { name: patientNameRegex })
    //             .getByRole("link", { name: "View" }).click()

    //         await expect(page.getByRole('heading', { name: 'Patient Profile' })).toBeVisible();

    //     });

    // };


    for (const { firstName, lastName } of patients) {
        test(`Verify ${firstName} can click on view button and redirect to patient profile page`, async ({ patientListPage, page }) => {
            const patientName = `${firstName} ${lastName}`;
            const patientNameRegex = new RegExp(patientName, "i");

            await page.locator('tr', { hasText: new RegExp(`${firstName} ${lastName}`, "i") }).locator('a', { hasText: "View" }).click();

            await expect(page.getByRole('heading', { name: 'Patient Profile' })).toBeVisible();

        });

    };


})