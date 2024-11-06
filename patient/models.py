# models.py
from django.db import models
from django.contrib.auth.models import User

# Choices for gender field
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's User model
    nid = models.CharField(max_length=20, unique=True)  # National ID, unique for each patient
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    role = models.CharField(max_length=10, default="Patient", editable=False)  # Automatically set role

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        self.role = "Patient"  # Ensure the role is always set to "Patient"
        super().save(*args, **kwargs)
