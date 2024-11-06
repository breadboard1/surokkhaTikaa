from django.contrib import admin
from .models import Campaign, VaccineSchedule, DoseBooking, CampaignReview

admin.site.register(Campaign)
admin.site.register(VaccineSchedule)
admin.site.register(DoseBooking)
admin.site.register(CampaignReview)