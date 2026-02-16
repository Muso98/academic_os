import os
import re

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')
LANGUAGES = ['uz', 'ru', 'en']

def get_trans_strings(base_dir):
    """
    Scans all .html files in the project and extracts strings inside {% trans "..." %} tags.
    Returns a set of unique strings.
    """
    trans_strings = set()
    # Pattern to match {% trans "string" %} or {% trans 'string' %}
    # We handle both single and double quotes. 
    # capturing group 1 is the string content.
    pattern = re.compile(r'{%\s*trans\s+["\'](.*?)["\']\s*%}')
    
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = pattern.findall(content)
                        for match in matches:
                            trans_strings.add(match)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return trans_strings

def read_po_file(po_path):
    """
    Reads a .po file and returns a set of existing msgids.
    """
    existing_msgids = set()
    if not os.path.exists(po_path):
        return existing_msgids
    
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Simple regex to find msgid "..."
        # This is a basic parser and might not handle multiline msgids perfectly if they are not standard,
        # but for our simple script it should suffice.
        matches = re.findall(r'msgid\s+"(.*?)"', content)
        for match in matches:
            if match: # Ignore empty msgid "" used for header
                existing_msgids.add(match)
    return existing_msgids

def append_to_po(po_path, new_strings, existing_ids):
    """
    Appends new strings to the .po file.
    """
    if not new_strings:
        return
    
    with open(po_path, 'a', encoding='utf-8') as f:
        f.write('\n')
        for s in new_strings:
            # Escape quotes if necessary (basic)
            s_escaped = s.replace('"', '\\"')
            if s_escaped not in existing_ids:
                f.write(f'\nmsgid "{s_escaped}"\n')
                f.write('msgstr ""\n')
                print(f"Added: {s}")

def main():
    print("Scanning templates for translatable strings...")
    extracted_strings = get_trans_strings(BASE_DIR)
    print(f"Found {len(extracted_strings)} unique existing strings in templates.")

    for lang in LANGUAGES:
        po_file = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(po_file), exist_ok=True)
        
        # Create file if it doesn't exist
        if not os.path.exists(po_file):
             with open(po_file, 'w', encoding='utf-8') as f:
                f.write('msgid ""\n')
                f.write('msgstr ""\n')
                f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        
        print(f"Processing {lang}...")
        existing_ids = read_po_file(po_file)
        
        # Determine which strings are new
        # We need to be careful about escaping in our comparison
        # The extraction captures raw string, the po reader captures escaped string (kind of)
        # Actually, python's re.findall on msgid "..." captures the inner content.
        # If the file has msgid "O\"zbek", read_po_file returns O\"zbek.
        #Extracted string is O'zbek. Escaped is O\'zbek (if using single quotes) or O'zbek (if double).
        # Let's simple check: if the raw string isn't in the list of existing (unescaped)
        # This basic parser might be slightly off on complex escapes but should work for alphanumeric + simple punctuation.
        
        # Let's refine read_po_file to return unescaped strings for comparison?
        # No, let's just check if "string" is in the file content to be safe/lazy?
        # Better: just use the append logic with check.
        
        # Simpler approach for this script:
        # Just append unique checks.
        
        append_cnt = 0
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()

        with open(po_file, 'a', encoding='utf-8') as f:
            for s in extracted_strings:
                # Basic check if the string is already literally in the file
                # This prevents duplication even if my parser logic is weak
                # We check for: msgid "STRING"
                s_escaped = s.replace('"', '\\"')
                check_str = f'msgid "{s_escaped}"'
                
                if check_str not in content:
                    f.write(f'\nmsgid "{s_escaped}"\n')
                    f.write('msgstr ""\n')
                    append_cnt += 1
        
        print(f"Appended {append_cnt} new strings to {lang}.")

if __name__ == "__main__":
    main()
