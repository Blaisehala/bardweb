from django.db import models
from django.contrib.auth.models import User
import secrets
import string

# Create your models here.

class MemmberNumber(models.Model):
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

