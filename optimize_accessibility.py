#!/usr/bin/env python3
import os
import re
import glob

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 1. Add <main id="main-content"> right after header
    if '<main' not in content:
        # Match the end of the main header or page banner
        # Usually </header> or similar
        content = re.sub(
            r'(</header>|<!-- End Main Header -->)',
            r'\1\n\n    <main id="main-content">',
            content,
            count=1
        )
        # Close </main> before footer
        content = re.sub(
            r'(<footer|<!-- Main Footer -->)',
            r'    </main>\n\n\1',
            content,
            count=1
        )

    # 2. Add aria-labels to social links
    # Standard pattern: <a href="#"><span class="fab fa-facebook-f"></span></a>
    content = re.sub(
        r'<a href="#"(?![^>]*?aria-label)><span class="fab fa-facebook-f"></span></a>',
        r'<a href="#" aria-label="Facebook"><span class="fab fa-facebook-f"></span></a>',
        content
    )
    content = re.sub(
        r'<a href="#"(?![^>]*?aria-label)><span class="fab fa-twitter"></span></a>',
        r'<a href="#" aria-label="Twitter"><span class="fab fa-twitter"></span></a>',
        content
    )
    content = re.sub(
        r'<a href="#"(?![^>]*?aria-label)><span class="fab fa-linkedin-in"></span></a>',
        r'<a href="#" aria-label="LinkedIn"><span class="fab fa-linkedin-in"></span></a>',
        content
    )

    # 3. Add aria-label to mobile nav toggler
    content = re.sub(
        r'<div class="mobile-nav-toggler"(?![^>]*?aria-label)>',
        r'<div class="mobile-nav-toggler" aria-label="Toggle Navigation" role="button" tabindex="0">',
        content
    )

    # 4. Add aria-label to scroll-to-top
    content = re.sub(
        r'<div class="scroll-to-top scroll-to-target"(?![^>]*?aria-label)',
        r'<div class="scroll-to-top scroll-to-target" aria-label="Scroll to top"',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ACCESSIBILITY FIXED: {os.path.basename(filepath)}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = glob.glob(os.path.join(base_dir, '*.html'))
    for filepath in sorted(html_files):
        # Skip sitemap and other non-page files if needed
        if 'google' in filepath or 'm3xrpk' in filepath:
            continue
        process_html_file(filepath)

if __name__ == '__main__':
    main()
