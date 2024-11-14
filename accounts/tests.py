from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class MyViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="12")

    def test_view_without_login(self):
        response = self.client.get(reverse('clinic:home'))
        self.assertRedirects(response, reverse('accounts:login') + '?next=' + reverse('clinic:home'))

    def test_view_with_login(self):
        self.client.login(username="admin", password="12")
        response = self.client.get(reverse("clinic:home"))
        self.assertEqual(response.status_code, 200)