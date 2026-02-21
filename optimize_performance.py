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
    
    # remove any existing preload for these images so we don't duplicate old urls
    for h in hero_images:
        # look for any preload referencing the src or srcset urls
        for src in re.findall(r'src=["\']([^"\']+)["\']', h):
            content = re.sub(r'<link[^>]+href=["\']' + re.escape(src) + r'["\'][^>]*>', '', content)
        for part in re.findall(r'srcset=["\']([^"\']+)["\']', h):
            for url in [p.strip().split(' ')[0] for p in part.split(',')]:
                content = re.sub(r'<link[^>]+href=["\']' + re.escape(url) + r'["\'][^>]*>', '', content)

    preloads = []
    for hero_img_tag in hero_images:
        # Extract src and any srcset width hints
        src_match = re.search(r'src=["\']([^"\']+)["\']', hero_img_tag)
        srcset_match = re.search(r'srcset=["\']([^"\']+)["\']', hero_img_tag)
        chosen_preload = None
        if srcset_match:
            # prefer the 700‑w version if present, otherwise fall back to the first
            parts = [p.strip() for p in srcset_match.group(1).split(',')]
            for part in parts:
                if '700w' in part:
                    chosen_preload = part.split(' ')[0]
                    break
            if not chosen_preload and parts:
                # use first width (usually mobile)
                chosen_preload = parts[0].split(' ')[0]
            # don't bother with the "original" if it's larger than 800px
        if not chosen_preload and src_match:
            chosen_preload = src_match.group(1)
        if chosen_preload:
            preload_tag = f'<link rel="preload" href="{chosen_preload}" as="image" fetchpriority="high">'
            if preload_tag not in content:
                preloads.append(preload_tag)
        
        # Update the tag itself: ensure eager loading and fetchpriority="high"
        if src_match:
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
    # prefetch the main icon/font files we need.  adding brands/regular ensures the
    # page doesn't wait for a subset of the FontAwesome family to arrive later.
    core_fonts = [
        "fonts/fa-solid-900.woff2",
        "fonts/fa-regular-400.woff2",
        "fonts/fa-brands-400.woff2",
        "fonts/Flaticon.woff2",
    ]
    font_preloads = []
    for font in core_fonts:
        font_tag = f'<link rel="preload" href="{font}" as="font" type="font/woff2" crossorigin>'
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
