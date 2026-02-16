from django.db import models
from django.conf import settings
from core.models import UUIDModel
from django.core.exceptions import ValidationError

class Task(UUIDModel):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('VERIFIED', 'Verified'),
    )
    
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_tasks', blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validation: check dependencies before starting the task
        if self.status in ['IN_PROGRESS', 'COMPLETED', 'VERIFIED']:
            pending_dependencies = self.dependencies.exclude(depends_on__status='COMPLETED').exclude(depends_on__status='VERIFIED')
            if pending_dependencies.exists():
                unfinished_tasks = ", ".join([dep.depends_on.title for dep in pending_dependencies])
                raise ValidationError(f"Cannot start task. Dependencies not completed: {unfinished_tasks}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"

class TaskDependency(UUIDModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies')
    depends_on = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='required_by')

    class Meta:
        unique_together = ('task', 'depends_on')

    def clean(self):
        if self.task == self.depends_on:
            raise ValidationError("A task cannot depend on itself.")
        # Simple circular check could be added here, but for MVP we skip deep recursion check
    
    def __str__(self):
        return f"{self.task.title} -> {self.depends_on.title}"

class TaskAttachment(UUIDModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.task.title}"
