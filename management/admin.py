from django.contrib import admin
from .models import CommitteeMember, CommitteeSettings
from kantha_project.admin_site import kantha_admin_site

@admin.register(CommitteeMember, site=kantha_admin_site)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'name', 'designation', 'village', 'mobile_number')
    list_display_links = ('name',)
    list_editable = ('display_order', 'designation', 'village', 'mobile_number')
    search_fields = ('name', 'village', 'designation')
    list_filter = ('designation', 'village')
    ordering = ('display_order', 'name')

@admin.register(CommitteeSettings, site=kantha_admin_site)
class CommitteeSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_year', 'end_year')

    def has_add_permission(self, request):
        # Only allow one settings object
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
