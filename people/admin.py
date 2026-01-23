from django.contrib import admin
from kantha_project.admin_site import kantha_admin_site
from .models import Person, FamilyGroup

class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'village')
    search_fields = ('name', 'village')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'family_group', 'native_gam', 'current_city', 'age', 'is_family_head')
    list_filter = ('native_gam', 'current_city', 'is_family_head', 'family_group')
    search_fields = ('full_name', 'native_gam', 'current_city', 'family_group__name')
    ordering = ('-is_family_head', 'full_name')

kantha_admin_site.register(FamilyGroup, FamilyGroupAdmin)
kantha_admin_site.register(Person, PersonAdmin)
