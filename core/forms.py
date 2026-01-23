from django import forms
from .models import SamajInformation

class SamajInfoForm(forms.ModelForm):
    class Meta:
        model = SamajInformation
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Section Title'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Content', 'rows': 10}),
        }
        labels = {
            'title': 'Section Title',
            'section': 'Section Type',
            'content': 'Page Content',
        }
