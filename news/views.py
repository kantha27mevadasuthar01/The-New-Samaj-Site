from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import NewsAnnouncement
from .forms import NewsAnnouncementForm

def is_staff_check(user):
    """
    Check if the user is staff or an Admin/Sub-Admin.
    """
    return user.is_staff or user.role in ['ADMIN', 'SUB_ADMIN']

@login_required
@user_passes_test(is_staff_check)
def news_list(request):
    """
    Displays a list of all news announcements.
    Restricted to Staff/Admins.
    """
    news_items = NewsAnnouncement.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_items': news_items})

@login_required
@user_passes_test(is_staff_check)
def news_create(request):
    """
    Creates a new news announcement.
    """
    if request.method == 'POST':
        form = NewsAnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement created successfully.")
            return redirect('news_list')
    else:
        form = NewsAnnouncementForm()
    return render(request, 'news/news_form.html', {'form': form, 'title': 'Add New Announcement'})

@login_required
@user_passes_test(is_staff_check)
def news_edit(request, pk):
    """
    Edits an existing news announcement.
    """
    news_item = get_object_or_404(NewsAnnouncement, pk=pk)
    if request.method == 'POST':
        form = NewsAnnouncementForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully.")
            return redirect('news_list')
    else:
        form = NewsAnnouncementForm(instance=news_item)
    return render(request, 'news/news_form.html', {'form': form, 'title': 'Edit Announcement'})

@login_required
@user_passes_test(is_staff_check)
def news_delete(request, pk):
    """
    Deletes a news announcement.
    """
    news_item = get_object_or_404(NewsAnnouncement, pk=pk)
    if request.method == 'POST':
        news_item.delete()
        return redirect('news_list')
    return render(request, 'news/news_confirm_delete.html', {'news_item': news_item})
