import os

def append_to_css(filepath, new_css):
    if os.path.exists(filepath):
        with open(filepath, 'a') as f:
            f.write('\n' + new_css + '\n')
            print(f"Appended to {filepath}")
    else:
        print(f"File not found: {filepath}")

if __name__ == '__main__':
    css_to_add = ".nav-content { min-height: 60px; }"
    append_to_css('/Users/meetshah/Downloads/public_html 2/css/style.css', css_to_add)
    append_to_css('/Users/meetshah/Downloads/public_html 2/css/style.min.css', css_to_add)
