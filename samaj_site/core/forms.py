from django import forms
from .models import Post, Member

class PostForm(forms.ModelForm):
    POST_TYPE_CHOICES = [
        ('text', 'Text'),
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    post_type = forms.ChoiceField(choices=POST_TYPE_CHOICES, required=True)
    title = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Write your post here...'}))
    file = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'file']

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get("post_type")
        content = cleaned_data.get("content")
        file = cleaned_data.get("file")

        # Validation rules
        if post_type == 'text' and not content:
            raise forms.ValidationError("Text post must have content.")
        if post_type in ['photo', 'video'] and not file:
            raise forms.ValidationError(f"{post_type.capitalize()} post must include a file.")


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'age', 'location', 'education', 'profession']

class HomePageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'file']