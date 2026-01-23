from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import MediaItem
from .forms import MediaForm

def media_list(request):
    media_items = MediaItem.objects.all()
    return render(request, 'gallery/media_list.html', {'media_items': media_items})

@staff_member_required
def manage_gallery(request):
    media_items = MediaItem.objects.all()
    return render(request, 'gallery/manage_list.html', {'media_items': media_items})

@staff_member_required
def add_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_gallery')
    else:
        form = MediaForm()
    return render(request, 'gallery/media_form.html', {'form': form, 'title': 'Upload New Media to Gallery'})

@staff_member_required
def edit_media(request, pk):
    media_item = get_object_or_404(MediaItem, pk=pk)
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES, instance=media_item)
        if form.is_valid():
            form.save()
            return redirect('manage_gallery')
    else:
        form = MediaForm(instance=media_item)
    return render(request, 'gallery/media_form.html', {'form': form, 'title': 'Update Media Information'})

@staff_member_required
def delete_media(request, pk):
    media_item = get_object_or_404(MediaItem, pk=pk)
    if request.method == 'POST':
        media_item.delete()
        return redirect('manage_gallery')
    return render(request, 'gallery/media_confirm_delete.html', {'media_item': media_item})
