import polib

for lang in ['ru', 'en']:
    po = polib.pofile(f'locale/{lang}/LC_MESSAGES/django.po')
    for entry in po:
        if 'Berildi ushbu' in entry.msgid:
            if 'fuzzy' in entry.flags:
                entry.flags.remove('fuzzy')
            if lang == 'ru':
                if 'region' in entry.msgid:
                    entry.msgstr = '\n                Дана настоящая справка в том, что <b>%(name)s</b> действительно работает в должности %(position)s в %(org_name)s (%(region)s).\n                '
                else:
                    entry.msgstr = '\n                Дана настоящая справка в том, что <b>%(name)s</b> действительно работает в должности %(position)s в %(org_name)s.\n                '
            elif lang == 'en':
                if 'region' in entry.msgid:
                    entry.msgstr = '\n                This certificate confirms that <b>%(name)s</b> is currently employed as %(position)s at %(org_name)s in %(region)s.\n                '
                else:
                    entry.msgstr = '\n                This certificate confirms that <b>%(name)s</b> is currently employed as %(position)s at %(org_name)s.\n                '
        
        if "MAKTABGACHA VA MAKTAB" in entry.msgid:
            if lang == 'en': entry.msgstr = 'DEPARTMENT OF PRESCHOOL AND PUBLIC EDUCATION'
        if "Manzil kiritilmagan" in entry.msgid:
            if lang == 'en': entry.msgstr = 'Address not specified'
        if "kiritilmagan" == entry.msgid:
            if lang == 'en': entry.msgstr = 'not specified'
        if "Tel:" in entry.msgid:
            if lang == 'en': entry.msgstr = 'Tel:'
        if "Murojaat uchun tel:" in entry.msgid:
            if lang == 'en': entry.msgstr = 'Contact Phone:'
            if lang == 'ru': entry.msgstr = 'Телефон для справок:'
        if "Asl nusxani tekshirish" in entry.msgid:
            if lang == 'en': entry.msgstr = 'Verify Authenticity (QR)'
        if "Tashkilot rahbari" in entry.msgid:
            if lang == 'en': entry.msgstr = 'Head of Organization:'
        if "MA'LUMOTNOMA" in entry.msgid:
            if lang == 'en': entry.msgstr = 'CERTIFICATE'
        if "taqdim etish uchun berildi" in entry.msgid:
            if lang == 'en': entry.msgstr = 'This certificate is issued to be presented at the requested place.'
    
    po.save()
