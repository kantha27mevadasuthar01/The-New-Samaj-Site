from django import forms
from .models import Person, Family

class PersonForm(forms.ModelForm):
    # Field for hometown when creating/editing a head
    hometown = forms.CharField(
        max_length=100, 
        required=False, 
        label="Home Town (For Family Head)",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Home Town'})
    )

    class Meta:
        model = Person
        fields = [
            'photo', 'full_name', 'relation_with_head', 'is_head', 
            'marital_status', 'birth_date', 'education', 'education_other',
            'maternal_home', 'blood_group', 'address', 'job', 'mobile_number',
            'family', 'parent_person'
        ]
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-input-file'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Rajeshbhai Mevada'}),
            'relation_with_head': forms.Select(attrs={'class': 'form-input'}),
            'is_head': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'marital_status': forms.RadioSelect(attrs={'class': 'radio-group'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'education': forms.Select(attrs={'class': 'form-input', 'onchange': 'toggleEducationOther(this)'}),
            'education_other': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Specify Other Education',
                'id': 'id_education_other',
                'style': 'display: none;'
            }),
            'maternal_home': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Maternal Home (Piyu-vatan)'}),
            'blood_group': forms.Select(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Full Address'}),
            'job': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Current Job/Profession'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Mobile Number'}),
            'family': forms.Select(attrs={'class': 'form-input'}),
            'parent_person': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.is_head:
            if self.instance.family:
                self.fields['hometown'].initial = self.instance.family.hometown
        
        # Display education_other if already set
        if self.instance and self.instance.education == 'OTHER':
            self.fields['education_other'].widget.attrs['style'] = 'display: block;'

    def clean(self):
        cleaned_data = super().clean()
        is_head = cleaned_data.get('is_head')
        hometown = cleaned_data.get('hometown')
        education = cleaned_data.get('education')
        education_other = cleaned_data.get('education_other')

        if is_head and not hometown:
            self.add_error('hometown', "Hometown is required for Family Head.")
        
        if education == 'OTHER' and not education_other:
            self.add_error('education_other', "Please specify your education.")

        return cleaned_data
