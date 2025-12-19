from django.contrib import admin
from .models import Post, Member

# ===============================
# Posts Admin
# ===============================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'created_at')  # Columns visible in list view
    list_filter = ('post_type', 'created_at')            # Filter sidebar
    search_fields = ('title', 'content')                # Searchable fields
    ordering = ('-created_at',)                         # Newest first
    actions = ['make_text', 'make_photo', 'make_video'] # Optional bulk actions

    # Optional: bulk actions
    def make_text(self, request, queryset):
        queryset.update(post_type='text')
    make_text.short_description = "Mark selected posts as Text"

    def make_photo(self, request, queryset):
        queryset.update(post_type='photo')
    make_photo.short_description = "Mark selected posts as Photo"

    def make_video(self, request, queryset):
        queryset.update(post_type='video')
    make_video.short_description = "Mark selected posts as Video"


# ===============================
# Members Admin
# ===============================
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'location', 'education', 'profession')
    search_fields = ('name', 'location', 'education', 'profession')
    ordering = ('name',)


# ===============================
# Admin Panel Customization
# ===============================
admin.site.site_header = "Samaj Editor Panel"  # Top header
admin.site.site_title = "Samaj Admin"          # Browser tab title
admin.site.index_title = "Editor Dashboard"    # Main dashboard title
