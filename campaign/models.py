from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from vaccine.models import Vaccine
from django.utils import timezone


class Campaign(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'doctor__role': 'Doctor'})
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="campaign/images", null=True)

    def is_campaign_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date
    def __str__(self):
        return f"{self.title} - {self.vaccine.name} (by {self.doctor.username})"



class VaccineSchedule(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='schedules')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    available_slots = models.IntegerField()

    def __str__(self):
        return f"{self.vaccine.name} - {self.date}"


class DoseBooking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(VaccineSchedule, on_delete=models.CASCADE)
    first_dose_date = models.DateField()
    second_dose_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.second_dose_date:
            self.second_dose_date = self.first_dose_date + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username} - {self.schedule.vaccine.name} booking"


class CampaignReview(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='reviews')
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.patient.username} for {self.campaign.title}"

