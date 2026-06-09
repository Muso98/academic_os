from django.core.management.base import BaseCommand
from organization.models import Organization
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from hr.models import EmployeeProfile
from users.views import SCHOOL_ROLES

User = get_user_model()

class Command(BaseCommand):
    help = 'Baza uchun namunaviy maktab va xodimlarni yaratadi'

    def handle(self, *args, **kwargs):
        # 1. Tashkilot yaratish
        self.stdout.write("Maktab ma'lumotlarini qo'shish...")
        # Since it's a singleton pattern logically, we use first() or get_or_create
        org = Organization.objects.first()
        if not org:
            org = Organization(id=1)
        
        # O'zbek tili
        org.name_uz = "43-sonli umumiy o'rta ta'lim maktabi"
        org.region_uz = "Angor tumani"
        org.address_uz = "Surxondaryo viloyati, Angor tumani"
        org.director_name_uz = "Tashkilot rahbari"

        # Rus tili
        org.name_ru = "Общая средняя школа № 43"
        org.region_ru = "Ангорский район"
        org.address_ru = "Сурхандарьинская область, Ангорский район"
        org.director_name_ru = "Руководитель организации"

        # Ingliz tili
        org.name_en = "General Secondary School No. 43"
        org.region_en = "Angor district"
        org.address_en = "Surkhandarya region, Angor district"
        org.director_name_en = "Head of Organization"

        org.save()
        self.stdout.write(self.style.SUCCESS("Maktab muvaffaqiyatli qo'shildi/yangilandi!"))

        # 2. Xodimlarni yaratish
        self.stdout.write("Barcha lavozimlar (rollar) bo'yicha xodimlarni yaratish...")
        
        default_password = "Maktab2026"
        
        for role_key, role_label in SCHOOL_ROLES:
            username = role_key.lower()
            
            # Guruh yaratish yoki olish
            group, _ = Group.objects.get_or_create(name=role_key)
            
            # Xodimni yaratish
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=default_password,
                    first_name=role_label,
                    last_name="Testov"
                )
                user.groups.add(group)
                EmployeeProfile.objects.get_or_create(user=user)
                self.stdout.write(f"- Yaratildi: {username} (Rol: {role_label})")
            else:
                self.stdout.write(f"- Allaqachon mavjud: {username}")

        self.stdout.write(self.style.SUCCESS(f"Barcha xodimlar muvaffaqiyatli yaratildi! Parol: {default_password}"))
