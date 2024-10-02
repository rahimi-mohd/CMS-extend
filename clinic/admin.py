from django.contrib import admin

from .models import Patient, Checkin, MedicalRecord, Payment, Appointment, Medicine

# Register your models here.
admin.site.register(Patient)
admin.site.register(Checkin)
# admin.site.register(MedicalRecord)
admin.site.register(Payment)
admin.site.register(Appointment)
# admin.site.register(Medicine)


class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "doctor",
        "title",
        "record_date",
        "medical_leave",
        "price",
    ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "medicine":
            # Only show medicines that are related to the current medical record
            # This could be filtered further if needed
            kwargs["queryset"] = Medicine.objects.filter(quantity_in_stock__gt=0)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Medicine)  # Ensure Medicine is also registered if not already
