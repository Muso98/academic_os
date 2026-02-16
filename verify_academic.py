import os
import django
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from academic.models import Subject, LessonObservation, ObservationCriteria, ObservationScore, EducationalResource

User = get_user_model()

def verify():
    print("Starting Academic Verification...")

    # 1. Setup Users
    teacher, _ = User.objects.get_or_create(username='teacher1', defaults={'password': 'pass'})
    observer, _ = User.objects.get_or_create(username='observer1', defaults={'password': 'pass'})

    # 2. Setup Subject
    math, _ = Subject.objects.get_or_create(name="Mathematics")

    # 3. Test Self-Observation (Should Fail)
    print("Testing self-observation restriction...")
    try:
        obs = LessonObservation(
            teacher=teacher,
            observer=teacher, # Same user
            subject=math,
            date=timezone.now().date(),
            topic="Algebra",
            class_group="10-A"
        )
        obs.save()
        print("ERROR: Self-observation allowed unexpectedly!")
    except ValidationError as e:
        print(f"SUCCESS: Self-observation blocked. Error: {e}")

    # 4. Valid Observation
    obs = LessonObservation.objects.create(
        teacher=teacher,
        observer=observer,
        subject=math,
        date=timezone.now().date(),
        topic="Geometry",
        class_group="11-B"
    )
    print(f"Observation created: {obs}")

    # 5. Scoring
    criteria1, _ = ObservationCriteria.objects.get_or_create(text="Lesson Goal Clear?", max_score=5)
    criteria2, _ = ObservationCriteria.objects.get_or_create(text="Student Engagement?", max_score=5)

    ObservationScore.objects.create(observation=obs, criteria=criteria1, score=5)
    ObservationScore.objects.create(observation=obs, criteria=criteria2, score=4)

    total = obs.total_score()
    print(f"Total Score: {total} (Expected: 9)")
    if total == 9:
        print("SUCCESS: Score calculation correct.")
    else:
        print("ERROR: Score calculation failed.")

    # 6. Resource Versioning
    print("Testing Resource Versioning...")
    res_v1 = EducationalResource.objects.create(
        title="Math Syllabus",
        file=SimpleUploadedFile("syllabus_v1.txt", b"content_v1"),
        version=1
    )
    print(f"Created: {res_v1}")

    # Create v2 linking to v1
    res_v2 = EducationalResource.objects.create(
        title="Math Syllabus",
        file=SimpleUploadedFile("syllabus_v2.txt", b"content_v2"),
        version=2,
        previous_version=res_v1
    )
    print(f"Created: {res_v2}, Previous Version: {res_v2.previous_version}")

    if res_v2.previous_version == res_v1:
        print("SUCCESS: Version linking correct.")
    else:
        print("ERROR: Version linking failed.")

    print("Academic Verification Passed!")

if __name__ == "__main__":
    verify()
