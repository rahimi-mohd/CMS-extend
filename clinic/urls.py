from django.urls import path

from . import views

app_name = "clinic"
urlpatterns = [
    ############## home page ##############
    path("", views.home, name="home"),
    ############## patient handling ##############
    path("patient_list/", views.patient_list, name="patient_list"),
    path(
        "patient_list/<int:pk>/",
        views.patient_data,
        name="patient_data",
    ),
    path(
        "patient_list/register_patient/",
        views.register_patient,
        name="register_patient",
    ),
    ############## medical record handling ##############
    path(
        "patient_list/<int:pk>/add_medical_record/",
        views.add_medical_record,
        name="add_medical_record",
    ),
    ############## appointment handling ##############
    path(
        "patient_list/<int:pk>/add_appointment/",
        views.add_appointment,
        name="add_appointment",
    ),
    path("appointment_list/", views.appointment_list, name="appointment_list"),
    path(
        "appointment_list/<int:pk>/change_status/",
        views.change_appointment_status,
        name="change_status",
    ),
    ############## check in handling ##############
    path("checkin_list/", views.checkin_list, name="checkin_list"),
    path(
        "patient_list/<int:pk>/patient_checkin/",
        views.add_checkin,
        name="patient_checkin",
    ),
    path(
        "checkin_list/<int:pk>/update_status/",
        views.update_checkin_status,
        name="update_checkin_status",
    ),
]
