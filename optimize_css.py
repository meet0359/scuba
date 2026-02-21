#!/usr/bin/env python3
"""
Script to optimize CSS loading in HTML files by:
1. Adding Google Fonts preconnect + link tag (replacing the @import that was removed from style.min.css)
2. Deferring non-critical CSS with rel="preload" pattern
"""

import os
import re
import glob

# Critical CSS - keep as render-blocking
CRITICAL_CSS = [
    'bootstrap.min.css',
    'style.min.css',
    'responsive.css',
    'owl.css',
    'flaticon.css',
]

# Non-critical CSS to defer
NON_CRITICAL_CSS = [
    'fontawesome-all.css',
    'simple-line-icons.css',
    'themify-icons.css',
    'animate.css',
    'jquery-ui.css',
    'jquery.fancybox.min.css',
    'scrollbar.css',
    'datetimepicker.css',
    'hover.css',
    'custom-animate.css',
]

# Google Fonts URL
GOOGLE_FONTS_URL = "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700;1,900&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400&display=swap"

# Preload script to inject (once per page, before </body> or right after <body>)
PRELOAD_SCRIPT = """<script>
  // Load non-critical CSS asynchronously
  function loadCSS(href){
    var l=document.createElement('link');
    l.rel='stylesheet';l.href=href;
    document.head.appendChild(l);
  }
</script>"""

GOOGLE_FONTS_PRECONNECT = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{}" rel="preload" as="style" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link href="{}" rel="stylesheet" /></noscript>""".format(GOOGLE_FONTS_URL, GOOGLE_FONTS_URL)

def make_preload(href, is_cdn=False):
    """Convert a stylesheet link to preload pattern."""
    return (
        f'  <link rel="preload" href="{href}" as="style" onload="this.onload=null;this.rel=\'stylesheet\'" />\n'
        f'  <noscript><link rel="stylesheet" href="{href}" /></noscript>'
    )

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Skip if no CSS links found (probably not a page we need to optimize)
    if 'bootstrap.min.css' not in content and 'style.min.css' not in content:
        print(f"  SKIP (no relevant CSS): {os.path.basename(filepath)}")
        return False

    # 1. Remove the old prefetch for FA woff2 if present (it's already handled by fontawesome-all.css)
    content = re.sub(
        r'\s*<link href="https://www\.scubadivingadventure\.in/fonts/fa-brands-400\.woff2" rel="prefetch" />\n?',
        '\n',
        content
    )

    # 2. Add Google Fonts preconnect + preload right after <link href="css/style.min.css" ...>
    # but we want the font links to appear *before* other styles so the requests
    # begin as early as possible.  We'll also attempt to warm up the actual
    # woff2 files by fetching the CSS from Google and preloading each font URL.
    if 'fonts.googleapis.com' not in content:
        insertion = GOOGLE_FONTS_PRECONNECT

        # fetch the CSS to harvest font definitions and optionally inline them.
        inline_css = ''
        try:
            import urllib.request, ssl
            ctx = ssl.create_default_context()
            css_text = urllib.request.urlopen(GOOGLE_FONTS_URL, context=ctx, timeout=5).read().decode('utf-8')
            # we may not be able to preload woff2 URLs (Google often serves ttf),
            # but we can inline the whole stylesheet so the font requests start
            # as soon as the HTML parser reaches this block.
            inline_css = '<style>' + css_text + '</style>'
        except Exception:
            inline_css = ''

        # place the combined block before the first stylesheet link in head
        content = re.sub(
            r'(<link href="css/style\.min\.css" rel="stylesheet" />)',
            insertion + '\n' + inline_css + '\n\1',
            content
        )

    # 3. Convert non-critical local CSS to preload
    for css_file in NON_CRITICAL_CSS:
        # Match standard rel="stylesheet" links for this css file
        pattern = r'(\s*)<link href="css/{}" rel="stylesheet" />'.format(re.escape(css_file))
        replacement = '\n' + make_preload('css/' + css_file)
        content = re.sub(pattern, replacement, content)

    # 4. Convert CDN cookie consent CSS to preload
    cdn_pattern = r'(\s*)<link rel="stylesheet" type="text/css"\s+href="(https://cdn\.jsdelivr\.net/npm/cookieconsent@3/build/cookieconsent\.min\.css)" />'
    cdn_match = re.search(cdn_pattern, content)
    if cdn_match:
        cdn_url = cdn_match.group(2)
        content = re.sub(
            cdn_pattern,
            '\n' + make_preload(cdn_url, is_cdn=True),
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  UPDATED: {os.path.basename(filepath)}")
    return True

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = glob.glob(os.path.join(base_dir, '*.html'))
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        result = process_html_file(filepath)
        if result:
            updated += 1
        else:
            skipped += 1
    
    print(f"\nDone! Updated: {updated}, Skipped: {skipped}")

if __name__ == '__main__':
    main()
