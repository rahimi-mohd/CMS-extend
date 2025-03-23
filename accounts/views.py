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
    profile_user = get_object_or_404(User, pk=pk)
    context = {
        "profile_user": profile_user,
        "title": f"{profile_user.username}'s Profile",
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
    """Get or create profile if it doesn't exist"""
    user_profile, created = Profile.objects.get_or_create(user_id=pk)

    if created:
        messages.warning(request, "A new profile was created for this user.")

    """Check if the user is allowed to edit"""
    if not request.user.is_superuser and request.user.profile.user_type != "admin":
        # If not an admin, only allow editing their own profile
        if request.user.pk != user_profile.user.pk:
            messages.error(request, "You can only edit your own profile.")
            return redirect("accounts:edit_profile", pk=request.user.pk)  # Redirect to their own edit profile page

    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=user_profile.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:user_list" if request.user.profile.user_type == "admin" else "accounts:user_profile", pk=request.user.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = EditUserForm(instance=user_profile.user)
        profile_form = EditProfileForm(instance=user_profile)

    context = {
        "profile": user_profile,
        "user_form": user_form,
        "profile_form": profile_form,
        "title": "Update Profile",
    }

    return render(request, "accounts/update_user.html", context)
