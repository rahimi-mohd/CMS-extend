import pytest
from playwright.sync_api import Page, expect
from config import User, Patient

URL = "http://localhost:8000"
# list of users
admin = User("admin", "12", "Admin")
clinic_staff = User("staff1", "bingo132$", "Staff")
doctor = User("doctor1", "dd-1-clinic", "Doctor")
not_existed_user = User("not_existed", "never_registered", "Not Existed")

# list of patients
# TODO: add another generic patient instead of using real name
patient1 = Patient("Patient1", "Generic", "121212121212", "090900901111")


# browser context
@pytest.fixture(scope="session")
def browser_context(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture
def page(browser_context):
    context = browser_context.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def user(request):
    return request.param


def login(page: Page, user: User):
    page.goto(URL)
    page.get_by_label("Username").fill(user.username)
    page.get_by_label("Password").fill(user.password)
    page.get_by_role("button", name="Login").click()

    if user == not_existed_user:
        expect(
            page.get_by_text(
                "Please enter a correct username and password. Note that both fields may be case-sensitive."
            )
        ).to_be_visible()
    else:
        expect(page.get_by_text(f"Welcome, {user.user_type} {user.username.title()}."))


def logout(page: Page, user: User):
    if user != not_existed_user:
        page.get_by_role("button", name=f"{user.username.title()}").click()
        page.get_by_role("button", name="Logout").click()
        expect(page.get_by_role("button", name="Login")).to_be_visible()


@pytest.mark.parametrize(
    "user", [admin, clinic_staff, doctor, not_existed_user], indirect=True
)
def test_user_can_login_and_logout(page: Page, user: User):
    login(page, user)
    if user != not_existed_user:
        logout(page, user)


# dashboard test


def dashboard(page: Page, user: User):
    expect(page.get_by_text("Clinic Management System")).to_be_visible
    # get the Patient List's button
    expect(page.get_by_role("link", name="Patient List")).to_be_visible()
    # get the Appointment List's button
    expect(page.get_by_role("link", name="Appointment List")).to_be_visible()
    # get the Check-In List's button
    expect(page.get_by_role("link", name="Check-In List")).to_be_visible()


@pytest.mark.parametrize(
    "user", [admin, clinic_staff, doctor, not_existed_user], indirect=True
)
def test_user_can_see_dashboard(page: Page, user: User):
    login(page, user)
    if user != not_existed_user:
        dashboard(page, user)


def patient_list_page(page: Page, user: User):
    # user click on the Patient List button
    page.get_by_role("link", name="Patient list").click()
    # user can see input with "Search patient" placeholder and Search button
    expect(page.get_by_placeholder("Search patient")).to_be_visible()
    expect(page.get_by_role("button", name="Search")).to_be_visible()
    # verified that user can see "Patient List" header
    expect(page.get_by_text("Patient List")).to_be_visible()
    # verified that user can see table header with #, Full Name and Action
    expect(page.get_by_role("table").filter(has_text="#")).to_be_visible()
    expect(page.get_by_role("table").filter(has_text="Full Name")).to_be_visible()
    expect(page.get_by_role("table").filter(has_text="Action")).to_be_visible()
    # verified that user can see 1, patient first name + last name, View button
    expect(page.get_by_role("table").filter(has_text="1")).to_be_visible()
    expect(
        page.get_by_role("table").filter(
            has_text=f"{patient1.first_name} {patient1.last_name}"
        )
    ).to_be_visible()
    expect(page.get_by_role("link", name="View")).to_be_visible()
    # verified that user can see Register New Patient button
    expect(page.get_by_role("button", name="Register New Patient")).to_be_visible()


@pytest.mark.parametrize("user", [clinic_staff], indirect=True)
def test_patient_list_page(page: Page, user: User):
    login(page, user)
    patient_list_page(page, user)
