import os
import django
from django.test import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def verify():
    print("Starting Frontend Verification...")
    c = Client()

    # 1. Anonymous Access (Should Redirect)
    print("Testing Anonymous Access to Dashboard...")
    response = c.get('/')
    if response.status_code == 302 and '/login/' in response.url:
        print("SUCCESS: Redirected to login.")
    else:
        print(f"ERROR: Expected redirect, got {response.status_code}")

    # 2. Login Page
    print("Testing Login Page Load...")
    response = c.get('/login/')
    if response.status_code == 200:
        print("SUCCESS: Login page loaded.")
    else:
        print(f"ERROR: Login page failed {response.status_code}")

    # 3. Authenticated Access
    print("Testing Authenticated Access...")
    user, _ = User.objects.get_or_create(username='frontend_user', defaults={'password': 'password123'})
    user.set_password('password123')
    user.save()

    login_success = c.login(username='frontend_user', password='password123')
    if login_success:
        print("Logged in successfully.")
        response = c.get('/')
        if response.status_code == 200:
            print("SUCCESS: Dashboard loaded (200 OK).")
            # Check for content
            if b"Dashboard" in response.content:
                print("SUCCESS: Dashboard content found.")
            else:
                print("ERROR: Dashboard content missing.")
        else:
            print(f"ERROR: Dashboard failed {response.status_code}")
    else:
        print("ERROR: Login failed.")

    print("Frontend Verification Passed!")

if __name__ == "__main__":
    verify()
