import re

file_path = 'documents/templates/documents/report_list.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the specific split tag for admin_comment
# Looking for: Izoh: {{ report.admin_comment [newline] }}
# Regex to find {{ ... }} split across lines
pattern = r'\{\{\s*report\.admin_comment\s*\n\s*\}\}'
replacement = '{{ report.admin_comment }}'

new_content = re.sub(pattern, replacement, content)

# Also fix any other potentially split tags just in case
new_content = re.sub(r'\{\{\s*([a-zA-Z0-9_.]+)\s*\n\s*\}\}', r'{{\1}}', new_content)

if content != new_content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Fixed split template tags in report_list.html")
else:
    print("ℹ️ No split tags found or pattern didn't match.")
