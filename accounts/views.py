from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, EditUserForm, EditProfileForm
from .models import Profile


# Create your views here.
@login_required
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


@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {
        "user": user,
        "title": f"{user.username}'s Profile",
    }
    return render(request, "accounts/user_profile.html", context)


# this can be used by admin only!
@login_required
def user_list(request):
    users = User.objects.all()
    context = {
        "users": users,
        "title": "User List",
    }

    return render(request, "accounts/user_list.html", context)


# FIXME: this function return error if i want to edit my own profile?
@login_required
def update_user_profile(request, pk):
    """check if current logged in user is admin"""
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You have to be admin to access this page.")
        return redirect("accounts:user_list")

    user_profile = Profile.objects.get(user_id=pk)

    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=user_profile.user)
        profile_form = EditProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:user_list")
    else:
        user_form = EditUserForm()
        profile_form = EditProfileForm()

    context = {
        "profile": user_profile,
        "user_form": user_form,
        "profile_form": profile_form,
        "title": "Update Profile",
    }

    return render(request, "accounts/update_user.html", context)
