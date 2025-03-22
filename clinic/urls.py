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
    ############## check in handling ##############
    path("checkin_list/", views.checkin_list, name="checkin_list"),
    path("checkin_table", views.checkin_table, name="checkin_table"),
    path(
        "patient_list/<int:pk>/patient_checkin/",
        views.add_checkin,
        name="patient_checkin",
    ),
    path(
        "appointment_list/<int:pk>/checkin_list/",
        views.move_to_checkin,
        name="move_to_checkin",
    ),
    ############## payment handling ##############
    path(
        "checkin_list/<int:checkin_pk>/payment/",
        views.customer_payment,
        name="payment",
    ),
    ############## Inventory handling ##############
    path("inventory_list/", views.inventory_list, name="inventory_list"),
    path(
        "inventory_list/<int:pk>/add_stock/",
        views.add_item_into_inventory,
        name="add_stock",
    ),
]
