from django.contrib import admin
from . models import MemberNumber
from django.utils.html import format_html


@admin.register(MemberNumber)
class MemberNumberAdmin(admin.ModelAdmin):
    list_display = [
        'member_number',
        'secret_code_display',
        'phone_number', 
        'amount_paid',
        'payment_date',
        'status_badge',
        'registered_user'
    ]

    list_filter = ['is_registered', 'payment_date']
    search_fields = ['member_number', 'phone_number', 'secret_code', 'registered_user__username']
    readonly_fields = ['secret_code', 'registered_at', 'created_at']

    fieldsets = (
        ('Member Information', {
            'fields': ('member_number', 'secret_code', 'phone_number', 'amount_paid', 'payment_date')
        }),
        ('Registration Status', {
            'fields': ('is_registered', 'registered_user', 'registered_at')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
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


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Display the secret code after saving
        if not change:  # Only for new records
            from django.contrib import messages
            messages.success(
                request, 
                f'Member #{obj.member_number} created with Secret Code: {obj.secret_code}. '
                f'Send this to the member at {obj.phone_number}.'
            )