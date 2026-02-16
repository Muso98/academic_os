import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from hr.models import EmployeeProfile

User = get_user_model()
users = User.objects.all()

print(f"Checking {users.count()} users...")

for user in users:
    try:
        profile = getattr(user, 'employee_profile', None)
        if profile:
            print(f"User: {user.username}")
            print(f"  Avatar Field: '{profile.avatar}'")
            print(f"  Avatar URL:   '{profile.avatar.url}'" if profile.avatar else "  Avatar URL:   None")
            
            # Check if file exists
            if profile.avatar:
                full_path = profile.avatar.path
                exists = os.path.exists(full_path)
                print(f"  File path:    {full_path}")
                print(f"  Exists?       {exists}")
        else:
            print(f"User: {user.username} (No Profile)")
    except Exception as e:
        print(f"Error checking {user.username}: {e}")
