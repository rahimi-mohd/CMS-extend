from django.db import models
from django.utils import timezone

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
