from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages

from .models import Patient, MedicalRecord
from .forms import PatientRegistrationForm, MedicalRecordUpdateForm


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
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by(
        "-record_date"
    )
    context = {
        "medical_records": medical_records,
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


def add_medical_record(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = MedicalRecordUpdateForm(request.POST)
        if form.is_valid():
            record_title = form.cleaned_data.get("title")
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            messages.success(request, f"{record_title} added.")
    else:
        form = MedicalRecordUpdateForm()

    context = {
        "patient": patient,
        "form": form,
        "title": "Medical Record",
    }

    return render(request, "clinic/add_medical_record.html", context)
