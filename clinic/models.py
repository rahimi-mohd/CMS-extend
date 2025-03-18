from django.db import models
from django.utils import timezone

from accounts.models import Profile

from datetime import date

# Create your models here.
TITLE_CHOICES = {
    1: "Mr.",
    2: "Mrs.",
    3: "Ms.",
}


class Patient(models.Model):
    class Meta:
        permissions = [
            ("can_register", "Can register new patient"),
        ]

    title = models.IntegerField(choices=TITLE_CHOICES, default=1, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    ic_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    register_date = models.DateTimeField(
        verbose_name="register_date", default=timezone.now
    )

    def __str__(self):
        return self.first_name


class Medicine(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    dosage_form = models.CharField(max_length=50)
    indication = models.CharField(max_length=50)
    strength = models.IntegerField(default=1)  # in mg
    quantity_in_stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} {self.strength}mg"


class Appointment(models.Model):
    TIMESLOT_LIST = {
        0: "9:00 - 10:00",
        1: "10:00 - 11:00",
        2: "11:00 - 12:00",
        3: "12:00 - 01:00",
        # doctor lunch break 1pm - 3pm
        4: "03:00 - 04:00",
        5: "04:00 - 05:00",
        6: "05:00 - 06:00",
    }

    STATUS_LISTS = {
        1: "Scheduled",
        2: "Completed",
        3: "No Show",
    }

    class Meta:
        # patient, timeslot and date have to be unique
        unique_together = ["time_slot", "date"]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    time_slot = models.IntegerField(choices=TIMESLOT_LIST)
    status = models.IntegerField(choices=STATUS_LISTS, default=1)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.description


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    medicine = models.ManyToManyField(Medicine, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    record_date = models.DateTimeField(verbose_name="record_date", default=timezone.now)
    medical_leave = models.IntegerField(
        default=0
    )  # to record if patient get any medical leaves
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.doctor.user_type != Profile.UserType.DOCTOR:
            raise ValueError("Selected user is not a doctor.")
        super().save(*args, **kwargs)


class Checkin(models.Model):
    CHECKIN_STATUS = {
        1: "waiting",
        2: "done",
    }
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CHECKIN_STATUS, default=1)
    date = models.DateField(auto_now_add=True)
    medical_record = models.OneToOneField(
        MedicalRecord, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.patient.first_name} checkin at {self.date}"


class Payment(models.Model):
    PAYMENT_STATUS = {
        1: "unpaid",
        2: "paid",
    }
    PAYMENT_TYPE = {
        1: "cash",
        2: "card",
    }
    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=1)
    payment_type = models.IntegerField(choices=PAYMENT_TYPE, default=1)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.medical_record.title} - Status: {self.get_payment_status_display()} "
