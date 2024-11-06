from django.urls import path
from . import views

urlpatterns = [
    path('add-vaccine/', views.add_vaccine, name='add_vaccine'),
    path('vaccine/list/', views.vaccine_list, name='vaccine_list'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('vaccine/<int:vaccine_id>/', views.vaccine_detail_view, name='vaccine_detail'),
]
