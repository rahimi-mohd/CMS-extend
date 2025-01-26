import { test as base, expect } from "@playwright/test";
import { LoginPage } from "../pages/loginPage";
import { DashboardPage } from "../pages/dashboardPage";
import { PatientListPage } from "../pages/patientListPage";

type CmsFixture = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  patientListPage: PatientListPage;
};

export const test = base.extend<CmsFixture>({

  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },
  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },
  patientListPage: async ({ page }, use) => {
    const patientListPage = new PatientListPage(page);
    await use(patientListPage);
  },
});

export { expect };
