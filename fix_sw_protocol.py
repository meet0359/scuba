import os
import re

base_dir = '/Users/meetshah/Downloads/public_html 2'

def patch_sw_registration():
    # This regex looks for the if('serviceWorker' in navigator) block and adds the protocol check.
    # It handles potential newlines and spaces.
    pattern = re.compile(r"if\s*\(\s*'serviceWorker'\s*in\s*navigator\s*\)\s*\{")
    replacement = "if ('serviceWorker' in navigator && window.location.protocol !== 'file:') {"

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if "window.location.protocol !== 'file:'" in content:
                        continue # Already patched
                    
                    new_content = pattern.sub(replacement, content)
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Patched ServiceWorker registration in {file}")
                except Exception as e:
                    print(f"Error patching {file}: {e}")

if __name__ == '__main__':
    patch_sw_registration()
