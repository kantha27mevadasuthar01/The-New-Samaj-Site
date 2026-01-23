from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import sub_admin_required, main_admin_required
from people.models import Person
from gallery.models import MediaItem
from locations.models import MandirLocation
from donations.models import Donation
from accounts.models import User, AuditLog
from accounts.forms import CustomUserCreationForm
from django.db.models import Sum

def log_action(user, action, target="", details=""):
    AuditLog.objects.create(actor=user, action=action, target=target, details=details)

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html', {'user': request.user})

@sub_admin_required
def staff_portal(request):
    context = {
        'person_count': Person.objects.count(),
        'media_count': MediaItem.objects.count(),
        'location_count': MandirLocation.objects.count(),
        'donation_total': Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    return render(request, 'dashboard/staff_portal.html', context)

@main_admin_required
def manage_sub_admins(request):
    sub_admins = User.objects.filter(role=User.Role.SUB_ADMIN)
    return render(request, 'dashboard/manage_sub_admins.html', {'sub_admins': sub_admins})

@main_admin_required
def create_sub_admin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.SUB_ADMIN
            user.can_view_directory = True
            user.is_staff = False # CRITICAL: No Django Admin Access
            user.save()
            log_action(request.user, "Created Sub-Admin", user.username)
            messages.success(request, f"Sub-Admin {user.username} created successfully.")
            return redirect('manage_sub_admins')
    else:
        form = CustomUserCreationForm()
    return render(request, 'dashboard/sub_admin_form.html', {'form': form})

@main_admin_required
def view_audit_logs(request):
    logs = AuditLog.objects.all()[:50] # Show last 50 actions
    return render(request, 'dashboard/audit_logs.html', {'logs': logs})
