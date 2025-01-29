import { test as base, expect } from "@playwright/test";
import { LoginPage } from "../pages/loginPage";
import { DashboardPage } from "../pages/dashboardPage";
import { PatientListPage } from "../pages/patientListPage";

import { users } from "../data/users";

type UserRole = keyof typeof users;

type CmsFixture = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  patientListPage: PatientListPage;
  loginAs: (role: UserRole) => Promise<void>;
};

export const test = base.extend<CmsFixture>({
  loginAs: async ({ page }, use) => {
    await use(async (role: UserRole) => {
      const user = users[role];

      if (!user) {
        throw new Error(`Invalid role: ${role}. Check the "users" object in data/users.ts`);
      }

      const loginPage = new LoginPage(page);
      await loginPage.navigateToAndVisible();
      await loginPage.startLogin(user.username, user.password);

    });
  },

  // this line can be delete later
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
