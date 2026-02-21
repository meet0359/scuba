import os
import re

base_dir = '/Users/meetshah/Downloads/public_html 2'

PRELOADER_CSS_START = "    /* Preloader Styles Start */"
PRELOADER_CSS_END = "    /* Preloader Styles End */"

# Designed for a "small" look
PRELOADER_CSS_CONTENT = """
    .preloader {
      position: fixed;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      background: #ffffff;
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: opacity 0.5s ease-out, visibility 0.5s ease-out;
    }
    
    .preloader.loaded {
      opacity: 0;
      visibility: hidden;
    }

    .preloader .icon {
      width: 60px;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .infinity-path {
      fill: none;
      stroke: #ff4d4d;
      stroke-width: 4;
      stroke-dasharray: 250;
      stroke-dashoffset: 250;
      animation: dash 2.5s linear infinite;
    }

    @keyframes dash {
      to {
        stroke-dashoffset: 0;
      }
    }
"""

PRELOADER_CSS_BLOCK = f"{PRELOADER_CSS_START}{PRELOADER_CSS_CONTENT}{PRELOADER_CSS_END}"

PRELOADER_HTML = """<!-- Preloader -->
<div class="preloader">
  <div class="icon">
    <svg width="60" height="30" viewBox="0 0 100 50">
      <path class="infinity-path" d="M31.6,3.5C5.9,3.5,5.9,46.5,31.6,46.5c15.4,0,23.1-21.5,36.8-21.5c13.7,0,21.4,21.5,36.8,21.5c25.7,0,25.7-43,0-43 c-15.4,0-23.1,21.5-36.8,21.5C54.7,25,47,3.5,31.6,3.5z" />
    </svg>
  </div>
</div>"""

def remove_all_preloader_html(content):
    """Loop until ALL stacked preloader blocks are removed."""
    pattern = re.compile(
        r'\s*<!--\s*Preloader\s*-->\s*<div\s+class="preloader"[^>]*>.*?</div>\s*</div>',
        re.DOTALL | re.IGNORECASE
    )
    prev = None
    while prev != content:
        prev = content
        content = pattern.sub('', content)
    return content

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Remove ALL existing preloader HTML blocks (loops to handle stacked duplicates)
        content = remove_all_preloader_html(content)
        
        # 2. Cleanup existing preloader CSS blocks
        content = re.sub(r'\s*/\* Preloader Styles Start \*/.*?/\* Preloader Styles End \*/', '', content, flags=re.DOTALL)
        content = re.sub(r'\s*/\* Preloader Styles \*/.*?@keyframes (spin|dash|pulse) \{.*?\}', '', content, flags=re.DOTALL)
        
        # 3. Cleanup specific corrupted fragments and dangling brackets
        content = re.sub(r'\s*100% \{ transform: rotate\(360deg\); \}\s*\}', '', content)
        content = re.sub(r'\s*50% \{ transform: scale\(1\); opacity: 1; \}\s*100% \{ transform: scale\(0.9\); opacity: 0.7; \}\s*\}', '', content)
        content = re.sub(r'\s*@keyframes (dash|spin|pulse) \{.*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\s*\}\s*(?=</style>|\s*\* \{)', '', content)
        
        # 4. Clean up empty style tags
        content = re.sub(r'<style>\s*</style>', '', content)

        # 5. Inject CSS at the start of <head>
        head_match = re.search(r'<head>', content)
        if head_match:
            head_end = head_match.end()
            content = content[:head_end] + f"\n  <style>{PRELOADER_CSS_BLOCK}</style>" + content[head_end:]

        # 6. Inject HTML at the start of <body>
        body_match = re.search(r'<body[^>]*>', content)
        if body_match:
            body_end = body_match.end()
            content = content[:body_end] + f"\n  {PRELOADER_HTML}" + content[body_end:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))
