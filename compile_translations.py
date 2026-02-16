import os
import struct
import sys

def msgfmt(input_file, output_file):
    """
    Compiles a .po file to a .mo file.
    Adapted from Python's Tools/i18n/msgfmt.py
    Auto-fills empty msgstr with msgid.
    """
    print(f"Compiling {input_file} -> {output_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    ID = 1
    STR = 2

    strings = {}
    id = str_val = ''
    state = 0

    # Parse and fill
    for l in lines:
        if l[:1] == '#':
            continue
        l = l.strip()
        if not l:
            if state == STR:
                # If translation is empty, use ID
                if str_val == '':
                    str_val = id
                strings[id] = str_val
                id = str_val = ''
                state = 0
            continue
            
        if l[:6] == 'msgid ':
            l = l[6:]
            state = ID
        elif l[:7] == 'msgstr ':
            l = l[7:]
            state = STR
        
        if l[:1] == '"':
            l = l[1:-1]
            l = l.replace('\\n', '\n').replace('\\"', '"')
        
        if state == ID:
            id += l
        elif state == STR:
            str_val += l

    if state == STR:
        if str_val == '':
            str_val = id
        strings[id] = str_val

    # Generate .mo
    keys = sorted(strings.keys())
    
    K = len(keys)
    
    # We build the data buffers
    ids_data = b''
    strs_data = b''
    
    ids_offsets = []
    strs_offsets = []
    
    for k in keys:
        v = strings[k]
        k_enc = k.encode('utf-8')
        v_enc = v.encode('utf-8')
        
        ids_offsets.append((len(k_enc), len(ids_data)))
        ids_data += k_enc + b'\0'
        
        strs_offsets.append((len(v_enc), len(strs_data)))
        strs_data += v_enc + b'\0'
        
    O_start = 28
    T_start = O_start + (K * 8)
    IDs_start = T_start + (K * 8)
    STRs_start = IDs_start + len(ids_data)
    
    output = bytearray()
    output.extend(struct.pack('<I', 0x950412de))
    output.extend(struct.pack('<I', 0))
    output.extend(struct.pack('<I', K))
    output.extend(struct.pack('<I', O_start))
    output.extend(struct.pack('<I', T_start))
    output.extend(struct.pack('<I', 0))
    output.extend(struct.pack('<I', 0))
    
    for length, offset in ids_offsets:
        output.extend(struct.pack('<II', length, IDs_start + offset))
        
    for length, offset in strs_offsets:
        output.extend(struct.pack('<II', length, STRs_start + offset))
        
    output.extend(ids_data)
    output.extend(strs_data)
    
    with open(output_file, 'wb') as f:
        f.write(output)

def main():
    base_dir = 'locale'
    # Ensure locale director exists
    if not os.path.exists(base_dir):
        print("Locale directory not found.")
        return

    for lang in ['uz', 'ru', 'en']:
        po_file = os.path.join(base_dir, lang, 'LC_MESSAGES', 'django.po')
        mo_file = os.path.join(base_dir, lang, 'LC_MESSAGES', 'django.mo')
        
        if os.path.exists(po_file):
            try:
                msgfmt(po_file, mo_file)
                print(f"✅ Compiled {lang}")
            except Exception as e:
                print(f"❌ Error compiling {lang}: {e}")
        else:
            print(f"⚠️ {po_file} not found")

if __name__ == '__main__':
    main()
