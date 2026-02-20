import os
import re

file_path = r'm:/my projects/ACADEMIC OS/academic_os/hr/templates/hr/certificate_print.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix {% tags %}
def fix_django_tag(match):
    inner = match.group(1).replace('\n', ' ')
    inner = re.sub(r'\s+', ' ', inner)
    return '{%' + inner + '%}'

# Fix {{ variables }}
def fix_django_var(match):
    inner = match.group(1).replace('\n', ' ')
    inner = re.sub(r'\s+', ' ', inner)
    return '{{' + inner + '}}'

content = re.sub(r'\{%([^%]+)%\}', fix_django_tag, content)
content = re.sub(r'\{\{([^}]+)\}\}', fix_django_var, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template tags fixed via regex script.")
