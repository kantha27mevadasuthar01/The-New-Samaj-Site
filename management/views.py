from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import CommitteeMember, CommitteeSettings
from .forms import CommitteeMemberForm, CommitteeSettingsForm

def committee_list(request):
    """
    Displays the list of committee members and the current term settings.
    This is a public view.
    """
    members = CommitteeMember.objects.all()
    settings = CommitteeSettings.objects.first()
    return render(request, 'management/committee_list.html', {
        'members': members,
        'settings': settings
    })

def is_admin(user):
    """
    Check if user has administrative privileges.
    """
    return user.is_authenticated and (user.role in ['ADMIN', 'SUB_ADMIN'] or user.is_superuser)

@user_passes_test(is_admin)
def committee_settings_update(request):
    """
    Calculates and updates committee term settings (Start/End Year).
    Limited to Admins.
    """
    settings = CommitteeSettings.objects.first()
    if not settings:
        settings = CommitteeSettings.objects.create()
    
    if request.method == 'POST':
        form = CommitteeSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Committee settings updated.")
            return redirect('committee_list')
    else:
        form = CommitteeSettingsForm(instance=settings)
    
    return render(request, 'management/committee_form.html', {
        'form': form, 
        'title': 'Update Committee Settings'
    })

@user_passes_test(is_admin)
def committee_create(request):
    """
    Manually creates a new committee member.
    """
    if request.method == 'POST':
        form = CommitteeMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Committee member added successfully.")
            return redirect('committee_list')
    else:
        form = CommitteeMemberForm()
    return render(request, 'management/committee_form.html', {'form': form, 'title': 'Add Member'})

@user_passes_test(is_admin)
def committee_update(request, pk):
    """
    Updates an existing committee member's details.
    """
    member = get_object_or_404(CommitteeMember, pk=pk)
    if request.method == 'POST':
        form = CommitteeMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Committee member updated successfully.")
            return redirect('committee_list')
    else:
        form = CommitteeMemberForm(instance=member)
    return render(request, 'management/committee_form.html', {'form': form, 'title': 'Update Member'})

@user_passes_test(is_admin)
def committee_delete(request, pk):
    """
    Removes a member from the committee.
    """
    member = get_object_or_404(CommitteeMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Committee member deleted.")
        return redirect('committee_list')
    return render(request, 'management/committee_confirm_delete.html', {'member': member})
