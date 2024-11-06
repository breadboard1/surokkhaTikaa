from django import forms
from .models import Vaccine

class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = ['name', 'description', 'manufacturer']
