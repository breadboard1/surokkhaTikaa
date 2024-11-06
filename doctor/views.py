# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm, DoctorForm
from .models import Doctor

def doctor_registration_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        doctor_form = DoctorForm(request.POST)

        if user_form.is_valid() and doctor_form.is_valid():
            # Save the User model instance
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Save the Doctor model instance
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            # role is automatically set in the model
            doctor.save()
            doctor_form.save_m2m()  # Save the many-to-many relationships

            # Log the user in and redirect
            login(request, user)
            messages.success(request, "Doctor registration successful!")
            return redirect('home')  # Adjust to redirect to an appropriate page

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        user_form = UserRegistrationForm()
        doctor_form = DoctorForm()

    context = {
        'user_form': user_form,
        'doctor_form': doctor_form,
    }
    return render(request, 'doctor/doctor_registration.html', context)
