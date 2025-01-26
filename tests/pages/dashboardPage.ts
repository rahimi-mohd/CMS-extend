import { expect, type Locator, type Page } from "@playwright/test";

export class DashboardPage {
  readonly page: Page;
  readonly patientListMenu: Locator;
  readonly appointmentListMenu: Locator;
  readonly checkInListMenu: Locator;


  constructor(page: Page) {
    this.page = page;
    this.patientListMenu = page.getByRole('link', { name: 'Patient List' });
    this.appointmentListMenu = page.getByRole('link', { name: 'Appointment List' });
    this.checkInListMenu = page.getByRole('link', { name: 'Check-In List' });
  };

  async navigateToAndVisible() {
    await this.page.goto("/");
    await expect(this.patientListMenu).toBeVisible();
    await expect(this.appointmentListMenu).toBeVisible();
    await expect(this.checkInListMenu).toBeVisible();
  }

  async clickPatientList() {
    await this.patientListMenu.click();
  }
  async clickAppointmentList() {
    await this.appointmentListMenu.click();
  }
  async clickCheckInList() {
    await this.checkInListMenu.click();
  }

}


