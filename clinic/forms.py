from django import forms
from django.forms import ModelForm

from .models import Patient, MedicalRecord, Appointment, Checkin, Payment

from datetime import date


# forms
class PatientRegistrationForm(ModelForm):
    class Meta:
        model = Patient
        fields = [
            "title",
            "first_name",
            "last_name",
            "ic_number",
            "email",
            "phone_number",
        ]


class MedicalRecordUpdateForm(ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            "doctor",
            "title",
            "description",
            "medical_leave",
            "medicine",
            "price",
        ]


class AddAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "time_slot",
            "description",
            "date",
        ]
        widgets = {
            "date": forms.SelectDateWidget,
        }

    def clean(self):
        cleaned_data = super().clean()
        time_slot = cleaned_data.get("time_slot")
        date = cleaned_data.get("date")

        if date < date.today():
            raise forms.ValidationError("Appointment cannot be made for past dates.")

        if Appointment.objects.filter(time_slot=time_slot, date=date).exists():
            raise forms.ValidationError(
                "An appointment with the same patient, time slot and date already existed."
            )

        return cleaned_data


class CheckInForm(ModelForm):
    class Meta:
        model = Checkin
        fields = ["patient"]
        widgets = {
            "patient": forms.HiddenInput(),
        }


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_type"]
