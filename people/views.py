from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Person, Family
from .models import Person, Family
from .forms import PersonForm
from management.models import CommitteeMember
from management.forms import AddToCommitteeForm
import pandas as pd
from io import BytesIO

def is_admin_or_subadmin(user):
    return user.is_authenticated and (user.role in ['ADMIN', 'SUB_ADMIN'] or user.is_superuser)

@login_required
def directory(request):
    # Only members with explicit permission or admins can view
    if not request.user.can_view_directory and not is_admin_or_subadmin(request.user):
        messages.warning(request, "You do not have permission to view the People Directory. Please contact the administrator.")
        return redirect('home')
        
    query = request.GET.get('q', '')
    hometown = request.GET.get('hometown', '')
    
    people = Person.objects.select_related('family').all()
    
    if query:
        people = people.filter(Q(full_name__icontains=query) | Q(job__icontains=query))
    if hometown:
        people = people.filter(family__hometown__icontains=hometown)
        
    # Sorting: Hometown (alphabetical) then Full Name
    people = people.order_by('family__hometown', 'full_name')

    # Committee info
    committee_full = CommitteeMember.is_committee_full()
    available_slots = CommitteeMember.get_available_slots()
        
    return render(request, 'people/directory_list.html', {
        'people': people,
        'is_admin': is_admin_or_subadmin(request.user),
        'query': query,
        'hometown': hometown,
        'committee_full': committee_full,
        'available_slots': available_slots
    })

@login_required
def person_detail(request, pk):
    if not request.user.can_view_directory and not is_admin_or_subadmin(request.user):
        messages.warning(request, "Permission denied.")
        return redirect('home')
        
    person = get_object_or_404(Person.objects.select_related('family'), pk=pk)
    family_members = []
    if person.family:
        family_members = person.family.members.all().exclude(pk=person.pk)
        
    return render(request, 'people/person_detail.html', {
        'person': person,
        'family_members': family_members,
        'is_admin': is_admin_or_subadmin(request.user)
    })

@login_required
def add_person(request):
    if not is_admin_or_subadmin(request.user):
        messages.error(request, "Only Administrators can add people to the directory.")
        return redirect('people_directory')

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)
            
            if person.is_head:
                # Create or update family with hometown
                hometown = form.cleaned_data.get('hometown')
                family = Family.objects.create(hometown=hometown)
                person.family = family
                person.relation_with_head = 'HEAD'
                person.save()
                family.head = person
                family.save()
            else:
                person.save()

            # Audit Log
            from accounts.models import AuditLog
            AuditLog.objects.create(
                actor=request.user, 
                action="Added Person", 
                target=person.full_name,
                details=f"Created member with ID {person.pk}"
            )

            messages.success(request, f"{person.full_name} added successfully.")
            return redirect('people_directory')
    else:
        form = PersonForm()
    return render(request, 'people/person_form.html', {'form': form, 'title': 'Add to People Directory'})

@login_required
def edit_person(request, pk):
    if not is_admin_or_subadmin(request.user):
        messages.error(request, "Only Administrators can edit directory entries.")
        return redirect('people_directory')

    person = get_object_or_404(Person, pk=pk)
    
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person = form.save(commit=False)
            
            if person.is_head:
                hometown = form.cleaned_data.get('hometown')
                if person.family:
                    person.family.hometown = hometown
                    person.family.head = person
                    person.family.save()
                else:
                    family = Family.objects.create(hometown=hometown, head=person)
                    person.family = family
                person.relation_with_head = 'HEAD'
            
            person.save()
            
            # Audit Log
            from accounts.models import AuditLog
            AuditLog.objects.create(
                actor=request.user, 
                action="Edited Person", 
                target=person.full_name,
                details=f"Updated profile for ID {person.pk}"
            )

            messages.success(request, "Profile updated successfully.")
            return redirect('people_directory')
    else:
        form = PersonForm(instance=person)
    return render(request, 'people/person_form.html', {'form': form, 'title': 'Edit Profile'})

@login_required
def delete_person(request, pk):
    if not is_admin_or_subadmin(request.user):
        messages.error(request, "Only Administrators can delete directory entries.")
        return redirect('people_directory')

    person = get_object_or_404(Person, pk=pk)
    name = person.full_name
    if request.method == 'POST':
        person.delete()
        messages.success(request, f"{name} removed from directory.")
        return redirect('people_directory')
    return render(request, 'people/person_confirm_delete.html', {'person': person})

@login_required
def download_directory(request):
    if not is_admin_or_subadmin(request.user):
        messages.error(request, "Only Administrators can download the directory.")
        return redirect('people_directory')

    people = Person.objects.select_related('family').all().order_by('family__hometown', 'full_name')
    
    data = []
    for person in people:
        data.append({
            'Home Town': person.family.hometown if person.family else 'N/A',
            'Full Name': person.full_name,
            'Relation with Head': person.get_relation_with_head_display(),
            'Marital Status': person.get_marital_status_display(),
            'Birth Date': person.birth_date,
            'Education': person.get_education_display() if person.education != 'OTHER' else person.education_other,
            'Maternal Home': person.maternal_home,
            'Blood Group': person.blood_group,
            'Address': person.address,
            'Job': person.job,
            'Mobile': person.mobile_number
        })
    
    df = pd.DataFrame(data)
    
    # Export to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='People Directory')
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="People_Directory.xlsx"'
    return response

@login_required
def add_to_committee(request, person_pk):
    if not is_admin_or_subadmin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('people_directory')
        
    person = get_object_or_404(Person, pk=person_pk)
    
    # Check if already in committee
    if CommitteeMember.objects.filter(person=person).exists():
        messages.warning(request, f"{person.full_name} is already in the committee.")
        return redirect('people_directory')
        
    # Check if committee is full
    if CommitteeMember.is_committee_full():
        messages.error(request, "The committee is full (47 members). You must remove a member before adding a new one.")
        return redirect('people_directory')
        
    if request.method == 'POST':
        form = AddToCommitteeForm(request.POST, person=person)
        if form.is_valid():
            committee_member = form.save()
            
            # Audit Log
            from accounts.models import AuditLog
            AuditLog.objects.create(
                actor=request.user, 
                action="Promoted to Committee", 
                target=person.full_name,
                details=f"Added {person.full_name} as {committee_member.get_designation_display()}"
            )
            
            messages.success(request, f"{person.full_name} added to the committee successfully!")
            return redirect('people_directory')
    else:
        form = AddToCommitteeForm(person=person)
        
    return render(request, 'people/add_to_committee.html', {
        'form': form,
        'person': person,
        'available_slots': CommitteeMember.get_available_slots()
    })
