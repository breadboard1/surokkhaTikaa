from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('patient.urls')),
    path('', include('doctor.urls')),
    path('vaccine/', include('vaccine.urls')),
    path('', include('campaign.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)