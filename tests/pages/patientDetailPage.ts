import { expect, type Locator, type Page } from "@playwright/test";

export class PatientDetailPage {
    readonly page: Page;


    constructor(page: Page) {
        this.page = page;
    };

    async navigateToAndVisible() {
        await this.page.goto("/");
    }


}
