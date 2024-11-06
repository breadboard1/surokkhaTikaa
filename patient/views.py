# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from campaign.models import DoseBooking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegistrationForm, PatientForm, UserProfileForm
from vaccine.models import Vaccine
from campaign.models import Campaign

def patient_registration_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        patient_form = PatientForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()

            login(request, user)
            messages.success(request, "Patient registration successful!")
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        patient_form = PatientForm()

    context = {
        'user_form': user_form,
        'patient_form': patient_form,
    }
    return render(request, 'patient/register.html', context)





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'doctor'):
                    messages.success(request, "Welcome, Doctor!")
                    return redirect('home')
                elif hasattr(user, 'patient'):
                    messages.success(request, "Welcome, Patient!")
                    return redirect('home')
                else:
                    messages.error(request, "User role is not recognized.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'patient/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


def home_view(request):
    vaccines = Vaccine.objects.all()
    campaigns = Campaign.objects.all()
    context = {
        'vaccines': vaccines,
        'campaigns': campaigns,
    }
    return render(request, 'patient/index.html', context)


def register_choice(request):
    return render(request, 'patient/registration_choice.html')



@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    booked_campaigns = DoseBooking.objects.filter(patient=user).select_related('schedule__vaccine')

    context = {
        'form': form,
        'booked_campaigns': booked_campaigns,
    }
    return render(request, 'patient/profile.html', context)



@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'patient/password_change.html', context)
