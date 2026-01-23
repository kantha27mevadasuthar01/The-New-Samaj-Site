from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import MandirLocation
from .forms import LocationForm

def location_list(request):
    locations = MandirLocation.objects.all()
    return render(request, 'locations/location_list.html', {'locations': locations})

@staff_member_required
def manage_locations(request):
    locations = MandirLocation.objects.all()
    return render(request, 'locations/manage_list.html', {'locations': locations})

@staff_member_required
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')
    else:
        form = LocationForm()
    return render(request, 'locations/location_form.html', {'form': form, 'title': 'Add New Mandir Location'})

@staff_member_required
def edit_location(request, pk):
    location = get_object_or_404(MandirLocation, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('manage_locations')
    else:
        form = LocationForm(instance=location)
    return render(request, 'locations/location_form.html', {'form': form, 'title': 'Edit Location Details'})

@staff_member_required
def delete_location(request, pk):
    location = get_object_or_404(MandirLocation, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('manage_locations')
    return render(request, 'locations/location_confirm_delete.html', {'location': location})
