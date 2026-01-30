from django import forms
from .models import CommitteeMember, CommitteeSettings
from people.models import Person

class CommitteeMemberForm(forms.ModelForm):
    class Meta:
        model = CommitteeMember
        fields = ['name', 'designation', 'village', 'mobile_number', 'display_order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        # Calculate available positions
        available_positions = []
        for code, label in CommitteeMember.POSITIONS:
            limit = CommitteeMember.POSITION_LIMITS.get(code, 0)
            count = CommitteeMember.objects.filter(designation=code).count()
            
            # If editing, don't count the current position for the current instance
            if instance and instance.designation == code:
                count -= 1
            
            if count < limit:
                available_positions.append((code, f"{label} (Remaining: {limit - count})"))
        
        self.fields['designation'].choices = available_positions

class AddToCommitteeForm(forms.ModelForm):
    """Form to add an existing person from directory to the committee"""
    class Meta:
        model = CommitteeMember
        fields = ['designation', 'display_order']
        widgets = {
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person', None)
        super().__init__(*args, **kwargs)
        
        # Calculate available positions
        available_positions = []
        for code, label in CommitteeMember.POSITIONS:
            limit = CommitteeMember.POSITION_LIMITS.get(code, 0)
            count = CommitteeMember.objects.filter(designation=code).count()
            
            if count < limit:
                available_positions.append((code, f"{label} (Remaining: {limit - count})"))
        
        self.fields['designation'].choices = available_positions
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.person:
            instance.person = self.person
            instance.name = self.person.full_name
            instance.village = self.person.family.hometown if self.person.family else "Unknown"
            instance.mobile_number = self.person.mobile_number
        if commit:
            instance.save()
        return instance

class CommitteeSettingsForm(forms.ModelForm):
    class Meta:
        model = CommitteeSettings
        fields = ['start_year', 'end_year']
        widgets = {
            'start_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
