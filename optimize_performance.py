#!/usr/bin/env python3
import os
import re
import glob

def process_html_file(filepath):
    print(f"Optimizing: {os.path.basename(filepath)}")
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original_content = content

    # 1. Identify LCP Image and Optimize (Hero Slider images)
    # Usually the first large image or banner-carousel image
    hero_images = re.findall(r'<(?:img|div)[^>]+(?:images/scuba9|images/main-slider/|banner-carousel)[^>]+>', content)
    
    preloads = []
    for hero_img_tag in hero_images:
        # Extract src
        src_match = re.search(r'src=["\']([^"\']+)["\']', hero_img_tag)
        if src_match:
            src = src_match.group(1)
            # Add preload to head if not already there
            preload_tag = f'<link rel="preload" href="{src}" as="image" fetchpriority="high">'
            if preload_tag not in content:
                preloads.append(preload_tag)
            
            # Update the tag itself: ensure eager loading and fetchpriority="high"
            new_tag = hero_img_tag
            if 'loading="lazy"' in new_tag:
                new_tag = new_tag.replace('loading="lazy"', 'loading="eager"')
            elif 'loading=' not in new_tag:
                new_tag = new_tag.replace('<img', '<img loading="eager"')
            
            if 'fetchpriority=' not in new_tag:
                new_tag = new_tag.replace('<img', '<img fetchpriority="high"')
            
            content = content.replace(hero_img_tag, new_tag)

    # 2. Inject preloads into <head>
    if preloads:
        preload_block = "\n  ".join(preloads)
        content = re.sub(r'(<head[^>]*>)', r'\1\n  ' + preload_block, content, count=1)

    # 3. Ensure critical font preloading
    core_fonts = ["fonts/fa-solid-900.woff2", "fonts/Flaticon.woff2"]
    font_preloads = []
    for font in core_fonts:
        font_tag = f'<link rel="preload" href="{font}" as="font" type="font/woff2" crossorigin>'
        # Check if already preloaded (might have variations in tags)
        if font not in content:
            font_preloads.append(font_tag)
    
    if font_preloads:
        font_block = "\n  ".join(font_preloads)
        content = re.sub(r'(<head[^>]*>)', r'\1\n  ' + font_block, content, count=1)

    # 4. Defer non-critical JS (move to end of body or add defer)
    # Already handled partly by other scripts, but let's be thorough
    def defer_script(match):
        tag = match.group(0)
        if 'defer' in tag or 'async' in tag or 'type="module"' in tag:
            return tag
        return tag.replace('<script', '<script defer')

    # Specifically target common heavy plugins
    content = re.sub(r'<script[^>]+src=["\']js/(?:owl|isotope|jquery-ui|fancybox|scrollbar)[^"\']+["\'][^>]*></script>', defer_script, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = glob.glob(os.path.join(base_dir, '*.html'))
    count = 0
    for filepath in sorted(html_files):
        if process_html_file(filepath):
            count += 1
    print(f"Finished! Optimized {count} HTML files.")

if __name__ == '__main__':
    main()
