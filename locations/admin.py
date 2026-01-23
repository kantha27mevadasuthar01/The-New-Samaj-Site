from django.contrib import admin
from kantha_project.admin_site import kantha_admin_site
from .models import MandirLocation

class MandirLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country')
    list_filter = ('city', 'state')
    search_fields = ('name', 'city', 'description')

kantha_admin_site.register(MandirLocation, MandirLocationAdmin)
