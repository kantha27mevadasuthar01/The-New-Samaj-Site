from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from kantha_project.admin_site import kantha_admin_site
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'can_view_directory')}),
    )

kantha_admin_site.register(User, CustomUserAdmin)
