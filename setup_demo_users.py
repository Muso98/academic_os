import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from hr.models import EmployeeProfile

User = get_user_model()

def create_demo_users():
    password = 'password123'
    
    # 1. Admin
    admin, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    admin.set_password(password)
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f"✅ Admin: admin / {password}")

    # 2. Director
    director_group, _ = Group.objects.get_or_create(name='Director')
    director, created = User.objects.get_or_create(username='director1', defaults={'email': 'director@example.com', 'first_name': 'Ali', 'last_name': 'Valiyev'})
    director.set_password(password)
    director.save()
    director.groups.add(director_group)
    print(f"✅ Director: director1 / {password}")

    # 3. Methodist
    methodist_group, _ = Group.objects.get_or_create(name='Methodist')
    methodist, created = User.objects.get_or_create(username='methodist1', defaults={'email': 'methodist@example.com', 'first_name': 'Guli', 'last_name': 'Karimova'})
    methodist.set_password(password)
    methodist.save()
    methodist.groups.add(methodist_group)
    print(f"✅ Methodist: methodist1 / {password}")

    # 4. Teacher
    teacher_group, _ = Group.objects.get_or_create(name='Teacher')
    teacher, created = User.objects.get_or_create(username='teacher1', defaults={'email': 'teacher@example.com', 'first_name': 'Olim', 'last_name': 'Olimov'})
    teacher.set_password(password)
    teacher.save()
    teacher.groups.add(teacher_group)
    
    # Create profile for teacher if missing
    if not hasattr(teacher, 'employee_profile'):
        EmployeeProfile.objects.create(
            user=teacher,
            qualification_category='Oliy toifa',
            employment_contract_end_date=timezone.now().date()
        )
    
    print(f"✅ Teacher: teacher1 / {password}")

if __name__ == '__main__':
    create_demo_users()
