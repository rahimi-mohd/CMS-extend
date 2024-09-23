from django.urls import path

from . import views

app_name = "clinic"
urlpatterns = [
    path("", views.home, name="home"),
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
    path(
        "patient_list/<int:pk>/add_medical_record/",
        views.add_medical_record,
        name="add_medical_record",
    ),
]
