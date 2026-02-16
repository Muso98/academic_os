from django.contrib import admin
from .models import Organization, Department, Unit

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'head')
    list_filter = ('organization',)
    search_fields = ('name', 'organization__name')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'head')
    list_filter = ('department__organization', 'department')
    search_fields = ('name', 'department__name')
