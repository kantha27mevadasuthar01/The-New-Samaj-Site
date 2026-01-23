from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Person, FamilyGroup
from .forms import PersonForm

@login_required
def directory(request):
    if not request.user.can_view_directory and not request.user.is_staff:
        messages.warning(request, "You do not have permission to view the People Directory. Please contact the administrator.")
        return redirect('home')
        
    query_name = request.GET.get('name', '')
    query_age = request.GET.get('age', '')
    query_city = request.GET.get('city', '')
    query_village = request.GET.get('village', '')
    query_family = request.GET.get('family', '')
    
    people = Person.objects.select_related('family_group').all()
    
    
    if query_name:
        people = people.filter(full_name__icontains=query_name)
    if query_age:
        people = people.filter(age=query_age)
    if query_city:
        people = people.filter(current_city__icontains=query_city)
    if query_village:
        people = people.filter(native_gam__icontains=query_village)
    if query_family:
        people = people.filter(family_group__name__icontains=query_family)
        
    return render(request, 'people/directory.html', {
        'people': people,
        'filters': {
            'name': query_name,
            'age': query_age,
            'city': query_city,
            'village': query_village,
            'family': query_family,
        }
    })

@login_required
def person_detail(request, pk):
    if not request.user.can_view_directory and not request.user.is_staff:
        messages.warning(request, "Permission denied.")
        return redirect('home')
        
    person = get_object_or_404(Person.objects.select_related('family_group'), pk=pk)
    family_members = []
    if person.family_group:
        family_members = Person.objects.filter(family_group=person.family_group).exclude(pk=person.pk)
        
    return render(request, 'people/person_detail.html', {
        'person': person,
        'family_members': family_members
    })

@staff_member_required
def manage_people(request):
    people = Person.objects.all()
    return render(request, 'people/manage_list.html', {'people': people})

@staff_member_required
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)
            
            # Handle Family Logic
            family_role = form.cleaned_data.get('family_role')
            if family_role == 'head':
                # Create a new FamilyGroup automatically
                family_name = f"{person.full_name} Family"
                group = FamilyGroup.objects.create(name=family_name, village=person.native_gam)
                person.family_group = group
                person.is_family_head = True
            elif family_role == 'member':
                # Member of existing family
                person.family_group = form.cleaned_data.get('family_group')
                person.is_family_head = False
            
            person.save()
            
            # Integrated User Creation
            if form.cleaned_data.get('create_user_account'):
                from accounts.models import User
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('user_password')
                
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    phone_number=form.cleaned_data.get('phone_number'),
                    role=User.Role.MEMBER,
                    can_view_directory=True # Admin-created members get permission automatically
                )
                messages.success(request, f"Member added and User account created for {email}")
            else:
                messages.success(request, "Member added successfully.")
            
            # Audit Log
            from accounts.models import AuditLog
            AuditLog.objects.create(
                actor=request.user, 
                action="Added Person", 
                target=person.full_name,
                details=f"Created member with ID {person.pk}"
            )

            return redirect('manage_people')
    else:
        form = PersonForm()
    return render(request, 'people/person_form.html', {'form': form, 'title': 'Register New Community Member'})

@staff_member_required
def edit_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    from accounts.models import User
    user = User.objects.filter(email=person.email).first() if person.email else None
    
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person = form.save(commit=False)
            
            # Handle Family Logic
            family_role = form.cleaned_data.get('family_role')
            if family_role == 'head':
                if not person.is_family_head: # Change to head
                    family_name = f"{person.full_name} Family"
                    group = FamilyGroup.objects.create(name=family_name, village=person.native_gam)
                    person.family_group = group
                    person.is_family_head = True
            elif family_role == 'member':
                person.family_group = form.cleaned_data.get('family_group')
                person.is_family_head = False
            
            person.save()
            
            # Sync permission or create account if requested
            if form.cleaned_data.get('create_user_account') and not user:
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('user_password')
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    phone_number=form.cleaned_data.get('phone_number'),
                    role=User.Role.MEMBER,
                    can_view_directory=True
                )
                messages.success(request, "User account created for this member.")
            elif user:
                user.can_view_directory = form.cleaned_data.get('can_view_directory')
                # Also update role if needed, but keeping it simple for now
                user.save()
                messages.success(request, "Member profile and User permissions updated.")
            
            # Audit Log
            from accounts.models import AuditLog
            AuditLog.objects.create(
                actor=request.user, 
                action="Edited Person", 
                target=person.full_name,
                details=f"Updated profile for ID {person.pk}"
            )

            return redirect('manage_people')
    else:
        initial = {}
        if user:
            initial['can_view_directory'] = user.can_view_directory
        form = PersonForm(instance=person, initial=initial)
    return render(request, 'people/person_form.html', {'form': form, 'title': 'Update Member Profile'})

@staff_member_required
def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('manage_people')
    return render(request, 'people/person_confirm_delete.html', {'person': person})
