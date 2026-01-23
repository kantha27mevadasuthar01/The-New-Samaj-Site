from django.contrib import admin
from kantha_project.admin_site import kantha_admin_site
from .models import SamajInformation

class SamajInformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title', 'content')

kantha_admin_site.register(SamajInformation, SamajInformationAdmin)
