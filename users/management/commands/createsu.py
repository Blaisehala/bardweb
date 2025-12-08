import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@bardweb.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not password:
            self.stdout.write(self.style.ERROR('❌ DJANGO_SUPERUSER_PASSWORD not set in environment'))
            return
        
        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'⚠️ Superuser "{username}" already exists'))
            return
        
        # Create the superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating superuser: {str(e)}'))