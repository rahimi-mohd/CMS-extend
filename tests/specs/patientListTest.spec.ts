import { expect, test } from "../fixtures/cmsFixture";
import { users } from "../data/users";
import { patients } from "../data/patients";
import exp from "constants";

test.describe("Test patient list page", () => {
    test.beforeEach(async ({ loginPage, patientListPage }) => {
        await loginPage.navigateToAndVisible();
        await loginPage.startLogin(users.admin.username, users.admin.password);
        await patientListPage.navigateToAndVisible();
    });


    for (const { firstName, lastName } of patients) {
        test(`Verify ${firstName} can click on the View button and redirect to the patient profile page`, async ({ page }) => {
            const patientName = `${firstName} ${lastName}`; // Combine first and last name dynamically
            const patientNameRegex = new RegExp(patientName, "i"); // Create a case-insensitive regex

            // Locate the row dynamically using the patient's name
            const row = page.locator("table#patient-list tr", {
                hasText: patientNameRegex
            });

            // Within the row, locate the "View" button and click
            await row.locator("a", { hasText: "View" }).click();

            // Verify that the patient profile page is displayed
            await expect(page.getByRole("heading", { name: "Patient Profile" })).toBeVisible();
        });
    };

    for (const { firstName, lastName } of patients) {
        test(`${firstName} can be search using the search function`, async ({ patientListPage, page }) => {
            await patientListPage.searchName(firstName);
            await expect(page.getByRole("cell", { name: `${firstName} ${lastName}` })).toBeVisible()

        });

        test(`${lastName} can be search using the search function`, async ({ patientListPage, page }) => {
            await patientListPage.searchName(lastName);
            await expect(page.getByRole("cell", { name: `${firstName} ${lastName}` })).toBeVisible()
        });
    }


})