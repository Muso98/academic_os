import re
import os

file_path = 'academic_os/templates/dashboard.html'
# Handle relative path from project root
if not os.path.exists(file_path):
    file_path = 'templates/dashboard.html'

print(f"Reading {file_path}...")

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: Fix specific long string split
# {% trans "Here's what's happening in your academic
# workspace today." %}
content = re.sub(
    r'{%\s*trans\s+"Here\'s what\'s happening in your academic\s+workspace today\."\s*%}', 
    '{% trans "Here\'s what\'s happening in your academic workspace today." %}', 
    content
)

# Pattern 2: Fix tags where the closing %} is on a new line
# {% trans "All time"
# %}
content = re.sub(
    r'{%\s*trans\s+"([^"]+)"\s+%}', 
    r'{% trans "\1" %}', 
    content
)

# Pattern 3: Generic collapse of any multi-line {% trans ... %}
# This finds {% trans "..." %} that spans multiple lines and joins them
def collapse_tag(match):
    full_tag = match.group(0)
    if '\n' in full_tag:
        clean_tag = re.sub(r'\s+', ' ', full_tag).strip()
        print(f"Fixed: {clean_tag}")
        return clean_tag
    return full_tag

content = re.sub(r'{%\s*trans\s+"[^"]+"\s*%}', collapse_tag, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully fixed template tags in {file_path}")
