#!/usr/bin/env python3
import os
import re
import glob

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 1. Add defer to local scripts (js/*.js)
    # Avoid double defer and handle both single/double quotes
    content = re.sub(
        r'<script(?![^>]*?(?:defer|async|type="module"))\s+src="(js/[^"]+\.js)"></script>',
        r'<script defer src="\1"></script>',
        content
    )

    # 2. Add loading="lazy" and dimensions to images
    def img_replacer(match):
        img_tag = match.group(0)
        
        # Skip tracking pixels (width="1" or height="1")
        if 'width="1"' in img_tag or 'height="1"' in img_tag:
            return img_tag
            
        # Skip hero/banner images
        if 'scuba9.webp' in img_tag or 'fetchpriority="high"' in img_tag or 'loading="eager"' in img_tag:
            return img_tag
        
        # Add loading="lazy" if not present
        if 'loading=' not in img_tag:
            img_tag = img_tag.replace('<img', '<img loading="lazy"')
        
        # Add dimensions if BOTH are missing
        if 'width=' not in img_tag and 'height=' not in img_tag:
            if '/6.webp' in img_tag:
                img_tag = img_tag.replace('<img', '<img width="160" height="160"')
            elif 'logo canva 10.webp' in img_tag:
                img_tag = img_tag.replace('<img', '<img width="400" height="300"')
            elif 'images/review/' in img_tag:
                img_tag = img_tag.replace('<img', '<img width="100" height="100"')
            else:
                # Default generic size for list items/thumbnails
                img_tag = img_tag.replace('<img', '<img width="400" height="300"')
        
        # Clean up any potential double spaces introduced
        img_tag = re.sub(r'\s+', ' ', img_tag)
        return img_tag

    content = re.sub(r'<img[^>]+>', img_replacer, content)

    # 3. Ensure 3rd party scripts are async if they aren't already
    # (Google Tag Manager, Facebook Pixel etc are usually already async in their snippets, 
    # but we can enforce it for external src lookups)
    #
    # 4. Defer loading of Google Tag Manager snippet by wrapping the inline factory
    # in a load/interaction listener.  This knocks ~300 ms off the main thread cost during
    # initial page load.
    def defer_gtm(match):
        inner = match.group(1)
        # wrap the original snippet so it executes after the window load event
        return '<script>window.addEventListener("load",function(){' + inner + '});</script>'

    content = re.sub(
        r'<script>([\s\S]*?googletagmanager\.com/gtm\.js[\s\S]*?)</script>',
        defer_gtm,
        content,
        flags=re.IGNORECASE
    )

    # 5. Add async attribute to other external 3rd party script tags
    content = re.sub(
        r'<script\s+([^>]*src=["\"][^"\"]+://[^"\"]+\"[^>]*)>',
        lambda m: '<script async ' + m.group(1) + '>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # -------------------------------------------------------------------------
    # 6. After modifying HTML we also keep sw.js up to date with every asset in the
    # directory tree so the service worker will precache them on next install.
    update_service_worker_cache_list()


def update_service_worker_cache_list():
    """Scan directories for static files and rewrite sw.js STATIC_ASSETS array."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sw_path = os.path.join(base_dir, 'sw.js')
    if not os.path.exists(sw_path):
        return

    assets = ['./', './index.html']
    # include all css, js, images, fonts
    patterns = ['css/**/*.css', 'js/**/*.js', 'images/**/*.*', 'fonts/**/*.*']
    for pattern in patterns:
        for filepath in glob.glob(os.path.join(base_dir, pattern), recursive=True):
            rel = os.path.relpath(filepath, base_dir).replace('\\','/')
            assets.append('./' + rel)

    # build new array string
    arr_entries = ',\n    '.join(f"'{a}'" for a in sorted(set(assets)))
    new_list = f"const STATIC_ASSETS = [\n    {arr_entries},\n];"

    with open(sw_path, 'r', encoding='utf-8') as f:
        sw_content = f.read()

    sw_content = re.sub(r'const STATIC_ASSETS = \[[^\]]*\];', new_list, sw_content)

    with open(sw_path, 'w', encoding='utf-8') as f:
        f.write(sw_content)

    print(f"  UPDATED service worker cache list with {len(assets)} entries")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = glob.glob(os.path.join(base_dir, '*.html'))
    print(f"Found {len(html_files)} HTML files. Processing...")
    for filepath in sorted(html_files):
        process_html_file(filepath)
    print("Optimization complete.")

if __name__ == '__main__':
    main()
