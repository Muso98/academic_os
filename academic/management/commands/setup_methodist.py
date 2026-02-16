from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from academic.models import LessonObservation, EducationalResource

class Command(BaseCommand):
    help = 'Create Methodist group with appropriate permissions'

    def handle(self, *args, **kwargs):
        # Create or get Methodist group
        methodist_group, created = Group.objects.get_or_create(name='Methodist')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created Methodist group'))
        else:
            self.stdout.write(self.style.WARNING('Methodist group already exists'))
        
        # Clear existing permissions
        methodist_group.permissions.clear()
        
        # Add permissions for LessonObservation
        observation_ct = ContentType.objects.get_for_model(LessonObservation)
        observation_perms = Permission.objects.filter(
            content_type=observation_ct,
            codename__in=['view_lessonobservation', 'add_lessonobservation', 'change_lessonobservation']
        )
        
        # Add permissions for EducationalResource
        resource_ct = ContentType.objects.get_for_model(EducationalResource)
        resource_perms = Permission.objects.filter(
            content_type=resource_ct,
            codename__in=['view_educationalresource', 'add_educationalresource', 'change_educationalresource']
        )
        
        # Assign permissions
        for perm in observation_perms:
            methodist_group.permissions.add(perm)
            self.stdout.write(f'  Added permission: {perm.codename}')
        
        for perm in resource_perms:
            methodist_group.permissions.add(perm)
            self.stdout.write(f'  Added permission: {perm.codename}')
        
        self.stdout.write(self.style.SUCCESS('Methodist group configured successfully!'))
