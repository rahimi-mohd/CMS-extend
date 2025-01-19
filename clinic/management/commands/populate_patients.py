import random
from faker import Faker
from django.core.management.base import BaseCommand
from clinic.models import Patient  # Import Patient model from clinic.models

# Define TITLE_CHOICES (same as in your model)
TITLE_CHOICES = [(1, "Mr."), (2, "Mrs."), (3, "Ms.")]

class Command(BaseCommand):
    help = "Populate the database with fake patients"

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(20):  # Number of patients to create
            # Randomly choose a title
            title = random.choice([choice[0] for choice in TITLE_CHOICES])  # Get the integer value
            first_name = fake.first_name()
            last_name = fake.last_name()
            ic_number = str(fake.unique.random_number(digits=12, fix_len=True))
            email = fake.unique.email()
            phone_number = fake.unique.phone_number()
            register_date = fake.date_time_this_year()

            # Create and save the patient instance
            patient = Patient.objects.create(
                title=title,
                first_name=first_name,
                last_name=last_name,
                ic_number=ic_number,
                email=email,
                phone_number=phone_number,
                register_date=register_date,
            )
            # Print success message
            print(f"Created patient: {patient.first_name} {patient.last_name}, Title: {dict(TITLE_CHOICES)[title]}")
