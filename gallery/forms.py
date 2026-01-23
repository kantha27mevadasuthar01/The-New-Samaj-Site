from django import forms
from .models import MediaItem

class MediaForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Description', 'rows': 3}),
            'media_type': forms.Select(attrs={'class': 'form-select'}),
            'video_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Video URL (if applicable)'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Display Order'}),
        }
        labels = {
            'media_type': 'Media Type (Photo/Video)',
            'video_url': 'YouTube Video URL',
        }
