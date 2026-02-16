from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from hr.models import EmployeeProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test users for demonstration'

    def handle(self, *args, **options):
        users_data = [
            {'username': 'director1', 'password': 'password123', 'role': 'Director', 'first_name': 'Ali', 'last_name': 'Valiyev'},
            {'username': 'hod_math', 'password': 'password123', 'role': 'HeadOfDepartment', 'first_name': 'Hasan', 'last_name': 'Egamov'},
            {'username': 'hod_phys', 'password': 'password123', 'role': 'HeadOfDepartment', 'first_name': 'Husan', 'last_name': 'Olimov'},
            {'username': 'teacher_math1', 'password': 'password123', 'role': 'Teacher', 'first_name': 'Olim', 'last_name': 'Qodirov'},
            {'username': 'teacher_math2', 'password': 'password123', 'role': 'Teacher', 'first_name': 'Zarina', 'last_name': 'Nizomova'},
            {'username': 'teacher_phys1', 'password': 'password123', 'role': 'Teacher', 'first_name': 'Botir', 'last_name': 'Zokirov'},
            {'username': 'teacher_phys2', 'password': 'password123', 'role': 'Teacher', 'first_name': 'Maftuna', 'last_name': 'Karimova'},
        ]

        for data in users_data:
            user, created = User.objects.get_or_create(username=data['username'])
            user.set_password(data['password'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

            # Ensure profile exists
            EmployeeProfile.objects.get_or_create(user=user)

            # Assign Group
            group_name = data['role']
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} user: {user.username} ({group_name})"))

        self.stdout.write(self.style.SUCCESS("All test users created successfully."))
