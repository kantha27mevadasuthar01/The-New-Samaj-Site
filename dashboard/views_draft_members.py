from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import User
# ... other imports ...

# Helper to check if user is staff/admin
def is_staff_or_admin(user):
    return user.is_authenticated and (user.is_staff or user.role in [User.Role.ADMIN, User.Role.SUB_ADMIN] or user.is_superuser)

@login_required
@user_passes_test(is_staff_or_admin)
def member_management(request):
    """
    View for Admins/Sub-Admins to manage member permissions.
    """
    members = User.objects.all().order_by('-date_joined')
    
    # Simple search
    query = request.GET.get('q')
    if query:
        members = members.filter(username__icontains=query) | members.filter(email__icontains=query)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        target_user = get_object_or_404(User, id=user_id)
        
        if action == 'toggle_view':
            target_user.can_view_directory = not target_user.can_view_directory
            target_user.save()
            messages.success(request, f"Updated viewing permission for {target_user.username}")
        
        elif action == 'toggle_download':
            target_user.can_download_directory = not target_user.can_download_directory
            target_user.save()
            messages.success(request, f"Updated download permission for {target_user.username}")
            
        return redirect('member_management')

    return render(request, 'dashboard/member_management.html', {'members': members})
