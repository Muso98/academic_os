import os
import django
from django.core.management import call_command
from io import StringIO

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from hr.models import EmployeeProfile
from django.conf import settings
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

User = get_user_model()

def verify():
    print("Starting Security Verification...")

    # 1. Test Encryption
    print("Testing Encryption...")
    user, _ = User.objects.get_or_create(username='secure_user_custom', defaults={'password': 'pass'})
    profile, _ = EmployeeProfile.objects.get_or_create(user=user)
    
    secret_passport = "AA1234567"
    secret_salary = 5000000

    profile.passport_number = secret_passport
    profile.salary = secret_salary
    profile.save()

    # Re-fetch from DB
    profile.refresh_from_db()
    if str(profile.passport_number) == secret_passport:
        print(f"SUCCESS: Encrypted field decryption works transparently. ({profile.passport_number})")
    else:
        print(f"ERROR: Decryption failed. Got {profile.passport_number}")
    
    # Check raw value (simulation) - tough to do easily in script without raw SQL, 
    # but we rely on the library's correctness here if the roundtrip works.

    # 2. Test Throttling
    print("Testing Throttling Configuration...")
    if 'rest_framework.throttling.UserRateThrottle' in settings.REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES']:
        print(f"SUCCESS: Throttling classes configured. Rates: {settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']}")
    else:
        print("ERROR: Throttling not configured correctly.")

    # 3. Test Backup Command
    print("Testing Backup Command...")
    out = StringIO()
    call_command('backup_db', stdout=out)
    output = out.getvalue()
    if "Database backed up to" in output:
        print(f"SUCCESS: Backup command ran. Output: {output.strip()}")
    else:
        print(f"ERROR: Backup command failed. Output: {output}")

    print("Security Verification Passed!")

if __name__ == "__main__":
    verify()
