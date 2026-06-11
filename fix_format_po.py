import polib

format_strings = {
    'uz': {
        '%(year)s-yil "%(day)s"-%(month)s <br> %(num)s-son': '%(year)s-yil "%(day)s"-%(month)s <br> %(num)s-son',
        '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(region)sdagi %(org_name)sning %(position)s vazifasida ishlaydi.\n                ': '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(region)sdagi %(org_name)sning %(position)s vazifasida ishlaydi.\n                ',
        '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(org_name)sning %(position)s vazifasida ishlaydi.\n                ': '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(org_name)sning %(position)s vazifasida ishlaydi.\n                ',
        '%(year)s-yil %(num)s-sonli ma\'lumotnoma': '%(year)s-yil %(num)s-sonli ma\'lumotnoma'
    },
    'ru': {
        '%(year)s-yil "%(day)s"-%(month)s <br> %(num)s-son': 'от "%(day)s" %(month)s %(year)s года <br> № %(num)s',
        '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(region)sdagi %(org_name)sning %(position)s vazifasida ishlaydi.\n                ': '\n                Дана настоящая справка в том, что <b>%(name)s</b> действительно работает в %(org_name)s (%(region)s) в должности %(position)s.\n                ',
        '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(org_name)sning %(position)s vazifasida ishlaydi.\n                ': '\n                Дана настоящая справка в том, что <b>%(name)s</b> действительно работает в %(org_name)s в должности %(position)s.\n                ',
        '%(year)s-yil %(num)s-sonli ma\'lumotnoma': 'Справка №%(num)s от %(year)s года'
    },
    'en': {
        '%(year)s-yil "%(day)s"-%(month)s <br> %(num)s-son': 'Date: %(month)s %(day)s, %(year)s <br> No. %(num)s',
        '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(region)sdagi %(org_name)sning %(position)s vazifasida ishlaydi.\n                ': '\n                This certificate confirms that <b>%(name)s</b> is employed at %(org_name)s in %(region)s as %(position)s.\n                ',
        '\n                Berildi ushbu ma\'lumotnoma shu haqdadirki, <b>%(name)s</b> haqiqatan ham %(org_name)sning %(position)s vazifasida ishlaydi.\n                ': '\n                This certificate confirms that <b>%(name)s</b> is employed at %(org_name)s as %(position)s.\n                ',
        '%(year)s-yil %(num)s-sonli ma\'lumotnoma': 'Certificate No. %(num)s of %(year)s'
    }
}

for lang in ['uz', 'ru', 'en']:
    po_path = f'locale/{lang}/LC_MESSAGES/django.po'
    po = polib.pofile(po_path)
    changed = False
    for entry in po:
        if entry.msgid in format_strings[lang]:
            entry.msgstr = format_strings[lang][entry.msgid]
            if 'fuzzy' in entry.flags:
                entry.flags.remove('fuzzy')
            changed = True
    if changed:
        po.save()
        print(f"Updated format strings for {lang}")
