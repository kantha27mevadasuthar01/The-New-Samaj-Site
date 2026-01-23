from django.contrib import admin
from kantha_project.admin_site import kantha_admin_site
from .models import Donation

class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'transaction_id')
    readonly_fields = ('created_at',)

kantha_admin_site.register(Donation, DonationAdmin)
