from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError, transaction
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Patient, MedicalRecord, Appointment, Checkin, Payment, Medicine
from accounts.models import Profile
from .forms import (
    PatientRegistrationForm,
    MedicalRecordUpdateForm,
    AddAppointmentForm,
    PaymentForm,
    InventoryAddItemForm,
)

from accounts.decorators import allowed_users

from datetime import date


########################### home page ################################
@login_required
# everyone can see this page
def home(request):
    today = date.today()

    appointment_count = Appointment.objects.filter(date=today).count()
    checkin_count = Checkin.objects.filter(date=today).count()

    context = {
        "title": "Home",
        "appointment_count" : appointment_count,
        "checkin_count": checkin_count,
        "user": request.user,
    }
    return render(request, "clinic/index.html", context)

########################### patient handling ################################
@login_required
# everyone can see this page
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
# everyone can see this page
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
# only clinic staff and admin can see this page
@allowed_users(
    message="You do not have permission to register new patient.",
    redirect_link="clinic:patient_list",
    allowed_user_types=[Profile.UserType.ADMIN, Profile.UserType.CLINIC_STAFF],
)
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
# only doctors and admin can see this page
@allowed_users(
    "You do not have permission to add medical record.",
    redirect_link="clinic:checkin_list",
    allowed_user_types=[Profile.UserType.DOCTOR, Profile.UserType.ADMIN],
)
def add_medical_record(request, pk):
    today = date.today()

    """get checkin by patient id, status:waiting and date: today"""
    checkin = Checkin.objects.get(patient_id=pk, status=1, date=today)

    """check if user has no profile, usually super user which create with command line"""
    if not hasattr(request.user, "profile"):
        messages.error(
            request,
            "You do not have a profile. If you're superuser, you can access this using admin page.",
        )
        return redirect("clinic:checkin_list")

    """check if medical record already updated,
    to make sure that there's no duplicate medical record in one checkin"""
    if checkin.medical_record:
        messages.error(
            request, "A medical record has already been added for this check-in."
        )
        return redirect("clinic:checkin_list")

    form = MedicalRecordUpdateForm()

    if request.method == "POST":
        form = MedicalRecordUpdateForm(request.POST)
        if form.is_valid():
            medicines = form.cleaned_data.get("medicines")
            stock_error = False

            # Check for stock availability
            for med in medicines:
                if med.quantity_in_stock <= 0:
                    messages.error(request, f"Not enough stock for {med.name}!")
                    stock_error = True

            if stock_error:
                # Render the form with the error message instead of redirecting
                return render(
                    request,
                    "clinic/add_medical_record.html",
                    {"form": form, "checkin": checkin, "title": "Medical Record"},
                )

            record_title = form.cleaned_data.get("title")
            record = form.save(commit=False)
            record.patient = checkin.patient
            record.doctor = request.user.profile

            try:
                # Save each medicine record and update stock
                with transaction.atomic():
                    record.save()
                    record.medicine.set(medicines)  # save medicines into record

                    """update the stock quantity of each medicine selected for this record"""
                    for med in medicines:
                        med.quantity_in_stock -= 1
                        med.save()

                    """update checkin instance"""
                    checkin.medical_record = record
                    checkin.status = 2
                    checkin.save()

                messages.success(request, f"{record_title} added.")
                return redirect("clinic:checkin_list")
            except ValueError as e:
                messages.error(request, str(e))
                return render(
                    request,
                    "clinic/add_medical_record.html",
                    {"form": form, "checkin": checkin, "title": "Medical Record"},
                )
    else:
        # If the request method is GET, you can initialize the form with existing data if needed.
        form = MedicalRecordUpdateForm()

    context = {
        "form": form,
        "checkin": checkin,
        "title": "Medical Record",
    }

    return render(request, "clinic/add_medical_record.html", context)


########################### appointment handling ################################
@login_required
# everyone can see this page
def appointment_list(request):
    today = date.today()

    """appointment list excluding today appointment"""
    appointment_list = Appointment.objects.all().exclude(date=today).order_by("-date")

    """today appointment only"""
    today_appointment = Appointment.objects.filter(date=today)

    context = {
        "today_appointment": today_appointment,
        "appointment_list": appointment_list,
        "title": "List Of Appointment",
    }
    return render(request, "clinic/appointment_list.html", context)


