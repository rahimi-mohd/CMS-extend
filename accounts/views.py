from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

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
    # users = User.objects.all()
    query = request.GET.get("search", "")

    if query:
        users = User.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(username__icontains=query)
        )
    else:
        users = User.objects.all()

    context = {
        "users": users,
        "title": "User List",
    }

    return render(request, "accounts/user_list.html", context)


@login_required
def update_user_profile(request, pk):
    """check if current logged in user is admin"""
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You have to be admin to access this page.")
        return redirect("accounts:user_list")

    """check if user already have a profile or not
    if not, create new profile for user
    Scenario: createsuperuser command create only the base user, not the profile,
    Register user without the profile also possible using the admin page."""
    try:
        user_profile = Profile.objects.get(user_id=pk)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user_id=pk)
        messages.warning(
            request,
            "Profile did't exist for this user, a new profile has been created.",
        )

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
