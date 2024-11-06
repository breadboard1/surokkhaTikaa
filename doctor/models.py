# models.py
from django.db import models
from django.contrib.auth.models import User

class Specialization(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.ManyToManyField(Designation)
    specialization = models.ManyToManyField(Specialization)
    role = models.CharField(max_length=10, default="Doctor", editable=False)  # Automatically set role

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


    def save(self, *args, **kwargs):
        self.role = "Doctor"  # Reinforce the role
        super().save(*args, **kwargs)

