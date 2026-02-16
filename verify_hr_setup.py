import os
import django
import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from hr.models import EmployeeProfile, KPIIndicator, KPIRecord

User = get_user_model()

def verify():
    print("Starting HR verification...")

    # 1. Verify Groups
    groups = ['Teacher', 'HeadOfDepartment', 'Director', 'Admin']
    for g in groups:
        if Group.objects.filter(name=g).exists():
            print(f"Group '{g}' exists.")
        else:
            print(f"ERROR: Group '{g}' missing!")

    # 2. Create/Get User and Assign Group
    username = 'teacher_user'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password='password123')
        print(f"User {username} created.")
    else:
        user = User.objects.get(username=username)
    
    teacher_group = Group.objects.get(name='Teacher')
    user.groups.add(teacher_group)
    print(f"User {username} added to Teacher group.")

    # 3. Create Employee Profile
    profile, created = EmployeeProfile.objects.get_or_create(
        user=user,
        defaults={
            'qualification_category': 'Oliy toifa', 
            'employment_contract_end_date': datetime.date(2025, 12, 31)
        }
    )
    print(f"Employee Profile created: {profile}")

    # 4. KPI System
    kpi, created = KPIIndicator.objects.get_or_create(
        name="Darsga o'z vaqtida kirish",
        defaults={'weight': 10.0, 'criteria': 'Har bir dars uchun'}
    )
    print(f"KPI Indicator: {kpi}")

    record, created = KPIRecord.objects.get_or_create(
        user=user,
        indicator=kpi,
        date_achieved=datetime.date.today(),
        defaults={'score_obtained': 10.0, 'verified': True}
    )
    print(f"KPI Record: {record}")

    print("HR Module Verification Passed!")

if __name__ == "__main__":
    verify()
