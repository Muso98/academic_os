from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Organization, Department, Unit

@admin.register(Organization)
class OrganizationAdmin(TranslationAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(TranslationAdmin):
    list_display = ('name', 'organization', 'head')
    list_filter = ('organization',)
    search_fields = ('name', 'organization__name')

@admin.register(Unit)
class UnitAdmin(TranslationAdmin):
    list_display = ('name', 'department', 'head')
    list_filter = ('department__organization', 'department')
    search_fields = ('name', 'department__name')
