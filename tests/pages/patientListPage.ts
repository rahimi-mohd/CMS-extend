import { expect, type Locator, type Page } from "@playwright/test";

export class PatientListPage {
    readonly page: Page;
    readonly header: Locator;
    readonly searchInput: Locator;
    readonly searchBtn: Locator;

    constructor(page: Page) {
        this.page = page;
        this.header = page.getByRole("heading", { name: "Patient List" });
        this.searchInput = page.getByPlaceholder("Search Patient");
        this.searchBtn = page.getByRole("button", { name: "Search" });
    }

    async navigateToAndVisible() {
        await this.page.goto("./patient_list");
        await expect(this.header).toBeVisible();
    }

    async searchName(name: string) {
        await this.searchInput.fill(name);
        await this.searchBtn.click();
    }

}

