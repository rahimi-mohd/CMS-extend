from django.forms import ModelForm

from .models import Patient


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
