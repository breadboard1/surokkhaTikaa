# urls.py
from django.urls import path
from .views import patient_registration_view, login_view, logout_view, home_view, register_choice, profile_view, password_change_view

urlpatterns = [
    path('patient/register/', patient_registration_view, name='patient_register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('register-choice/', register_choice, name='register_choice'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', password_change_view, name='change_password'),
]
