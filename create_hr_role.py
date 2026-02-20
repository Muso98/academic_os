import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
django.setup()

def create_hr_manager_role():
    # 1. Create the Group
    hr_group, created = Group.objects.get_or_create(name='HR')
    
    if created:
        print("Created new HR group.")
    else:
        print("HR group already exists.")

    # 2. Get relevant content types
    # We want HR to manage Users (add, change, view)
    user_ct = ContentType.objects.get(app_label='users', model='user')
    # HR manages KPI Records and Certificates
    kpi_record_ct = ContentType.objects.get(app_label='hr', model='kpirecord')
    certificate_ct = ContentType.objects.get(app_label='hr', model='certificate')
    
    # We also want them to VIEW Organization info, but maybe not delete it
    org_ct = ContentType.objects.get(app_label='organization', model='organization')
    dep_ct = ContentType.objects.get(app_label='organization', model='department')
    unit_ct = ContentType.objects.get(app_label='organization', model='unit')

    # 3. Assign Permissions
    permissions_to_add = [
        # Users
        Permission.objects.get(content_type=user_ct, codename='add_user'),
        Permission.objects.get(content_type=user_ct, codename='change_user'),
        Permission.objects.get(content_type=user_ct, codename='view_user'),
        
        # KPI Records
        Permission.objects.get(content_type=kpi_record_ct, codename='add_kpirecord'),
        Permission.objects.get(content_type=kpi_record_ct, codename='change_kpirecord'),
        Permission.objects.get(content_type=kpi_record_ct, codename='view_kpirecord'),
        Permission.objects.get(content_type=kpi_record_ct, codename='delete_kpirecord'),
        
        # Certificates
        Permission.objects.get(content_type=certificate_ct, codename='add_certificate'),
        Permission.objects.get(content_type=certificate_ct, codename='change_certificate'),
        Permission.objects.get(content_type=certificate_ct, codename='view_certificate'),
        Permission.objects.get(content_type=certificate_ct, codename='delete_certificate'),
        
        # Organization Info (View only)
        Permission.objects.get(content_type=org_ct, codename='view_organization'),
        Permission.objects.get(content_type=dep_ct, codename='view_department'),
        Permission.objects.get(content_type=unit_ct, codename='view_unit'),
    ]

    hr_group.permissions.set(permissions_to_add)
    print("Successfully assigned 14 specific permissions to 'HR' group.")

if __name__ == '__main__':
    create_hr_manager_role()
