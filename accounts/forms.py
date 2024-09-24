from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.UserType.choices, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    ic_number = forms.CharField(max_length=12, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        profile = Profile.objects.create(
            user=user,
            user_type=self.cleaned_data["user_type"],
            phone_number=self.cleaned_data.get("phone_number"),
            ic_number=self.cleaned_data.get("ic_number"),
        )

        return user
