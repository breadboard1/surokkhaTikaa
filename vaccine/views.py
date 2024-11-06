from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vaccine
from .forms import VaccineForm
from functools import wraps



def doctor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'doctor'):
            return redirect('access_denied')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@login_required
@doctor_required
def add_vaccine(request):
    if request.method == "POST":
        form = VaccineForm(request.POST)
        if form.is_valid():
            vaccine = form.save(commit=False)
            vaccine.save()
            return redirect("vaccine_list")
    else:
        form = VaccineForm()
    return render(request, "vaccine/add_vaccine.html", {"form": form})



def access_denied(request):
    return render(request, 'vaccine/access_denied.html')



def vaccine_list(request):
    vaccines = Vaccine.objects.all()  # Retrieve all vaccines from the database
    return render(request, 'vaccine/vaccine_list.html', {'vaccines': vaccines})



def vaccine_detail_view(request, vaccine_id):
    vaccine = get_object_or_404(Vaccine, id=vaccine_id)
    context = {
        'vaccine': vaccine
    }
    return render(request, 'vaccine/vaccine_detail.html', context)