import os
import re

replacements = {
    "Kasallik Varaqasi Yuborish": '{% trans "Kasallik varaqasi yuborish" %}',
    "Kasallik Varaqalari — HR Ko'rinishi": '{% trans "Kasallik varaqalari — HR ko\'rinishi" %}',
    "HR: Kasallik Varaqalari": '{% trans "HR: Kasallik varaqalari" %}',
    "Kasallik Varaqasini Ko'rib Chiqish": '{% trans "Kasallik varaqasini ko\'rib chiqish" %}',
    "Mening Kasallik Varaqlariim": '{% trans "Mening kasallik varaqlariim" %}',
    "Kasallik varaqlariim": '{% trans "Kasallik varaqlariim" %}',
    "Xodimlar Boshqaruvi": '{% trans "Xodimlar boshqaruvi" %}',
    "Xodimlarni Boshqarish": '{% trans "Xodimlarni boshqarish" %}'
}

template_dirs = []
for root, dirs, files in os.walk('d:/Projects for clients/academic_os'):
    if 'venv' in root or '.git' in root:
        continue
    if 'templates' in root:
        template_dirs.append(root)

for d in template_dirs:
    for f in os.listdir(d):
        if f.endswith('.html'):
            filepath = os.path.join(d, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            new_content = content
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)
                
            if content != new_content:
                # Make sure {% load i18n %} is at the top if we added {% trans %}
                if '{% trans' in new_content and '{% load i18n %}' not in new_content:
                    if '{% extends' in new_content:
                        # Insert after extends
                        lines = new_content.split('\n')
                        for i, line in enumerate(lines):
                            if '{% extends' in line:
                                lines.insert(i+1, '{% load i18n %}')
                                break
                        new_content = '\n'.join(lines)
                    else:
                        new_content = '{% load i18n %}\n' + new_content

                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated {filepath}")
