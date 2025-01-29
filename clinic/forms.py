from django import forms
from django.db.models.expressions import fields
from django.forms import ModelForm

from .models import Patient, MedicalRecord, Appointment, Checkin, Payment, Medicine

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
    medicines = forms.ModelMultipleChoiceField(
        queryset=Medicine.objects.all().exclude(quantity_in_stock__lte=0),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = MedicalRecord
        fields = [
            # "doctor",
            "title",
            "description",
            "medical_leave",
            "medicines",
            "price",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for medicine in self.fields["medicines"].queryset:
            medicine_quantity = medicine.quantity_in_stock
            # You can customize the label to include the quantity
            self.fields["medicines"].label_from_instance = (
                lambda obj: f"{obj.name} (Stock: {medicine_quantity})"
            )


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


class InventoryAddItemForm(forms.Form):
    amount = forms.IntegerField(label="Enter amount")
