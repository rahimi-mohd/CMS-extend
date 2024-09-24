from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    class UserType(models.IntegerChoices):
        CLINIC_STAFF = 1, "Clinic Staff"
        DOCTOR = 2, "Doctor"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(
        choices=UserType.choices, default=UserType.CLINIC_STAFF
    )
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    ic_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    register_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
