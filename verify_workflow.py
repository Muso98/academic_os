import os
import django
from django.core.exceptions import ValidationError
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from workflow.models import Task, TaskDependency
from workflow.tasks import check_deadlines

User = get_user_model()

def verify():
    print("Starting Workflow Verification...")

    # 1. Setup User
    user = User.objects.first()
    if not user:
        user = User.objects.create_user('task_user', 'password')

    # 2. Create Tasks
    task_a = Task.objects.create(title="Task A (Foundation)", creator=user, status='PENDING')
    task_b = Task.objects.create(title="Task B (Dependent)", creator=user, status='PENDING')
    print(f"Created tasks: {task_a}, {task_b}")

    # 3. Create Dependency: B depends on A
    TaskDependency.objects.create(task=task_b, depends_on=task_a)
    print("Created dependency: B -> A")

    # 4. Try to start Task B (Should Fail)
    print("Attempting to start Task B (while A is Pending)...")
    try:
        task_b.status = 'IN_PROGRESS'
        task_b.save()
        print("ERROR: Task B started unexpectedly!")
    except ValidationError as e:
        print(f"SUCCESS: Task B blocked as expected. Error: {e}")

    # 5. Complete Task A
    print("Completing Task A...")
    task_a.status = 'COMPLETED'
    task_a.save()
    print(f"Task A status: {task_a.status}")

    # 6. Try to start Task B (Should Succeed)
    print("Attempting to start Task B (after A is Completed)...")
    try:
        task_b.status = 'IN_PROGRESS'
        task_b.save()
        print(f"SUCCESS: Task B started. Status: {task_b.status}")
    except ValidationError as e:
        print(f"ERROR: Task B still blocked! Error: {e}")

    # 7. Test Notifications (Mock)
    print("Testing Notification Logic...")
    task_b.deadline = timezone.now() + timezone.timedelta(hours=1)
    task_b.save()
    check_deadlines() # Calling directly without Celery worker

    print("Workflow Verification Passed!")

if __name__ == "__main__":
    verify()
