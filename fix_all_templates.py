import os
import re

from pathlib import Path

BASE_DIR = Path('m:/my projects/ACADEMIC OS/academic_os')

def fix_django_tag(match):
    inner = match.group(1).replace('\n', ' ')
    inner = re.sub(r'\s+', ' ', inner)
    return '{%' + inner + '%}'

def fix_django_var(match):
    inner = match.group(1).replace('\n', ' ')
    inner = re.sub(r'\s+', ' ', inner)
    return '{{' + inner + '}}'

count = 0
for html_file in BASE_DIR.rglob('*.html'):
    if 'venv' in html_file.parts or '.venv' in html_file.parts:
         continue
         
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    content = re.sub(r'\{%([^%]+)%\}', fix_django_tag, content)
    content = re.sub(r'\{\{([^}]+)\}\}', fix_django_var, content)
    
    if original != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed formatting in {html_file.relative_to(BASE_DIR)}")
        count += 1

print(f"Done! Fixed {count} files.")
