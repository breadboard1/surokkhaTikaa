# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('doctor/register/', views.doctor_registration_view, name='doctor_register'),
]
