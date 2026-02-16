from django.contrib import admin
from .models import Order, Report

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'title', 'date_signed', 'created_at']
    list_filter = ['date_signed', 'created_at']
    search_fields = ['order_number', 'title']
    ordering = ['-date_signed']
    date_hierarchy = 'date_signed'

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'report_type', 'status', 'submitted_at']
    list_filter = ['status', 'report_type', 'submitted_at']
    search_fields = ['title', 'teacher__username', 'teacher__first_name', 'teacher__last_name']
    ordering = ['-submitted_at']
    date_hierarchy = 'submitted_at'
    readonly_fields = ['submitted_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('teacher', 'title', 'report_type', 'file')
        }),
        ('Review', {
            'fields': ('status', 'admin_comment')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
