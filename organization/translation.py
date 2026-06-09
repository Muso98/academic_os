from modeltranslation.translator import register, TranslationOptions
from .models import Organization, Department, Unit

@register(Organization)
class OrganizationTranslationOptions(TranslationOptions):
    fields = ('name', 'region', 'director_name', 'address')

@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Unit)
class UnitTranslationOptions(TranslationOptions):
    fields = ('name',)
