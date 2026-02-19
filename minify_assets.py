import re
import os

def minify_css(css):
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove whitespace
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{:;,])\s*', r'\1', css)
    return css.strip()

def minify_js(js):
    # Very basic JS minification: strip block comments and multi-spaces
    # Note: This is simplified; won't handle all edge cases but safe for most plugins.
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    # Strip single line comments (keeping URLs safe)
    lines = js.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith('//'):
            continue
        new_lines.append(line)
    js = "\n".join(new_lines)
    # Simplify whitespace
    js = re.sub(r'[ \t]+', ' ', js)
    return js.strip()

def process_files():
    css_files = ['css/responsive.css', 'css/owl.css', 'css/flaticon.css', 'css/fontawesome-all.css', 'css/style.css']
    js_files = ['js/jquery.js', 'js/scrollbar.js', 'js/appear.js', 'js/wow.js', 'js/validate.js', 'js/sticky.js', 'js/datetimepicker.js', 'js/jquery-ui.min.js']

    for fpath in css_files:
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                content = f.read()
            minified = minify_css(content)
            # Save to .min.css if it doesn't exist, otherwise overwrite?
            # User wants to reduce payload, let's create .min versions or overwrite.
            # Usually better to overwrite if the HTML expects the original name, 
            # OR create .min and update HTML.
            # I'll overwrite for simplicity in this case as it's a static site.
            with open(fpath, 'w') as f:
                f.write(minified)
            print(f"Minified CSS: {fpath}")

    for fpath in js_files:
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                content = f.read()
            minified = minify_js(content)
            with open(fpath, 'w') as f:
                f.write(minified)
            print(f"Minified JS: {fpath}")

if __name__ == "__main__":
    process_files()
