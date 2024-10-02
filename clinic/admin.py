from django.contrib import admin

from .models import Patient, Checkin, MedicalRecord, Payment, Appointment, Medicine

# Register your models here.
admin.site.register(Patient)
admin.site.register(Checkin)
admin.site.register(MedicalRecord)
admin.site.register(Payment)
admin.site.register(Appointment)
admin.site.register(Medicine)
