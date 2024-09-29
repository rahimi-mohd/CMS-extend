import pytest
import re
from playwright.sync_api import Page, expect

from config import User

URL = "http://localhost:8000"

# list of users
admin = User("admin", "12", "Admin")
clinic_staff = User("staff1", "bingo132$", "Staff")
doctor = User("doctor1", "dd-1-clinic", "Doctor")
not_existed_user = User("not_existed", "never_registered")


# login for admin
def test_admin_can_login_and_logout(page: Page):
    # admin go to the page
    page.goto(URL)

    # admin see a login page
    page.get_by_text("Login")

    # admin enter their username and password
    page.get_by_label("Username").fill(admin.username)
    page.get_by_label("Password").fill(admin.password)

    # admin click on login button
    page.get_by_role("button", name="Login").click()

    # admin see welcome message 'Welcome, Admin {admin username}.
    page.get_by_text(f"Welcome, {admin.user_type} {admin.username.title()}.")

    # admin try to click on nav button
    page.get_by_role("button", name=f"{admin.username.title()}").click()

    # admin click the logout button
    page.get_by_role("button", name="Logout").click()

    # admin redirect to login page
    expect(page.get_by_role("button", name="Login")).to_be_visible()
