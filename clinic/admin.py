from django.contrib import admin

from .models import Patient, Checkin

# Register your models here.
admin.site.register(Patient)
admin.site.register(Checkin)
