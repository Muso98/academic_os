import re
import os

file_path = 'academic_os/templates/dashboard.html'
if not os.path.exists(file_path):
    file_path = 'templates/dashboard.html'

print(f"Reading {file_path}...")

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: Find {{ ... }} tags that span multiple lines
# We capture {{ then anything until }} but across lines
def collapse_var(match):
    full_tag = match.group(0)
    if '\n' in full_tag:
        # Replace newlines and multiple spaces with a single space
        clean_tag = re.sub(r'\s+', ' ', full_tag).strip()
        print(f"Fixed variable: {clean_tag}")
        return clean_tag
    return full_tag

# Regex for {{ ... }} allowing newlines
content = re.sub(r'{{\s*[^}]+\s*}}', collapse_var, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully fixed variable tags in {file_path}")
