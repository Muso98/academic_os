from django.contrib import admin
from .models import KPIIndicator, KPIRecord, Certificate, SickLeave

@admin.register(KPIIndicator)
class KPIIndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'description')
    search_fields = ('name', 'description')
    list_filter = ('weight',)

@admin.register(KPIRecord)
class KPIRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'indicator', 'score_obtained', 'date_achieved', 'verified')
    list_filter = ('verified', 'date_achieved', 'indicator')
    search_fields = ('user__username', 'indicator__name')
    date_hierarchy = 'date_achieved'
    list_editable = ('verified',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee', 'issuer', 'date_issued', 'expiry_date', 'is_expired')
    list_filter = ('date_issued', 'expiry_date')
    search_fields = ('name', 'employee__username', 'employee__first_name', 'employee__last_name', 'issuer')
    date_hierarchy = 'date_issued'
    ordering = ['-date_issued']
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'

@admin.register(SickLeave)
class SickLeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'days_count', 'status', 'submitted_at', 'reviewed_by')
    list_filter = ('status', 'start_date')
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name')
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']
    readonly_fields = ('submitted_at', 'reviewed_at', 'days_count')

    def days_count(self, obj):
        return obj.days_count
    days_count.short_description = "Kunlar soni"
