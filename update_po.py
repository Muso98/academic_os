import polib
import re

def sentence_case(text):
    if not text: return text
    words = text.split(' ')
    if len(words) <= 1: return text
    
    res = [words[0]]
    for w in words[1:]:
        # Preserve fully uppercase words like KPI, PDF, ID, HR
        # and words that contain HTML tags or formatting like <br>, %(num)s
        if w.isupper() or '<' in w or '>' in w or '%' in w:
            res.append(w)
        else:
            res.append(w.lower())
    return ' '.join(res)

def process_po_file(filepath):
    try:
        po = polib.pofile(filepath)
        changed = False
        for entry in po:
            original = entry.msgstr
            if not original:
                continue
                
            new_text = sentence_case(original)
            
            # Special case for Django Admin words if any
            if original != new_text:
                entry.msgstr = new_text
                changed = True
                
        if changed:
            po.save()
            print(f"Saved {filepath}")
        else:
            print(f"No changes in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

process_po_file('locale/uz/LC_MESSAGES/django.po')
process_po_file('locale/ru/LC_MESSAGES/django.po')
