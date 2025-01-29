import csv
import os
import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.conf import settings
from clinic.models import Medicine, Patient  # Adjust this import as necessary

# Define TITLE_CHOICES (same as in your model)
TITLE_CHOICES = [(1, "Mr."), (2, "Mrs."), (3, "Ms.")]

class Command(BaseCommand):
    help = "Populate the database with medicines or fake patients."

    def add_arguments(self, parser):
        parser.add_argument(
            '--medicines',
            action='store_true',
            help='Populate the database with medicines from CSV'
        )
        parser.add_argument(
            '--patients',
            action='store_true',
            help='Populate the database with fake patients'
        )

    def handle(self, *args, **kwargs):
        if kwargs['medicines']:
            self.populate_medicines()
        elif kwargs['patients']:
            self.populate_patients()
        else:
            self.stderr.write(self.style.ERROR("Please specify --medicines or --patients"))

    def populate_medicines(self):
        file_path = os.path.join(settings.BASE_DIR, "clinic", "data", "medicine_dataset.csv")  # Adjust path if needed
        
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR("CSV file not found."))
            return
        
        try:
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                
                medicines = []
                for row in reader:
                    strength_value = row["Strength"].replace("mg", "").strip()
                    
                    medicine = Medicine(
                        name=row["Name"],
                        category=row["Category"],
                        dosage_form=row["Dosage Form"],
                        indication=row["Indication"],
                        strength=int(strength_value),
                    )
                    medicines.append(medicine)
                
                Medicine.objects.bulk_create(medicines)  # Bulk insert for efficiency
                self.stdout.write(self.style.SUCCESS("Medicines imported successfully!"))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {str(e)}"))
    
    def populate_patients(self):
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
