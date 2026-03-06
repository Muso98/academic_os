from django.core.management.base import BaseCommand
from academic.models import ObservationCriteria

class Command(BaseCommand):
    help = "Sets up default observation criteria for Academic OS"

    def handle(self, *args, **kwargs):
        criteria_list = [
            {"text": "O'qituvchining darsga farovon tayyorgarligi", "max_score": 5},
            {"text": "Dars maqsadlarining to'g'ri belgilanishi", "max_score": 5},
            {"text": "Barcha o'quvchilarni faol jalb eta olishi", "max_score": 5},
            {"text": "Pedagogik texnologiyalardan samarali o'rni", "max_score": 5},
            {"text": "Vaqtdan unumli foydalanish", "max_score": 5},
        ]

        count = 0
        for item in criteria_list:
            obj, created = ObservationCriteria.objects.get_or_create(
                text=item['text'],
                defaults={'max_score': item['max_score']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Yaratildi: {obj.text}"))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Mavjud: {obj.text}"))

        self.stdout.write(self.style.SUCCESS(f"Jami {count} ta yangi mezon qo'shildi."))
