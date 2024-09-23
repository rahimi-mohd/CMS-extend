from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import IntegrityError

from .models import Patient, MedicalRecord, Appointment
from .forms import PatientRegistrationForm, MedicalRecordUpdateForm, AddAppointmentForm


# Create your views here.
def home(request):
    context = {
        "title": "Home",
    }
    return render(request, "clinic/index.html", context)


def patient_list(request):
    # patients = get_list_or_404(Patient)
    patients = Patient.objects.all()

    context = {
        "patients": patients,
    }

    return render(request, "clinic/patient_list.html", context)


def patient_data(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by(
        "-record_date"
    )
    appointments = Appointment.objects.filter(patient=patient).order_by("-date")
    context = {
        "medical_records": medical_records,
        "appointments": appointments,
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


def add_appointment(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = AddAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            try:
                appointment.save()
                messages.success(request, f"appointment added.")
                return redirect("clinic:patient_data", pk=pk)
            except IntegrityError:
                messages.info(request, "Already existed")
                return redirect("clinic:patient_data", pk=pk)
    else:
        form = AddAppointmentForm()

    context = {
        "patient": patient,
        "form": form,
        "title": "Add Appointment",
    }

    return render(request, "clinic/add_appointment.html", context)


def appointment_list(request):
    appointment_list = get_list_or_404(Appointment)
    context = {
        "appointment_list": appointment_list,
        "title": "List Of Appointment",
    }
    return render(request, "clinic/list_of_appointment.html", context)
