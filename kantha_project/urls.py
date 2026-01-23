from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_site import kantha_admin_site

urlpatterns = [
    path('admin/', kantha_admin_site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('people/', include('people.urls')),
    path('locations/', include('locations.urls')),
    path('gallery/', include('gallery.urls')),
    path('donations/', include('donations.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
