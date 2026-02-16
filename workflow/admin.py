from django.contrib import admin
from .models import Task, TaskDependency, TaskAttachment

class TaskDependencyInline(admin.TabularInline):
    model = TaskDependency
    fk_name = 'task'
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline', 'creator')
    list_filter = ('status', 'priority', 'deadline')
    filter_horizontal = ('assignees',)
    inlines = [TaskDependencyInline]
    search_fields = ('title', 'description')

@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'uploaded_at')
