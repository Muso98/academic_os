import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'director1'  # Target user from screenshot

try:
    user = User.objects.get(username=username)
    print(f"User found: {user.username}")
    
    if hasattr(user, 'employee_profile'):
        profile = user.employee_profile
        print(f"Profile: Found")
        print(f"Avatar Field Value: '{profile.avatar}'")
        
        if profile.avatar:
            print(f"Avatar URL: {profile.avatar.url}")
            print(f"Avatar Path: {profile.avatar.path}")
            print(f"File Exists on Disk: {os.path.exists(profile.avatar.path)}")
        else:
            print("Avatar field is empty/None")
    else:
        print("No EmployeeProfile attached to user.")
        
except User.DoesNotExist:
    print(f"User '{username}' not found.")
except Exception as e:
    print(f"Error: {e}")
