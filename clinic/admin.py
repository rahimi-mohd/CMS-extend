from django.contrib import admin

from .models import Patient, Checkin, MedicalRecord, Payment

# Register your models here.
admin.site.register(Patient)
admin.site.register(Checkin)
admin.site.register(MedicalRecord)
admin.site.register(Payment)
