from django.db import models
from django.contrib.auth.models import User
import secrets
import string

# Create your models here.

class MemberNumber(models.Model):
    member_number = models.IntegerField(unique=True, verbose_name="Member Number")
    secret_code = models.CharField(max_length=8, unique=True, verbose_name="Secret Code")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    payment_date = models.DateField()


     # Registration tracking
    is_registered = models.BooleanField(default=False)
    registered_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    registered_at = models.DateTimeField(null=True, blank=True)

    # Admin notes
    notes = models.TextField(blank=True, help_text="Any additional notes about this member")
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.secret_code:
            # Generate random 6-character code (avoiding confusing characters)
            chars = string.ascii_uppercase.replace('O', '').replace('I', '').replace('Q', '') + string.digits.replace('0', '').replace('1', '')
            self.secret_code = ''.join(secrets.choice(chars) for _ in range(6))
        super().save(*args, **kwargs)


    def __str__(self):
        status = "✓ Registered" if self.is_registered else "⏳ Pending Registration"
        return f"Member #{self.member_number} - Code: {self.secret_code} ({status})"

        
    class Meta:
        verbose_name = "Member Number"
        verbose_name_plural ="Member Numbers"
        ordering = ['member_number']



class AlumniProfile(models.Model):
    YEAR_CHOICES = [(year, str(year)) for year in range(1950, 2030)]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_number = models.ForeignKey(MemberNumber, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Personal Information
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    year_graduated = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    current_location = models.CharField(max_length=100, blank=True)
    
    
    
    # Engagement
    is_mentor = models.BooleanField(default=False)
    is_looking_for_mentor = models.BooleanField(default=False)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volunteer_hours = models.IntegerField(default=0)
    
    # Social
    website = models.URLField(blank=True)
    Facebook_handle = models.CharField(max_length=50, blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Alumni Profile"
        verbose_name_plural = "Alumni Profiles"




class Post(models.Model):
    POST_TYPES = [
        ('update', 'General Update'),
        ('job', 'Job Posting'),
        ('event', 'Event'),
        ('achievement', 'Achievement'),
        ('memory', 'Memory'),
        ('opportunity', 'Opportunity'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='update')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    
    # For job postings
    job_title = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    job_link = models.URLField(blank=True)
    
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.post_type} - {self.created_at.strftime('%Y-%m-%d')}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} on {self.post}"


class Event(models.Model):
    EVENT_TYPES = [
        ('reunion', 'Reunion'),
        ('networking', 'Networking'),
        ('webinar', 'Webinar'),
        ('social', 'Social Gathering'),
        ('fundraiser', 'Fundraiser'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='networking')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_virtual = models.BooleanField(default=False)
    virtual_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='events_attending', blank=True)
    max_attendees = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def total_attendees(self):
        return self.attendees.count()

    def is_full(self):
        if self.max_attendees:
            return self.attendees.count() >= self.max_attendees
        return False

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.titlef