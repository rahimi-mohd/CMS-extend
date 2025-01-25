import { expect, type Locator, type Page } from "@playwright/test";

export class DashboardPage {
  readonly page: Page;
  readonly header1: Locator;
  readonly header2: Locator;
  readonly header3: Locator;


  constructor(page: Page) {
    this.page = page;
    this.header1 = page.getByRole('link', { name: 'Patient List' });
    this.header2 = page.getByRole('link', { name: 'Appointment List' });
    this.header3 = page.getByRole('heading', { name: 'Clinic Management System' });
  };

  async navigateToAndVisible() {
    await this.page.goto("/");
    await expect(this.header1).toBeVisible();
    await expect(this.header2).toBeVisible();
    await expect(this.header3).toBeVisible();

  }

}


