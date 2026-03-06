from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

SCHOOL_ROLES = [
    ('Director', "Direktor"),
    ('DeputyDirector', "Direktor o'rinbosari"),
    ('HeadOfDepartment', "Bo'lim/Kafedra mudiri"),
    ('Teacher', "O'qituvchi"),
    ('Methodist', "Metodist"),
    ('Accountant', "Buxgalter"),
    ('Librarian', "Kutubxonachi"),
    ('Psychologist', "Psixolog"),
    ('Secretary', "Kotib"),
    ('FacilitiesHead', "Xo'jalik bo'limi boshlig'i"),
    ('FacilitiesStaff', "Xo'jalik xodimi"),
    ('Technical', "Texnik xodim"),
]

class Command(BaseCommand):
    help = "Maktab xodimlarining rollarini (Django Groups) yaratadi"

    def handle(self, *args, **kwargs):
        created_count = 0
        for name, label in SCHOOL_ROLES:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Yaratildi: {name} ({label})"))
                created_count += 1
            else:
                self.stdout.write(f"  Mavjud: {name} ({label})")

        self.stdout.write(self.style.SUCCESS(
            f"\nJami {created_count} ta yangi rol yaratildi."
            if created_count else "\nBarcha rollar allaqachon mavjud."
        ))
