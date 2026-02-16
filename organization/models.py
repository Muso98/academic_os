from django.db import models
from core.models import UUIDModel
from django.conf import settings

class Organization(UUIDModel):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

class Department(UUIDModel):
    """
    Kafedra (e.g., Aniq fanlar, Ijtimoiy fanlar)
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class Unit(UUIDModel):
    """
    Metod birlashma (e.g., Matematika, Fizika)
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=255)
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_units')

    def __str__(self):
        return f"{self.name} - {self.department.name}"
