import os

path = 'locale/ru/LC_MESSAGES/django.po'
with open(path, 'rb') as f:
    data = f.read()

# PowerShell Add-Content often adds \r\n before the new content.
# And checks for BOM.
bom = b'\xff\xfe'
if bom in data:
    print("Found BOM, fixing...")
    parts = data.split(bom)
    # parts[0] is the original utf-8 content (plus maybe \r\n)
    # parts[1] is the utf-16-le content
    
    clean_header = parts[0]
    
    try:
        # Decode the appended part
        # PowerShell might have added newlines before BOM, identifying where it starts
        new_content = parts[1].decode('utf-16-le')
        print(f"Recovered content: {new_content}")
        
        # Re-encode as utf-8
        new_bytes = new_content.encode('utf-8')
        
        final_data = clean_header + new_bytes
        
        with open(path, 'wb') as f:
            f.write(final_data)
        print("File fixed.")
    except Exception as e:
        print(f"Error decoding: {e}")
        # Fallback: just truncate to clean_header
        with open(path, 'wb') as f:
            f.write(clean_header)
        print("Truncated file to before corruption.")
else:
    print("No BOM found. Checking for other corruption...")
    # If no BOM, maybe it just appended garbage?
    # Try to decode as utf-8
    try:
        data.decode('utf-8')
        print("File is valid utf-8.")
    except UnicodeDecodeError:
        print("File is invalid utf-8. Truncating file to last valid byte?")
        # Using ignore might be better
        cleaned = data.decode('utf-8', 'ignore').encode('utf-8')
        with open(path, 'wb') as f:
            f.write(cleaned)
        print("Cleaned file using ignore.")
