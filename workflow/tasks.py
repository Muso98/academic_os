from celery import shared_task
from django.utils import timezone
from .models import Task
from datetime import timedelta

@shared_task
def check_deadlines():
    now = timezone.now()
    # 24 hours from now
    tomorrow = now + timedelta(days=1)
    # 1 hour from now
    next_hour = now + timedelta(hours=1)

    # Tasks due in 24 hours (+/- 5 mins buffer)
    tasks_due_24h = Task.objects.filter(
        deadline__gte=tomorrow - timedelta(minutes=5),
        deadline__lte=tomorrow + timedelta(minutes=5),
        status__in=['PENDING', 'IN_PROGRESS']
    )

    for task in tasks_due_24h:
        print(f"NOTIFICATION: Task '{task.title}' is due in 24 hours!")
        # In real app: send_email or push notification

    # Tasks due in 1 hour
    tasks_due_1h = Task.objects.filter(
        deadline__gte=next_hour - timedelta(minutes=5),
        deadline__lte=next_hour + timedelta(minutes=5),
        status__in=['PENDING', 'IN_PROGRESS']
    )

    for task in tasks_due_1h:
        print(f"NOTIFICATION: Task '{task.title}' is due in 1 hour!")
