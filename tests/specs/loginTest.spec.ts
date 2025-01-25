import { test, expect } from "../fixtures/cmsFixture.ts";
import { users, fakeUser } from "../data/users";

test.describe("Test login and navigate to dashboard", () => {

  for (const { username, password } of users) {
    test(`(Positive Scenario) Login as ${username} and go to dashboard`, async ({ loginPage, dashboardPage }) => {
      await loginPage.navigateToAndVisible();
      await loginPage.startLogin(username, password);
      await dashboardPage.navigateToAndVisible();
    });
  };

  test("Login for non-existing user", async ({ loginPage }) => {
    await loginPage.navigateToAndVisible();
    await loginPage.startLogin(fakeUser.username, fakeUser.password);
    await loginPage.warningMessage();
  });

})
