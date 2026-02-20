import os
import re
from PIL import Image

def process_html_file(filepath):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <img ...> tags
    img_pattern = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
    
    unique_tags = {}
    
    for match in img_pattern.finditer(content):
        img_tag = match.group(0)
        src = match.group(1)
        
        # skip external images
        if src.startswith('http') or src.startswith('//') or src.startswith('data:'):
            continue
            
        # skip if already has srcset
        if 'srcset=' in img_tag.lower():
            continue
            
        # skip if it's already a mobile image
        if '-mobile.' in src:
            continue
            
        # resolve path
        dir_path = os.path.dirname(filepath)
        img_path_on_disk = os.path.join(dir_path, src)
        
        if not os.path.exists(img_path_on_disk):
            continue
            
        try:
            with Image.open(img_path_on_disk) as img:
                width, height = img.size
                
                # We only create mobile source if width >= 500
                if width >= 500:
                    base, ext = os.path.splitext(src)
                    
                    # Target mobile width
                    mobile_w = 412
                    mobile_h = int(height * (412 / width))
                    
                    # Create mobile image name
                    mobile_src = f"{base}-mobile.webp"
                    mobile_path_on_disk = os.path.join(dir_path, mobile_src)
                    
                    if not os.path.exists(mobile_path_on_disk):
                        print(f"  Creating {mobile_src} from {src}")
                        # Resize and save
                        mobile_img = img.resize((mobile_w, mobile_h), Image.Resampling.LANCZOS)
                        mobile_img.save(mobile_path_on_disk, 'WEBP', quality=80)
                    
                    srcset_str = f' srcset="{mobile_src} 412w, {src} {width}w" sizes="(max-width: 600px) 412px, {width}px"'
                    
                    if img_tag.endswith('/>'):
                        new_img_tag = img_tag[:-2] + srcset_str + ' />'
                    else:
                        new_img_tag = img_tag[:-1] + srcset_str + '>'
                        
                    unique_tags[img_tag] = new_img_tag
        except Exception as e:
            print(f"  Error processing {img_path_on_disk}: {e}")

    # Replace all gathered tags
    for old_tag, new_tag in unique_tags.items():
        content = content.replace(old_tag, new_tag)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Specific re-compression of large background/hero images
def recompress_image(filepath, quality=60):
    if os.path.exists(filepath):
        print(f"Recompressing {filepath}")
        try:
            with Image.open(filepath) as img:
                img.save(filepath, 'WEBP', quality=quality)
        except Exception as e:
            print(f"  Error recompressing {filepath}: {e}")

base_dir = '/Users/meetshah/Downloads/public_html 2'

# Recompress specific large files flagged in Lighthouse
recompress_image(os.path.join(base_dir, 'images/s46.webp'))
recompress_image(os.path.join(base_dir, 'images/scuba9.webp'), quality=65)

for root_dir, dirs, files in os.walk(base_dir):
    # skip temp or .git
    if 'temp' in root_dir or '.git' in root_dir:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root_dir, file)
            process_html_file(filepath)
            
print("Done optimizing images and adding srcset.")
