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
    js_files = [
        ('js/jquery.js', 'js/jquery.js'),
        ('js/scrollbar.js', 'js/scrollbar.js'),
        ('js/appear.js', 'js/appear.js'),
        ('js/wow.js', 'js/wow.js'),
        ('js/validate.js', 'js/validate.js'),
        ('js/sticky.js', 'js/sticky.js'),
        ('js/datetimepicker.js', 'js/datetimepicker.js'),
        ('js/jquery-ui.min.js', 'js/jquery-ui.min.js'),
        ('js/custom-script.js', 'js/custom-script.min.js')
    ]

    for fpath in css_files:
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                content = f.read()
            minified = minify_css(content)
            with open(fpath, 'w') as f:
                f.write(minified)
            print(f"Minified CSS: {fpath}")

    for input_path, output_path in js_files:
        if os.path.exists(input_path):
            with open(input_path, 'r') as f:
                content = f.read()
            minified = minify_js(content)
            with open(output_path, 'w') as f:
                f.write(minified)
            print(f"Minified JS: {input_path} -> {output_path}")

if __name__ == "__main__":
    process_files()
