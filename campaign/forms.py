from django import forms
from .models import DoseBooking, CampaignReview, Campaign

class DoseBookingForm(forms.ModelForm):
    class Meta:
        model = DoseBooking
        fields = ['schedule', 'first_dose_date']


class CampaignReviewForm(forms.ModelForm):
    class Meta:
        model = CampaignReview
        fields = ['review']


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['vaccine', 'title', 'description', 'start_date', 'end_date']

