import os
import re

def fix_sw():
    sw_path = '/Users/meetshah/Downloads/public_html 2/sw.js'
    if os.path.exists(sw_path):
        with open(sw_path, 'r') as f:
            content = f.read()

        # Update catch block in sw.js
        content = re.sub(
            r'throw error;', 
            r"return new Response('', { status: 408, statusText: 'Request timed out or blocked.' });", 
            content
        )

        with open(sw_path, 'w') as f:
            f.write(content)
        print("Updated sw.js")

def fix_html_files():
    base_dir = '/Users/meetshah/Downloads/public_html 2'
    html_files = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    meta_regex = re.compile(r'<\s*meta\s+http-equiv\s*=\s*[\'"]X-Frame-Options[\'"].*?>', re.IGNORECASE)

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            
            # 1. Remove X-Frame-Options meta tag
            content = meta_regex.sub('<!-- X-Frame-Options removed by optimization script -->', content)

            # 2. Fix spaces in the logo URL in srcset and src
            content = content.replace('logo canva 10.webp', 'logo%20canva%2010.webp')
            content = content.replace('logo canva 10-mobile.webp', 'logo%20canva%2010-mobile.webp')
            
            # Also handle icon paths just in case
            content = content.replace('logo icon.webp', 'logo%20icon.webp')

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {os.path.basename(filepath)}")
                
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

if __name__ == '__main__':
    fix_sw()
    fix_html_files()
