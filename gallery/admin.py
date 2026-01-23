from django.contrib import admin
from kantha_project.admin_site import kantha_admin_site
from .models import MediaItem

class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'description', 'created_at')
    list_filter = ('media_type', 'created_at')
    search_fields = ('title', 'description')

kantha_admin_site.register(MediaItem, MediaItemAdmin)
