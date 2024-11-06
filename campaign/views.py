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
            # Reduce the available slot count
            dose_booking.schedule.available_slots -= 1
            dose_booking.schedule.save()

            # Get the related campaign and vaccine details
            campaign = dose_booking.schedule.campaign  # Now this should work
            vaccine = campaign.vaccine

            # Redirect to the booking success page with campaign and vaccine info
            return redirect('dose_booking_success', campaign_id=campaign.id, vaccine_id=vaccine.id)
    else:
        form = DoseBookingForm()

    return render(request, "campaign/book_dose.html", {"form": form, "available_schedules": available_schedules})



@login_required
def add_review(request, vaccine_id):
    vaccine = Vaccine.objects.get(id=vaccine_id)
    # Check if the user has booked a dose for this campaign
    has_booking = DoseBooking.objects.filter(patient=request.user, schedule__vaccine=vaccine).exists()

    if not has_booking:
        return render(request, "campaign/access_denied.html", {"message": "You must book a dose to review this campaign."})

    if request.method == "POST":
        form = CampaignReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.campaign = vaccine
            review.patient = request.user
            review.save()
            return redirect('campaign_review_success')  # Redirect to a success page
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
            campaign.doctor = request.user  # Set the campaign's doctor
            campaign.save()
            return redirect('campaign_list')  # Redirect to the campaign list
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
    # Get the campaign or return a 404 if it doesn't exist
    campaign = get_object_or_404(Campaign, id=campaign_id)
    reviews = campaign.reviews.all()  # Access the reviews through the related_name

    # Initialize user_booking to False by default
    user_booking = False

    # Check if the user is authenticated and has booked the dose for this campaign
    if request.user.is_authenticated:
        user_booking = DoseBooking.objects.filter(patient=request.user, schedule__vaccine=campaign.vaccine).exists()

    if request.method == 'POST':
        # Only proceed if the user is authenticated and has booked the campaign
        if not user_booking:
            messages.error(request, 'You must book this campaign before leaving a review.')
            return redirect('campaign_detail', campaign_id=campaign.id)

        form = CampaignReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.campaign = campaign  # Associate the review with the campaign
            review.patient = request.user  # Associate the review with the logged-in user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('campaign_detail', campaign_id=campaign.id)
    else:
        form = CampaignReviewForm()

    context = {
        'campaign': campaign,
        'reviews': reviews,
        'form': form,
        'user_can_review': user_booking,  # Pass this variable to the template
        'vaccine_name': campaign.vaccine.name,  # Pass vaccine name to template
        'doctor_name': campaign.doctor.username if campaign.doctor else 'N/A',  # Pass doctor name to template
    }

    return render(request, 'campaign/campaign_detail.html', context)


@login_required
def dose_booking_success(request, campaign_id, vaccine_id):
    # Get the campaign and vaccine objects
    campaign = get_object_or_404(Campaign, id=campaign_id)
    vaccine = get_object_or_404(Vaccine, id=vaccine_id)

    context = {
        'campaign': campaign,
        'vaccine': vaccine,
    }
    return render(request, 'campaign/booking_success.html', context)

