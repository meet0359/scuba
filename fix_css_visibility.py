import re

def fix_css_visibility(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Replace visibility inside @keyframes or transitions, except backface-visibility
        # We want to replace 'visibility: visible;' with 'opacity: 1;'
        # and 'visibility: hidden;' with 'opacity: 0;'
        # Be careful not to replace 'backface-visibility'

        # Look for 'visibility: visible' not preceded by 'backface-'
        content = re.sub(r'(?<!backface-)visibility:\s*visible\s*;', 'opacity: 1;', content)
        
        # Look for 'visibility: hidden' not preceded by 'backface-'
        content = re.sub(r'(?<!backface-)visibility:\s*hidden\s*;', 'opacity: 0;', content)

        with open(filepath, 'w') as f:
            f.write(content)
            
        print(f"Successfully processed {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    css_files = [
        "/Users/meetshah/Downloads/public_html 2/css/animate.css",
        "/Users/meetshah/Downloads/public_html 2/css/style.css",
        "/Users/meetshah/Downloads/public_html 2/css/style.min.css"
    ]
    for filename in css_files:
        fix_css_visibility(filename)
