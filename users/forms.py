from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MemberNumber, AlumniProfile
from django.core.cache import cache


class UserRegisterForm (UserCreationForm):
    email = forms.EmailField()



    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form for updating user account information"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition'
            })


class AlumniProfileUpdateForm(forms.ModelForm):
    """Form for updating alumni profile information"""
    
    YEAR_CHOICES = [(year, str(year)) for year in range(1950, 2030)]
    
    year_graduated = forms.ChoiceField(
        choices=[('', 'Select Year')] + YEAR_CHOICES,
        required=False
    )
    
    class Meta:
        model = AlumniProfile
        fields = [
            'profile_picture',
            'bio',
            'year_graduated',
            'current_location',
            'website',
            'twitter_handle',
            'is_mentor',
            'is_looking_for_mentor',
        ]
        
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'current_location': forms.TextInput(attrs={
                'placeholder': 'e.g., Nairobi, Kenya'
            }),
            
            'website': forms.URLInput(attrs={
                'placeholder': 'https://yourwebsite.com'
            }),
            'twitter_handle': forms.TextInput(attrs={
                'placeholder': '@yourusername'
            }),
        }
        
        labels = {
            'bio': 'About Me',
            'year_graduated': 'Graduation Year',
            'current_location': 'Location',
            'current_company': 'Company',
            'job_title': 'Job Title',
            'industry': 'Industry',
            'linkedin_url': 'LinkedIn Profile',
            'website': 'Personal Website',
            'twitter_handle': 'Twitter Handle',
            'is_mentor': 'I am available as a mentor',
            'is_looking_for_mentor': 'I am looking for a mentor',
            'profile_picture': 'Profile Picture',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to form fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_mentor', 'is_looking_for_mentor', 'profile_picture']:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition'
                })
            elif field_name in ['is_mentor', 'is_looking_for_mentor']:
                field.widget.attrs.update({
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
                })