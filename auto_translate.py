import polib
from deep_translator import GoogleTranslator
import time

def auto_translate_po(lang_code, po_file_path):
    print(f"Translating {lang_code}...")
    try:
        po = polib.pofile(po_file_path)
    except Exception as e:
        print(f"Could not load {po_file_path}: {e}")
        return

    translator = GoogleTranslator(source='auto', target=lang_code)
    changed = False
    
    for entry in po:
        if not entry.msgstr and not entry.obsolete:
            # Skip python formatting strings, we will handle them manually if needed
            if '%' in entry.msgid:
                print(f"Skipping format string: {entry.msgid}")
                continue
                
            try:
                translated = translator.translate(entry.msgid)
                if translated:
                    entry.msgstr = translated
                    changed = True
                    print(f"[{lang_code}] {entry.msgid} -> {translated}")
                time.sleep(0.5) # Prevent rate limiting
            except Exception as e:
                print(f"Failed to translate '{entry.msgid}': {e}")
                
    if changed:
        po.save()
        print(f"Saved {po_file_path}")

auto_translate_po('uz', 'locale/uz/LC_MESSAGES/django.po')
auto_translate_po('ru', 'locale/ru/LC_MESSAGES/django.po')
auto_translate_po('en', 'locale/en/LC_MESSAGES/django.po')
