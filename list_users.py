import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print(f"{'Username':<20} {'Email':<25} {'Groups':<30}")
print("-" * 75)

for user in User.objects.all():
    groups = ", ".join([g.name for g in user.groups.all()])
    if user.is_superuser:
        groups += " (Superuser)"
    print(f"{user.username:<20} {user.email:<25} {groups:<30}")
