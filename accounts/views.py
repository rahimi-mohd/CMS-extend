from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomUserCreationForm


# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            messages.success(request, f"{username} register successfully.")
            return redirect("clinic:home")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
        "title": "User Registration",
    }

    return render(request, "accounts/user_registration.html", context)


def user_profile(request, pk):
    user = request.user

    context = {
        "user": user,
        "title": f"{user.username}'s Profile",
    }
    return render(request, "accounts/user_profile.html", context)
