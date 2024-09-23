from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages

from .models import Patient
from .forms import PatientRegistrationForm


# Create your views here.
def home(request):
    context = {
        "title": "Home",
    }
    return render(request, "clinic/index.html", context)


def patient_list(request):
    patients = get_list_or_404(Patient)

    context = {
        "patients": patients,
    }

    return render(request, "clinic/patient_list.html", context)


def patient_data(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    context = {
        "patient": patient,
        "title": f"{patient.first_name} Details",
    }
    return render(request, "clinic/patient_details.html", context)


def register_patient(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            form.save()
            messages.success(request, f"{first_name} registered.")
            return redirect("clinic:home")
    else:
        form = PatientRegistrationForm()

    context = {
        "form": form,
        "title": "Patient Registration",
    }

    return render(request, "clinic/register_patient.html", context)
