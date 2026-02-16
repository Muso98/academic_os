import re

with open('users/templates/users/profile.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Join lines and fix broken tags
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Fix broken small tag for date
    if 'Berilgan: {{ cert.date_issued' in line and i + 1 < len(lines):
        next_line = lines[i + 1]
        if '}}' in next_line:
            line = line.rstrip() + ' }}</small>\r\n'
            i += 2
            new_lines.append(line)
            continue
    
    # Fix broken small tag with class
    if line.strip() == '<small':
        if i + 1 < len(lines) and 'class="{%' in lines[i + 1]:
            line = '                                        <small class="{% if cert.is_expired %}text-danger{% else %}text-success{% endif %} d-block">\r\n'
            i += 2
            new_lines.append(line)
            continue
    
    # Fix broken endif
    if '{% if cert.is_expired %}<i class="bi bi-exclamation-circle ms-1"></i>{%' in line:
        if i + 1 < len(lines) and 'endif %}' in lines[i + 1]:
            line = line.replace('{%\r\n', '{% endif %}\r\n').replace('{%\n', '{% endif %}\n')
            i += 2
            new_lines.append(line)
            continue
    
    new_lines.append(line)
    i += 1

# Write back
with open('users/templates/users/profile.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ Template fixed successfully!')
