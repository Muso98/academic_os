from django.db import models
from django.conf import settings
from core.models import UUIDModel
from django.core.exceptions import ValidationError

class Subject(UUIDModel):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class ObservationCriteria(UUIDModel):
    text = models.CharField(max_length=500)
    max_score = models.PositiveIntegerField(default=5)
    
    def __str__(self):
        return self.text[:50]

class LessonObservation(UUIDModel):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='observations_received')
    observer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='observations_made')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    topic = models.CharField(max_length=255)
    class_group = models.CharField(max_length=50, help_text="e.g. 10-'A'")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        # Only validate if observer is set (it may not be set yet during creation)
        if hasattr(self, 'observer_id') and self.observer_id and self.teacher == self.observer:
            raise ValidationError("A teacher cannot observe their own lesson.")

    def save(self, *args, **kwargs):
        # Don't call clean() here - it will be called by forms when needed
        # This prevents errors when observer is not yet set
        super().save(*args, **kwargs)

    def total_score(self):
        scores = self.scores.all()
        if not scores:
            return 0
        return sum(s.score for s in scores)

    def __str__(self):
        return f"{self.date} - {self.teacher} ({self.topic})"

class ObservationScore(UUIDModel):
    observation = models.ForeignKey(LessonObservation, on_delete=models.CASCADE, related_name='scores')
    criteria = models.ForeignKey(ObservationCriteria, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('observation', 'criteria')

    def clean(self):
        if self.score > self.criteria.max_score:
            raise ValidationError(f"Score {self.score} exceeds max score {self.criteria.max_score}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class EducationalResource(UUIDModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    version = models.PositiveIntegerField(default=1)
    
    previous_version = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_version')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (v{self.version})"
