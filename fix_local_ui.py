import os
import re

base_dir = '/Users/meetshah/Downloads/public_html 2'

def patch_js_files():
    js_files = ['js/custom-script.js', 'js/custom-script.min.js']
    for js_file in js_files:
        filepath = os.path.join(base_dir, js_file)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Patch handlePreloader block
            # Originally:
            # function handlePreloader() {
            #   if ($('.preloader').length) {
            #     $('body').addClass('page-loaded');

            # We need to extract the addClass and put it before the if.
            
            patched_content = re.sub(
                r'function handlePreloader\(\)\s*\{\s*if\s*\(\$\(\'\.preloader\'\)\.length\)\s*\{\s*\$\(\'body\'\)\.addClass\(\'page-loaded\'\);',
                r'function handlePreloader() {\n\t\t\t$(\'body\').addClass(\'page-loaded\');\n\t\tif ($(\'.preloader\').length) {',
                content
            )

            if patched_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(patched_content)
                print(f"Patched strictly: {js_file}")
            else:
                # Let's try a softer patch just in case it was already modified or minified differently
                softer_patch = re.sub(
                    r'function handlePreloader\(\)\s*\{',
                    r'function handlePreloader() { $(\'body\').addClass(\'page-loaded\');',
                    content
                )
                if softer_patch != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(softer_patch)
                    print(f"Patched softly: {js_file}")

def patch_html_files():
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content

                # 1. Remove crossorigin="anonymous" from font preloads to bypass local file CORS
                content = re.sub(
                    r'<link\s+rel="preload"\s+href="(fonts/[^"]+)"\s+as="font"\s+type="font/woff2"\s+crossorigin="anonymous"\s*/?>',
                    r'<link rel="preload" href="\1" as="font" type="font/woff2">',
                    content
                )

                # 2. Add protocol check to sw.js registration
                content = content.replace(
                    "if ('serviceWorker' in navigator) { window.addEventListener('load', function() { navigator.serviceWorker.register",
                    "if ('serviceWorker' in navigator && window.location.protocol !== 'file:') { window.addEventListener('load', function() { navigator.serviceWorker.register"
                )

                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Patched HTML: {file}")

if __name__ == '__main__':
    patch_js_files()
    patch_html_files()
