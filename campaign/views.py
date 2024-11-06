from .models import Campaign
from .forms import CampaignForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Campaign, CampaignReview, Vaccine, DoseBooking
from .forms import CampaignReviewForm
from .models import DoseBooking, VaccineSchedule
from .forms import DoseBookingForm
from django.contrib import messages
from functools import wraps

@login_required
def book_dose(request):
    available_schedules = VaccineSchedule.objects.filter(available_slots__gt=0)
    if request.method == "POST":
        form = DoseBookingForm(request.POST)
        if form.is_valid():
            dose_booking = form.save(commit=False)
            dose_booking.patient = request.user
            dose_booking.save()
            dose_booking.schedule.available_slots -= 1
            dose_booking.schedule.save()

            campaign = dose_booking.schedule.campaign
            vaccine = campaign.vaccine

            return redirect('dose_booking_success', campaign_id=campaign.id, vaccine_id=vaccine.id)
    else:
        form = DoseBookingForm()

    return render(request, "campaign/book_dose.html", {"form": form, "available_schedules": available_schedules})



@login_required
def add_review(request, vaccine_id):
    vaccine = Vaccine.objects.get(id=vaccine_id)
    campaign = vaccine.campaign

    has_booking = DoseBooking.objects.filter(patient=request.user, schedule__vaccine=vaccine).exists()

    if not has_booking:
        return render(request, "campaign/access_denied.html", {"message": "You must book a dose to review this campaign."})

    if request.method == "POST":
        form = CampaignReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.campaign = campaign
            review.patient = request.user
            review.save()
            return redirect('campaign_review_success')
    else:
        form = CampaignReviewForm()

    return render(request, "campaign/add_review.html", {"form": form, "vaccine": vaccine})





def doctor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'doctor'):
            return redirect('access_denied')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@login_required
@doctor_required
def create_campaign(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.doctor = request.user
            campaign.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm()

    return render(request, 'campaign/create_campaign.html', {'form': form})



@login_required
@doctor_required
def edit_campaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id, doctor=request.user)
    if request.method == "POST":
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm(instance=campaign)

    return render(request, 'campaign/edit_campaign.html', {'form': form, 'campaign': campaign})




def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaign/campaign_list.html', {'campaigns': campaigns})




def campaign_detail_view(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    reviews = campaign.reviews.all()

    user_booking = False

    if request.user.is_authenticated:
        user_booking = DoseBooking.objects.filter(patient=request.user, schedule__vaccine=campaign.vaccine).exists()

    if request.method == 'POST':
        if not user_booking:
            messages.error(request, 'You must book this campaign before leaving a review.')
            return redirect('campaign_detail', campaign_id=campaign.id)

        form = CampaignReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.campaign = campaign
            review.patient = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('campaign_detail', campaign_id=campaign.id)
    else:
        form = CampaignReviewForm()

    context = {
        'campaign': campaign,
        'reviews': reviews,
        'form': form,
        'user_can_review': user_booking,
        'vaccine_name': campaign.vaccine.name,
        'doctor_name': campaign.doctor.username if campaign.doctor else 'N/A',
    }

    return render(request, 'campaign/campaign_detail.html', context)


@login_required
def dose_booking_success(request, campaign_id, vaccine_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    vaccine = get_object_or_404(Vaccine, id=vaccine_id)

    context = {
        'campaign': campaign,
        'vaccine': vaccine,
    }
    return render(request, 'campaign/booking_success.html', context)

