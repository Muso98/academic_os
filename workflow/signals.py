from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Task
from core.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(m2m_changed, sender=Task.assignees.through)
def notify_task_assignment(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Notify users when they are assigned to a task.
    """
    if action == 'post_add':
        # 'instance' is the Task object because reverse=False (modifying task.assignees)
        # If reverse=True, instance would be the User, and we'd be modifying user.assigned_tasks
        
        if not reverse:
            task = instance
            assigned_users = User.objects.filter(pk__in=pk_set)
            
            for user in assigned_users:
                # Don't notify the creator if they assign themselves (optional logic)
                if user != task.creator:
                    Notification.objects.create(
                        recipient=user,
                        message=f"You have been assigned to a new task: '{task.title}' by {task.creator.username}.",
                        link=f"/tasks/{task.id}/", # Assuming standard detail view URL
                        notification_type='INFO'
                    )

@receiver(post_save, sender=Task)
def notify_task_status_change(sender, instance, created, **kwargs):
    """
    Notify creator when task is completed.
    """
    if not created:
        if instance.status == 'COMPLETED':
             Notification.objects.create(
                recipient=instance.creator,
                message=f"Task '{instance.title}' has been marked as COMPLETED.",
                link=f"/tasks/{instance.id}/",
                notification_type='SUCCESS'
            )
