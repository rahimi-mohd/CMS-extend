import { expect, type Locator, type Page } from "@playwright/test";

export class PatientListPage {
    readonly page: Page;
    readonly header: Locator;

    constructor(page: Page) {
        this.page = page;
        this.header = page.getByRole("heading", { name: "Patient List" })
    }

    async navigateToAndVisible() {
        await this.page.goto("./patient_list");
        await expect(this.header).toBeVisible();

    }

}

