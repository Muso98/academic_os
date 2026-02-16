from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from hr.models import EmployeeProfile, KPIRecord

class Command(BaseCommand):
    help = 'Creates default user groups and permissions'

    def handle(self, *args, **options):
        groups = ['Teacher', 'HeadOfDepartment', 'Director', 'Admin']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(f'Group {group_name} already exists')

        # Assign basic permissions (Example)
        teacher_group = Group.objects.get(name='Teacher')
        # telecher can view their own KPI records (logic handled in views, but here we give model-level permission)
        ct = ContentType.objects.get_for_model(KPIRecord)
        permissions = Permission.objects.filter(content_type=ct, codename__in=['view_kpirecord', 'add_kpirecord'])
        teacher_group.permissions.set(permissions)
        
        self.stdout.write(self.style.SUCCESS('Permissions assigned successfully'))
