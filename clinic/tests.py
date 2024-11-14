from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.db.models import Q

from clinic.models import Patient

class PatientListViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="12")
        self.client = Client()

        self.patient1 = Patient.objects.create(first_name="Abu", last_name="Bakar", phone_number="0000", ic_number="1")
        self.patient2 = Patient.objects.create(first_name="Chong", last_name="Eng", phone_number="1111", ic_number="2")
        self.patient3 = Patient.objects.create(first_name="Rama", last_name="Chandran", phone_number="2222", ic_number="3")

    def test_patient_list_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("clinic:patient_list"))
        self.assertRedirects(response, reverse('accounts:login') + '?next=' + reverse('clinic:patient_list'))

    def test_patient_list_displays_all_patients_if_logged_in(self):
        self.client.login(username="admin", password="12")
        response = self.client.get(reverse("clinic:patient_list"))
        self.assertEqual(response.status_code, 200)

        # get all patient into context, then check if they're in the list
        patient_in_context = response.context["patients"]
        self.assertEqual(list(patient_in_context), [self.patient1, self.patient2, self.patient3])

    def test_patient_list_filters_patients_based_on_search_query(self):
        self.client.login(username="admin", password="12")
        response = self.client.get(reverse("clinic:patient_list"), {"search": "Abu"})
        self.assertEqual(response.status_code, 200)

        patients_in_context = response.context["patients"]
        expected_patients = Patient.objects.filter(
            Q(first_name__icontains="Abu") | Q(last_name__icontains="Bakar")
        )

        self.assertEqual(list(patients_in_context), list(expected_patients))