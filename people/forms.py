from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    FAMILY_ROLE_CHOICES = [
        ('head', 'New Family Head (Creates a new group)'),
        ('member', 'Member of Existing Family'),
    ]
    family_role = forms.ChoiceField(
        choices=FAMILY_ROLE_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Group Membership Role",
        required=True
    )
    create_user_account = forms.BooleanField(required=False, label="Create User Account for this Member", help_text="A user account will be created using the email as username.")
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Provide Password'}), required=False, label="Account Password")
    can_view_directory = forms.BooleanField(required=False, label="Grant Directory Access", initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            from accounts.models import User
            # If user account exists, hide setup fields
            if self.instance.email and User.objects.filter(email=self.instance.email).exists():
                fields_to_hide = ['family_role', 'family_group', 'create_user_account', 'user_password']
                for field in fields_to_hide:
                    if field in self.fields:
                        del self.fields[field]

    class Meta:
        model = Person
        fields = [
            'full_name', 'native_gam', 'current_city', 
            'state', 'phone_number', 'email', 'age', 'occupation', 'photo', 
            'family_role', 'family_group'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Age'}),
            'native_gam': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Native Village'}),
            'current_city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Current City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Occupation (Optional)'}),
            'family_group': forms.Select(attrs={'class': 'form-input'}),
        }
        labels = {
            'full_name': 'Full Name',
            'native_gam': 'Native Village (Gam)',
            'current_city': 'Current City',
            'phone_number': 'Phone Number',
            'photo': 'Profile Photo',
            'family_group': 'Join Existing Family'
        }

    def clean(self):
        cleaned_data = super().clean()
        family_role = cleaned_data.get('family_role')
        family_group = cleaned_data.get('family_group')
        
        if family_role == 'member' and not family_group:
            self.add_error('family_group', "Please select an existing family group if choosing 'Member'.")
        
        # Keep previous validations
        age = cleaned_data.get('age')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone_number')
        create_account = cleaned_data.get('create_user_account')
        password = cleaned_data.get('user_password')

        # Conditional checks for age < 16
        if age and age >= 16:
            if not email:
                self.add_error('email', "Email is required for members 16 or older.")
            if not phone:
                self.add_error('phone_number', "Phone number is required for members 16 or older.")

        # Account creation logic checks
        if create_account:
            if not email:
                self.add_error('create_user_account', "Email is required to create a user account.")
            if not password:
                self.add_error('user_password', "Password is required for new accounts.")
            
            # Check if email/phone already taken in User model
            from accounts.models import User
            if email and User.objects.filter(email=email).exists():
                self.add_error('email', "A user with this email already exists.")
            if phone and User.objects.filter(phone_number=phone).exists():
                self.add_error('phone_number', "A user with this phone number already exists.")

        return cleaned_data