@login_required
# only clinic staff and admin can see this page
@allowed_users(
    "You do not have permission to add new appointment.",
    redirect_link="clinic:patient_list",
    allowed_user_types=[Profile.UserType.CLINIC_STAFF, Profile.UserType.ADMIN],
)
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
# only clinic staff and admin can see this page
@allowed_users(
    "You do not have permission to move patient into check-in list.",
    redirect_link="clinic:checkin_list",
    allowed_user_types=[Profile.UserType.CLINIC_STAFF, Profile.UserType.ADMIN],
)
def move_to_checkin(request, pk):
    """Handle moving patients to check-in from the appointment list."""
    today = date.today()
    appointment = get_object_or_404(Appointment, pk=pk)

    # Ensure the appointment is for today
    if appointment.date != today:
        messages.error(
            request, "You can only check in patients with today's appointment."
        )
        return redirect("clinic:appointment_list")

    # Check if a check-in already exists for today with status "waiting"
    existing_checkin = Checkin.objects.filter(
        patient=appointment.patient, date=today, status=1
    ).exists()

    if existing_checkin:
        messages.info(request, "Patient is already checked in and waiting.")
        return redirect("clinic:appointment_list")

    # Check if the patient has already checked in today but the status is "done"
    previous_checkin = (
        Checkin.objects.filter(patient=appointment.patient, date=today)
        .exclude(status=1)
        .exists()
    )

    if previous_checkin:
        messages.info(
            request,
            "Patient has completed a previous check-in but can be re-checked in.",
        )

    checkin = Checkin.objects.create(
        patient=appointment.patient,
        status=1,
        date=today,
    )

    """change appointment status to Completed so that I can disabled to button/link"""
    appointment.status = 2
    appointment.save()

    messages.success(request, f"{appointment.patient.first_name} has been checked in.")
    return redirect("clinic:checkin_list")


########################### checkin handling ################################
@login_required
# everyone can see this page
def checkin_list(request):
    today = date.today()
    today_checkin = Checkin.objects.filter(date=today)
    context = {
        "checkin_list": today_checkin,
        "title": "Check-In List",
    }
    return render(request, "clinic/checkin_list.html", context)


@login_required
# change redirect later
@allowed_users(
    "You do not have permission to add this patient into check-in list.",
    redirect_link="clinic:checkin_list",
    allowed_user_types=[Profile.UserType.CLINIC_STAFF, Profile.UserType.ADMIN],
)
def add_checkin(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    today = date.today()

    """Check for user permission"""
    # # FIXME: same add appointment
    # if not request.user.has_perm("clinic.add_checkin"):
    #     messages.error(
    #         request,
    #         "You do not have permission to add this patient into check-in list.",
    #     )
    #     return redirect("clinic:patient_data", patient.pk)

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
@login_required
@allowed_users(
    "You do not have permission to handle payment.",
    redirect_link="clinic:checkin_list",
    allowed_user_types=[Profile.UserType.CLINIC_STAFF, Profile.UserType.ADMIN],
)
def customer_payment(request, checkin_pk):
    checkin = get_object_or_404(Checkin, pk=checkin_pk)
    record = checkin.medical_record

    """check if record already been updated"""
    if not record:
        messages.error(
            request,
            f"No medical record found for {checkin.patient.first_name}. Please update the medical checkup before proceeding with the payment.",
        )
        return redirect("clinic:checkin_list")

    # check if payment already been made
    if Payment.objects.filter(medical_record=record).exists():
        messages.error(
            request, f"Payment for {checkin.patient.first_name} has already been make."
        )
        return redirect("clinic:checkin_list")

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


########################### Inventory handling ################################
# @login_required
# # everyone can see this page
# def inventory_list(request):
    # query = request.GET.get("search", "")
    # page_number = request.GET.get("page", 1)
    # if query:
    #     medicines = (
    #         Medicine.objects.filter(
    #             Q(name__icontains=query) | Q(category__icontains=query)
    #         )
    #         .order_by("quantity_in_stock")
    #         .exclude(quantity_in_stock__lte=0)
    #     )
    # else:
    #     medicines = (
    #         Medicine.objects.all()
    #         .order_by("quantity_in_stock")
    #         .exclude(quantity_in_stock__lte=0)
    #     )
    
    # medicine_list = Medicine.objects.all()

    # context = {
    #     "medicines": medicines,
    #     "medicine_list": medicine_list,
    #     "title": "Inventory List",
    # }
    # return render(request, "clinic/inventory_list.html", context)

@login_required
def inventory_list(request):
    query = request.GET.get("search", "")

    # Filter based on search query if provided
    if query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        ).order_by("-quantity_in_stock", "name")  # Descending order for quantity
    else:
        medicines = Medicine.objects.order_by("-quantity_in_stock", "name")  # Descending order for quantity

    # Pagination: Show 50 medicines per page
    paginator = Paginator(medicines, 50)
    page_number = request.GET.get("page")
    medicines_page = paginator.get_page(page_number)

    context = {
        "medicines": medicines_page,
        "title": "Inventory List",
    }
    return render(request, "clinic/inventory_list.html", context)



@login_required
@allowed_users(
    "You do not have permission to change inventory data",
    redirect_link="clinic:inventory_list",
    allowed_user_types=[Profile.UserType.CLINIC_STAFF, Profile.UserType.ADMIN],
)
def add_item_into_inventory(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == "POST":
        form = InventoryAddItemForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            medicine.quantity_in_stock += amount
            medicine.save()
            messages.success(request, f"Quantity for {medicine.name} update.")
            return redirect("clinic:inventory_list")
    else:
        form = InventoryAddItemForm()

    context = {
        "form": form,
        "medicine": medicine,
        "title": "Add Stock",
    }

    return render(request, "clinic/add_stock.html", context)
