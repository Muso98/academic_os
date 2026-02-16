from django.contrib import admin
from .models import Subject, LessonObservation, ObservationCriteria, ObservationScore, EducationalResource

class ObservationScoreInline(admin.TabularInline):
    model = ObservationScore
    extra = 1

@admin.register(LessonObservation)
class LessonObservationAdmin(admin.ModelAdmin):
    list_display = ('date', 'teacher', 'observer', 'subject', 'topic', 'total_score')
    list_filter = ('date', 'subject', 'observer')
    search_fields = ('teacher__username', 'teacher__first_name', 'teacher__last_name', 'topic')
    date_hierarchy = 'date'
    inlines = [ObservationScoreInline]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ObservationCriteria)
class ObservationCriteriaAdmin(admin.ModelAdmin):
    list_display = ('text', 'max_score')
    list_filter = ('max_score',)

@admin.register(EducationalResource)
class EducationalResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'uploaded_by', 'created_at')
    list_filter = ('created_at', 'uploaded_by')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
