from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MemberNumber, AlumniProfile
from django.core.cache import cache


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    member_number = forms.IntegerField(
        required=True,
        label="Member Number",
        help_text="Enter your assigned member number"
    )
    secret_code = forms.CharField(
        max_length=8,
        required=True,
        label="Secret Code",
        help_text="Enter the 6-character secret code sent to you",
        widget=forms.TextInput(attrs={'style': 'text-transform: uppercase;'})
    )
    phone_number = forms.CharField(
        max_length=10,
        required=True,
        label="Phone Number",
        help_text="Enter your phone number (used for payment)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'member_number', 'secret_code', 'phone_number']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number').strip()
        # Remove spaces and standardize format
        phone = phone.replace(' ', '').replace('-', '')
        return phone

    def clean_secret_code(self):
        code = self.cleaned_data.get('secret_code').strip().upper()
        return code

    def clean(self):
        cleaned_data = super().clean()
        
        # 🔒 SECURITY: Rate limiting - prevent brute force
        ip = self.request.META.get('REMOTE_ADDR') if hasattr(self, 'request') else 'unknown'
        cache_key = f'registration_attempts_{ip}'
        
        attempts = cache.get(cache_key, 0)
        if attempts >= 5:
            raise forms.ValidationError(
                "Too many failed attempts. Please try again in 30 minutes or contact support."
            )
        
        member_number = cleaned_data.get('member_number')
        secret_code = cleaned_data.get('secret_code')
        phone_number = cleaned_data.get('phone_number')

        if member_number and secret_code and phone_number:
            try:
                # 🔒 CRITICAL: All 3 must match exactly
                member = MemberNumber.objects.get(
                    member_number=member_number,
                    secret_code=secret_code,
                    phone_number=phone_number
                )
            except MemberNumber.DoesNotExist:
                # Increment failed attempts
                cache.set(cache_key, attempts + 1, 1800)  # 30 minutes
                
                raise forms.ValidationError(
                    "Invalid credentials. Please verify your member number, secret code, and phone number. "
                    "All three must match our records exactly."
                )

            # 🔒 CRITICAL CHECK 1: Already registered?
            if member.is_registered:
                cache.set(cache_key, attempts + 1, 1800)
                raise forms.ValidationError(
                    "This member number has already been used to register an account. "
                    "Each member number can only be used once."
                )
            
            # 🔒 CRITICAL CHECK 2: Already linked to a user?
            if member.registered_user is not None:
                cache.set(cache_key, attempts + 1, 1800)
                raise forms.ValidationError(
                    "This member number is already linked to an account."
                )

            # Clear attempts on success
            cache.delete(cache_key)
            
            # Store for save()
            self.member = member

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # 🔒 CRITICAL: Mark as registered IMMEDIATELY
            member = self.member
            member.is_registered = True
            member.registered_user = user
            from django.utils import timezone
            member.registered_at = timezone.now()
            member.save()
            
            # Link to AlumniProfile
            profile, created = AlumniProfile.objects.get_or_create(user=user)
            profile.member_number = member
            profile.save()
        
        return user


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