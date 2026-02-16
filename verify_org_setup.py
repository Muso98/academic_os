import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from organization.models import Organization, Department, Unit
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def verify():
    print("Starting verification...")

    # 1. Create User
    username = 'testadmin'
    password = 'testpassword123'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, password=password, email='admin@example.com')
        print(f"User {username} created.")
    else:
        user = User.objects.get(username=username)
        print(f"User {username} already exists.")

    # 2. Generate Token
    refresh = RefreshToken.for_user(user)
    print(f"Access Token: {str(refresh.access_token)[:20]}...")
    
    # 3. Create Organization Structure
    org, created = Organization.objects.get_or_create(name="Test School", defaults={'slug': 'test-school'})
    print(f"Organization: {org}")

    dept, created = Department.objects.get_or_create(name="Exact Sciences", organization=org, defaults={'head': user})
    print(f"Department: {dept}")

    unit, created = Unit.objects.get_or_create(name="Mathematics", department=dept, defaults={'head': user})
    print(f"Unit: {unit}")

    print("Verification passed!")

if __name__ == "__main__":
    verify()
