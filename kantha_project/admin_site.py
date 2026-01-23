from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from donations.models import Donation

class KanthaAdminSite(admin.AdminSite):
    site_header = "Kantha27 Samaj Administration"
    site_title = "Kantha27 Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        # Calculate Monthly Donation Stats
        monthly_data = (
            Donation.objects
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        
        labels = [d['month'].strftime('%B %Y') for d in monthly_data] if monthly_data else []
        data = [float(d['total']) for d in monthly_data] if monthly_data else []

        extra_context = extra_context or {}
        extra_context['chart_labels'] = labels
        extra_context['chart_data'] = data
        
        return super().index(request, extra_context=extra_context)

kantha_admin_site = KanthaAdminSite(name='kantha_admin')
