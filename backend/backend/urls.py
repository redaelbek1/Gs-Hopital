from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('patients/', include('patients.urls')),
    path('medecins/', include('medecins.urls')),
    path('rendezvous/', include('rendezvous.urls')),
    path('dossier/', include('dossier_medical.urls')),
    path('services/', include('services.urls')),
    path('ordonnances/', include('ordonnances.urls')),
    path('administration/', include('administration.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
