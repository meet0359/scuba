import os
import re

base_dir = '/Users/meetshah/Downloads/public_html 2'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # Match <!-- Preloader --> block and the actual div
        # <div class="preloader">
        #   <div class="icon"></div>
        # </div>
        # We can just remove the whole div block.
        preloader_regex = re.compile(r'<!--\s*Preloader\s*-->\s*<div class="preloader">\s*<div class="icon"></div>\s*</div>', re.IGNORECASE)
        content = preloader_regex.sub('', content)

        # In case the format is slightly different
        preloader_regex_2 = re.compile(r'<!--\s*Preloader\s*-->\s*<div class="preloader">\s*</div>', re.IGNORECASE)
        content = preloader_regex_2.sub('', content)
        
        # or inline
        preloader_regex_3 = re.compile(r'<!--\s*Preloader\s*-->\s*<div class="preloader"><div class="icon"></div></div>', re.IGNORECASE)
        content = preloader_regex_3.sub('', content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Removed preloader from {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))
