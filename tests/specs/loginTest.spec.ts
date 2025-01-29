import { test, expect } from "../fixtures/cmsFixture.ts";
import { users, fakeUser } from "../data/users";

test.describe("Test login and navigate to dashboard", () => {

  for (const role of Object.keys(users)) {
    test(`(Positive Scenario) Login as ${role} and go to dashboard`, async ({ loginAs, dashboardPage }) => {
      await loginAs(role as keyof typeof users);
      await dashboardPage.navigateToAndVisible();
    });
  };

  test("Login for non-existing user", async ({ loginPage }) => {
    await loginPage.navigateToAndVisible();
    await loginPage.startLogin(fakeUser.username, fakeUser.password);
    await loginPage.warningMessage();
  });

})
