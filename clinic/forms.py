from django.forms import ModelForm

from .models import Patient
from .models import MedicalRecord


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
            "title",
            "description",
        ]
