from django.urls import path
from . import views

urlpatterns = [
    path('book-dose/', views.book_dose, name='book_dose'),
    path('campaign/<int:vaccine_id>/review/', views.add_review, name='add_review'),
    path('create-campaign/', views.create_campaign, name='create_campaign'),
    path('edit-campaign/<int:campaign_id>/', views.edit_campaign, name='edit_campaign'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaign/<int:campaign_id>/', views.campaign_detail_view, name='campaign_detail'),
    path('booking-success/<int:campaign_id>/<int:vaccine_id>/', views.dose_booking_success, name='dose_booking_success'),

]
