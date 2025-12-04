# admin.py

from django.contrib import admin
from .models import MemberNumber, AlumniProfile, Post, Comment, Event,Donation
from django.utils.html import format_html

@admin.register(MemberNumber)
class MemberNumberAdmin(admin.ModelAdmin):
    list_display = [
        'member_number',
        'full_name',
        'secret_code_display',
        'phone_number', 
        'amount_paid',
        'payment_date',
        'status_badge',
        'registered_user'
    ]
    list_filter = ['is_registered', 'payment_date']
    search_fields = [
        'member_number', 
        'phone_number', 
        'secret_code', 
        'first_name',
        'last_name',
        'registered_user__username'
    ]
    readonly_fields = ['secret_code', 'registered_at', 'created_at']
    
    fieldsets = (
        ('Member Information', {
            'fields': (
                'member_number', 
                'first_name',
                'last_name',
                'secret_code', 
                'phone_number', 
                'amount_paid', 
                'payment_date'
            )
        }),
        ('Registration Status', {
            'fields': ('is_registered', 'registered_user', 'registered_at')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        """Display full name in list view"""
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return "-"
    full_name.short_description = 'Full Name'
    
    def secret_code_display(self, obj):
        return format_html(
            '<code style="background-color: #f3f4f6; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 13px; font-family: monospace;">{}</code>',
            obj.secret_code
        )
    secret_code_display.short_description = 'Secret Code'
    
    def status_badge(self, obj):
        if obj.is_registered:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ REGISTERED</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #f59e0b; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">⏳ PENDING</span>'
            )
    status_badge.short_description = 'Status'


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'member_number', 'year_graduated', 'current_location', 'updated_at']
    list_filter = ['is_mentor', 'is_looking_for_mentor', 'year_graduated']
    search_fields = ['user__username', 'user__email', 'current_location']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'content_preview', 'total_likes', 'created_at']
    list_filter = ['post_type', 'created_at']
    search_fields = ['author__username', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'total_attendees', 'is_full']
    list_filter = ['event_type', 'date', 'is_virtual']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at']



@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'cause', 'payment_method', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'payment_method', 'cause', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'donor_phone', 'transaction_id']
    readonly_fields = ['created_at', 'completed_at']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor', 'donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'cause', 'message')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'mpesa_phone', 'transaction_id', 'is_completed', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )