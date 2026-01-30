from django import forms
from .models import NewsAnnouncement

class NewsAnnouncementForm(forms.ModelForm):
    class Meta:
        model = NewsAnnouncement
        fields = ['message', 'is_active', 'scroll_speed']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter announcement text...'}),
            'scroll_speed': forms.NumberInput(attrs={'class': 'form-control', 'min': 5, 'max': 60}),
        }
        help_texts = {
            'scroll_speed': 'Time in seconds for one full scroll loop (e.g., 10=Fast, 30=Slow).',
        }
