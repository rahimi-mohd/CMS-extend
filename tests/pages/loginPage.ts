import { expect, type Locator, type Page } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly loginBtn: Locator;
  readonly header: Locator;
  readonly username: Locator;
  readonly password: Locator;
  readonly errMessage: Locator;


  constructor(page: Page) {
    this.page = page;
    this.header = page.getByRole('heading', { name: 'Login' });
    this.loginBtn = page.getByRole('button', { name: 'Login' });
    this.username = page.getByLabel('Username*');
    this.password = page.getByLabel('Password*');
    this.errMessage = page.getByText(("Please enter a correct"));
  };

  async navigateToAndVisible() {
    await this.page.goto("/");
    await expect(this.header).toBeVisible();
    await expect(this.loginBtn).toBeVisible();
  };

  async startLogin(username, password) {
    await this.username.fill(username);
    await this.password.fill(password);
    await this.loginBtn.click();
  };

  async warningMessage() {
    await expect(this.page.getByText('Please enter a correct')).toBeVisible();
  }

}
