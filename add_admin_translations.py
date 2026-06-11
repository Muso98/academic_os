import polib

admin_translations = {
    "Add": "Qo'shish",
    "Change": "O'zgartirish",
    "Delete": "O'chirish",
    "Save": "Saqlash",
    "Save and add another": "Saqlash va yana qo'shish",
    "Save and continue editing": "Saqlash va tahrirlashda davom etish",
    "Are you sure?": "Ishonchingiz komilmi?",
    "Yes, I'm sure": "Ha, ishonchim komil",
    "No, take me back": "Yo'q, orqaga qaytish",
    "Action:": "Harakat:",
    "Go": "Bajarish",
    "Filter": "Filtr",
    "Clear all filters": "Barcha filtrlarni tozalash",
    "Select all": "Barchasini tanlash",
    "Welcome,": "Xush kelibsiz,",
    "View site": "Saytni ko'rish",
    "Change password": "Parolni o'zgartirish",
    "Log out": "Chiqish",
    "Home": "Bosh sahifa",
    "Search": "Qidirish",
    "History": "Tarix",
    "View on site": "Saytda ko'rish",
    "Delete selected": "Tanlanganlarni o'chirish",
    "Select %s to change": "O'zgartirish uchun %s tanlang",
    "Select %s to view": "Ko'rish uchun %s tanlang",
    "Add %s": "%s qo'shish",
    "Change %s": "%s o'zgartirish",
    "Recent actions": "Oxirgi harakatlar",
    "My actions": "Mening harakatlarim",
    "None available": "Mavjud emas",
    "Unknown content": "Noma'lum kontent",
    "Authentication and Authorization": "Autentifikatsiya va avtorizatsiya",
    "Users": "Foydalanuvchilar",
    "Groups": "Guruhlar",
    "Added": "Qo'shildi",
    "Changed": "O'zgartirildi",
    "Deleted": "O'chirildi",
    "Date/time": "Sana/vaqt",
    "User": "Foydalanuvchi",
    "Action": "Harakat",
}

po_path = 'locale/uz/LC_MESSAGES/django.po'
try:
    po = polib.pofile(po_path)
    
    # Check existing msgids
    existing_msgids = {entry.msgid: entry for entry in po}
    
    for en_text, uz_text in admin_translations.items():
        if en_text in existing_msgids:
            entry = existing_msgids[en_text]
            entry.msgstr = uz_text
            if 'fuzzy' in entry.flags:
                entry.flags.remove('fuzzy')
        else:
            entry = polib.POEntry(
                msgid=en_text,
                msgstr=uz_text,
                occurrences=[('django/contrib/admin', '0')]
            )
            po.append(entry)
            
    po.save()
    print("Admin translations successfully added/updated for uz locale!")
except Exception as e:
    print(f"Error: {e}")
