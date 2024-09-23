from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.db.models import Q

from .models import Patient, MedicalRecord, Appointment
from .forms import PatientRegistrationForm, MedicalRecordUpdateForm, AddAppointmentForm


# Create your views here.
@login_required
def home(request):
    # current_user = request.user
    context = {
        # "user": current_user.username,
        "title": "Home",
    }
    return render(request, "clinic/index.html", context)


@login_required
def patient_list(request):
    query = request.GET.get("search", "")
    if query:
        patients = Patient.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        patients = Patient.objects.all()

    context = {
        "patients": patients,
        "search_query": query,
        "title": "Patient List",
    }

    return render(request, "clinic/patient_list.html", context)


@login_required
def patient_data(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by(
        "-record_date"
    )
    past_appointments = Appointment.objects.filter(patient=patient, status__in=[2, 3])
    context = {
        "medical_records": medical_records,
        "past_appointments": past_appointments,
        "patient": patient,
        "title": f"{patient.first_name} Details",
    }
    return render(request, "clinic/patient_details.html", context)


@login_required
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


@login_required
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
            return redirect("clinic:patient_data", pk=pk)
    else:
        form = MedicalRecordUpdateForm()

    context = {
        "patient": patient,
        "form": form,
        "title": "Medical Record",
    }

    return render(request, "clinic/add_medical_record.html", context)


@login_required
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


@login_required
def appointment_list(request):
    appointment_list = Appointment.objects.all().order_by("-date")
    context = {
        "appointment_list": appointment_list,
        "title": "List Of Appointment",
    }
    return render(request, "clinic/list_of_appointment.html", context)


@login_required
def change_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if appointment.status == 1:
        appointment.status = 2
        appointment.save()
    elif appointment.status == 2:
        appointment.status = 3
        appointment.save()

    return redirect("clinic:appointment_list")
