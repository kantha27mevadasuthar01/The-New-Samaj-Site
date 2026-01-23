from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import SamajInformation
from .forms import SamajInfoForm

def home(request):
    history = SamajInformation.objects.filter(section='HISTORY').first()
    purpose = SamajInformation.objects.filter(section='PURPOSE').first()
    values = SamajInformation.objects.filter(section='VALUES').first()
    
    context = {
        'history': history,
        'purpose': purpose,
        'values': values,
    }
    return render(request, 'core/home.html', context)

@staff_member_required
def manage_content(request):
    info_items = SamajInformation.objects.all()
    return render(request, 'core/manage_list.html', {'info_items': info_items})

@staff_member_required
def add_content(request):
    if request.method == 'POST':
        form = SamajInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_content')
    else:
        form = SamajInfoForm()
    return render(request, 'core/samaj_info_form.html', {'form': form, 'title': 'Create New Content Section'})

@staff_member_required
def edit_content(request, pk):
    info_item = get_object_or_404(SamajInformation, pk=pk)
    if request.method == 'POST':
        form = SamajInfoForm(request.POST, instance=info_item)
        if form.is_valid():
            form.save()
            return redirect('manage_content')
    else:
        form = SamajInfoForm(instance=info_item)
    return render(request, 'core/samaj_info_form.html', {'form': form, 'title': 'Update Page Content Section'})

@staff_member_required
def delete_content(request, pk):
    info_item = get_object_or_404(SamajInformation, pk=pk)
    if request.method == 'POST':
        info_item.delete()
        return redirect('manage_content')
    return render(request, 'core/content_confirm_delete.html', {'info_item': info_item})
