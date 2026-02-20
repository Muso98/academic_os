import os
import polib
from pathlib import Path

BASE_DIR = Path('m:/my projects/ACADEMIC OS/academic_os')
LOCALE_DIR = BASE_DIR / "locale"
os.makedirs(LOCALE_DIR, exist_ok=True)

translations = {
    # Russian
    "ru": {
        "Foydalanuvchi": "Пользователь",
        "Foydalanuvchilar": "Пользователи",
        "Tashkilot": "Организация",
        "Tashkilotlar": "Организации",
        "Nomi": "Название",
        "Tuman/Shahar nomi": "Район/Город",
        "Masalan: Angor tumani": "Например: Ангорский район",
        "Direktor ism-sharifi": "ФИО Директора",
        "Masalan: B.Xolbutayev": "Например: Б.Холбутаев",
        "Telefon raqami": "Номер телефона",
        "Manzil": "Адрес",
        "Kafedra": "Кафедра",
        "Kafedralar": "Кафедры",
        "Mudiri": "Заведующий",
        "Metod birlashma": "Метод. объединение",
        "Metod birlashmalar": "Метод. объединения",
        "Rahbari": "Руководитель",
        "Xodim Profili": "Профиль сотрудника",
        "Xodimlar Profillari": "Профили сотрудников",
        "Pasport raqami/JShSHIR": "Номер паспорта/ПИНФЛ",
        "Oylik maosh (UZS)": "Месячная зарплата (UZS)",
        "Oylik maosh": "Месячная зарплата",
        "Shartnoma tugash sanasi": "Дата окончания контракта",
        "Malaka toifasi / Aniq vazifasi": "Категория квалификации / Точная должность",
        "Qiyofacha (Avatar)": "Аватар",
        "Tarjimayi hol (Bio)": "Биография (Bio)",
        "Sertifikatlar (JSON)": "Сертификаты (JSON)",
        "Xodim faoliyati va shaxsiy tafsilotlari": "Деятельность сотрудника и личные данные",
        "Shaxsiy ma'lumotlar (Foydalanuvchi)": "Личные данные (Пользователь)",
        "Guruhlar va Ruxsatlar (Vazifasi)": "Группы и Разрешения (Должность)",
        "Vazifasi (Guruhlar)": "Должность (Группы)",
        "KPI Indikatori": "Индикатор KPI",
        "KPI Indikatorlari": "Индикаторы KPI",
        "Tavsif": "Описание",
        "Vazni": "Вес",
        "Mezonlar": "Критерии",
        "Ushbu indikator uchun beriladigan ball": "Баллы за этот индикатор",
        "Ushbu KPI ga erishish qoidalari": "Правила достижения этого KPI",
        "KPI Yozuvi (Natijasi)": "Запись KPI (Результат)",
        "KPI Yozuvlari (Natijalari)": "Записи KPI (Результаты)",
        "Indikator": "Индикатор",
        "Erishilgan sana": "Дата достижения",
        "Olingan ball": "Полученный балл",
        "Isbotlovchi hujjat": "Документ-подтверждение",
        "Tasdiqlangan": "Подтверждено",
        "Sertifikat": "Сертификат",
        "Sertifikatlar": "Сертификаты",
        "Ma'lumotnoma Tartib Raqami": "Номер справки",
        "Ma'lumotnoma Tartib Raqamlari": "Номера справок",
        "Yil (Masalan: 2026)": "Год (Например: 2026)",
        "Yil": "Год",
        "Oxirgi berilgan ma'lumotnoma raqami": "Последний выданный номер справки",
        "Oxirgi raqam": "Последний номер"
    },
    # English
    "en": {
        "Foydalanuvchi": "User",
        "Foydalanuvchilar": "Users",
        "Tashkilot": "Organization",
        "Tashkilotlar": "Organizations",
        "Nomi": "Name",
        "Tuman/Shahar nomi": "District/City",
        "Masalan: Angor tumani": "Example: Angor district",
        "Direktor ism-sharifi": "Director Full Name",
        "Masalan: B.Xolbutayev": "Example: B.Kholbutayev",
        "Telefon raqami": "Phone Number",
        "Manzil": "Address",
        "Kafedra": "Department",
        "Kafedralar": "Departments",
        "Mudiri": "Head",
        "Metod birlashma": "Methodological Unit",
        "Metod birlashmalar": "Methodological Units",
        "Rahbari": "Leader",
        "Xodim Profili": "Employee Profile",
        "Xodimlar Profillari": "Employee Profiles",
        "Pasport raqami/JShSHIR": "Passport Number/PINFL",
        "Oylik maosh (UZS)": "Monthly Salary (UZS)",
        "Oylik maosh": "Monthly Salary",
        "Shartnoma tugash sanasi": "Contract End Date",
        "Malaka toifasi / Aniq vazifasi": "Qualification Category / Exact Position",
        "Qiyofacha (Avatar)": "Avatar",
        "Tarjimayi hol (Bio)": "Biography (Bio)",
        "Sertifikatlar (JSON)": "Certificates (JSON)",
        "Xodim faoliyati va shaxsiy tafsilotlari": "Employee Activity and Personal Details",
        "Shaxsiy ma'lumotlar (Foydalanuvchi)": "Personal details (User)",
        "Guruhlar va Ruxsatlar (Vazifasi)": "Groups and Permissions (Position)",
        "Vazifasi (Guruhlar)": "Position (Groups)",
        "KPI Indikatori": "KPI Indicator",
        "KPI Indikatorlari": "KPI Indicators",
        "Tavsif": "Description",
        "Vazni": "Weight",
        "Mezonlar": "Criteria",
        "Ushbu indikator uchun beriladigan ball": "Points given for this indicator",
        "Ushbu KPI ga erishish qoidalari": "Rules for reaching this KPI",
        "KPI Yozuvi (Natijasi)": "KPI Record (Result)",
        "KPI Yozuvlari (Natijalari)": "KPI Records (Results)",
        "Indikator": "Indicator",
        "Erishilgan sana": "Date Achieved",
        "Olingan ball": "Score Obtained",
        "Isbotlovchi hujjat": "Proof Document",
        "Tasdiqlangan": "Verified",
        "Sertifikat": "Certificate",
        "Sertifikatlar": "Certificates",
        "Ma'lumotnoma Tartib Raqami": "Certificate Sequence Number",
        "Ma'lumotnoma Tartib Raqamlari": "Certificate Sequence Numbers",
        "Yil (Masalan: 2026)": "Year (Example: 2026)",
        "Yil": "Year",
        "Oxirgi berilgan ma'lumotnoma raqami": "Last issued certificate number",
        "Oxirgi raqam": "Last number"
    }
}

for lang, messages in translations.items():
    lang_dir = LOCALE_DIR / lang / "LC_MESSAGES"
    os.makedirs(lang_dir, exist_ok=True)
    
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'system@localhost',
        'POT-Creation-Date': '2007-10-18 14:00+0100',
        'PO-Revision-Date': '2007-10-18 14:00+0100',
        'Last-Translator': 'system',
        'Language-Team': f'{lang} <localhost>',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }
    
    for msgid, msgstr in messages.items():
        entry = polib.POEntry(msgid=msgid, msgstr=msgstr, occurrences=[])
        po.append(entry)
    
    po.save(str(lang_dir / 'django.po'))
    po.save_as_mofile(str(lang_dir / 'django.mo'))

print("Updated translation files and mapped user profile details successfully.")
