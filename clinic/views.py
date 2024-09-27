from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q

from .models import Patient, MedicalRecord, Appointment, Checkin, Payment
from accounts.models import Profile
from .forms import (
    PatientRegistrationForm,
    MedicalRecordUpdateForm,
    AddAppointmentForm,
    PaymentForm,
)

from datetime import date


########################### home page ################################
@login_required
def home(request):
    # current_user = request.user
    context = {
        # "user": current_user.username,
        "title": "Home",
    }
    return render(request, "clinic/index.html", context)


########################### patient handling ################################
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


########################### medical records handling ################################
@login_required
def add_medical_record(request, pk):
    today = date.today()
    checkin = Checkin.objects.get(patient_id=pk, status=1, date=today)

    """check if the one updating this feature is doctor type user"""
    if request.user.profile.user_type != Profile.UserType.DOCTOR:
        messages.error(request, "You do not have permission to add medical records.")
        return redirect("clinic:checkin_list")

    """check if medical record already updated,
    to make sure that there's no duplicate medical record in one checkin"""
    if checkin.medical_record:
        messages.error(
            request, "A medical record has already been added for this check-in."
        )
        return redirect("clinic:checkin_list")

    if request.method == "POST":
        form = MedicalRecordUpdateForm(request.POST)
        if form.is_valid():
            record_title = form.cleaned_data.get("title")
            record = form.save(commit=False)
            record.patient = checkin.patient
            record.doctor = request.user.profile
            try:
                record.save()
                checkin.medical_record = record
                checkin.status = 2
                checkin.save()
                messages.success(request, f"{record_title} added.")
            except ValueError as e:
                messages.error(request, str(e))
            return redirect("clinic:checkin_list")
    else:
        form = MedicalRecordUpdateForm()

    context = {
        "form": form,
        "checkin": checkin,
        "title": "Medical Record",
    }

    return render(request, "clinic/add_medical_record.html", context)


########################### appointment handling ################################
@login_required
def appointment_list(request):
    appointment_list = Appointment.objects.all().order_by("-date")
    context = {
        "appointment_list": appointment_list,
        "title": "List Of Appointment",
    }
    return render(request, "clinic/list_of_appointment.html", context)


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
def change_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if appointment.status == 1:
        appointment.status = 2
        appointment.save()
    elif appointment.status == 2:
        appointment.status = 3
        appointment.save()

    return redirect("clinic:appointment_list")


########################### checkin handling ################################
@login_required
def checkin_list(request):
    today = date.today()
    today_checkin = Checkin.objects.filter(date=today)
    context = {
        "checkin_list": today_checkin,
        "today": today,
        "title": "Check In List",
    }
    return render(request, "clinic/checkin_list.html", context)


@login_required
def add_checkin(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    today = date.today()
    today_checkin = Checkin.objects.filter(
        patient=patient, date=today, status=1
    ).first()
    if today_checkin:
        messages.error(
            request, f"{patient.first_name} already checked in, in waiting list."
        )
    else:
        checkin = Checkin(patient=patient)
        messages.success(request, f"{patient.first_name} successfully checked in.")
        checkin.save()

    return redirect("clinic:patient_data", pk=pk)


########################### payment handling ################################
# def add_payment(request):
#     # list today checkin with done status, because they should already have a price on medical record
#     today = date.today()
#     form = PaymentForm()
#     context = {
#         "form": form,
#         "title": "Payment",
#     }
#     return render(request, "clinic/payment.html", context)


def customer_payment(request, checkin_pk):
    checkin = get_object_or_404(Checkin, pk=checkin_pk)
    record = checkin.medical_record
    # check if payment already been made
    if Payment.objects.filter(medical_record=record).exists():
        messages.error(
            request, f"Payment for {checkin.patient.first_name} has already been make."
        )
        return redirect("clinic:checkin_list")

    # TODO: check if medical record already been update

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_type = form.cleaned_data.get("payment_type")
            pay = form.save(commit=False)
            pay.medical_record = record
            pay.payment_status = 2
            pay.save()
            messages.success(
                request,
                f"Payment for {checkin.patient.first_name}: RM{record.price} successfull.",
            )
            return redirect("clinic:checkin_list")

    else:
        form = PaymentForm()
    context = {
        "form": form,
        "title": f"Payment",
        "checkin": checkin,
        "record": record,
    }
    return render(request, "clinic/payment.html", context)
