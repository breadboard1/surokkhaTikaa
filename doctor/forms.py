# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Specialization, Designation

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")


class DoctorForm(forms.ModelForm):
    designation = forms.ModelMultipleChoiceField(
        queryset=Designation.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    specialization = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Doctor
        fields = ['designation', 'specialization']  # No need for role field
