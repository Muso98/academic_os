from django.db import models
from core.models import UUIDModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Organization(UUIDModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Tuman/Shahar nomi"), help_text=_("Masalan: Angor tumani"))
    director_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Direktor ism-sharifi"), help_text=_("Masalan: B.Xolbutayev"))
    phone_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Telefon raqami"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Manzil"))
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = _('Tashkilot')
        verbose_name_plural = _('Tashkilotlar')

    def __str__(self):
        return self.name

class Department(UUIDModel):
    """
    Kafedra (e.g., Aniq fanlar, Ijtimoiy fanlar)
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments', verbose_name=_("Tashkilot"))
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments', verbose_name=_("Mudiri"))

    class Meta:
        verbose_name = _('Kafedra')
        verbose_name_plural = _('Kafedralar')

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class Unit(UUIDModel):
    """
    Metod birlashma (e.g., Matematika, Fizika)
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='units', verbose_name=_("Kafedra"))
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_units', verbose_name=_("Rahbari"))

    class Meta:
        verbose_name = _('Metod birlashma')
        verbose_name_plural = _('Metod birlashmalar')

    def __str__(self):
        return f"{self.name} - {self.department.name}"
