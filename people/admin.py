from django.contrib import admin
from kantha_project.admin_site import kantha_admin_site
from .models import Person, Family

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('head', 'hometown')
    search_fields = ('head__full_name', 'hometown')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'family', 'relation_with_head', 'marital_status', 'is_head')
    list_filter = ('family__hometown', 'marital_status', 'is_head', 'blood_group')
    search_fields = ('full_name', 'family__hometown', 'job')
    ordering = ('family__hometown', 'full_name')

kantha_admin_site.register(Family, FamilyAdmin)
kantha_admin_site.register(Person, PersonAdmin)
