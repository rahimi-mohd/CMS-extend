from django.test import TestCase

# Create your tests here.
# class HomePageTest(TestCase):
#     def test_home_page_returns_correct_html(self):
#         response = self.client.get("/")
#         self.assertContains(response, "<title>Home</title>")

class LoginPageTest(TestCase):
    def test_login_page(self):
        response = self.client.get("/login")
        self.assertContains(response, "<title>CMS</title>")