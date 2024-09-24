from django.db import models
from django.utils import timezone

from accounts.models import Profile

# Create your models here.
TITLE_CHOICES = {
    1: "Mr.",
    2: "Mrs.",
    3: "Ms.",
}


class Patient(models.Model):
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


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    record_date = models.DateTimeField(verbose_name="record_date", default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.doctor.user_type != Profile.UserType.DOCTOR:
            raise ValueError("Selected user is not a doctor.")
        super().save(*args, **kwargs)


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
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description
