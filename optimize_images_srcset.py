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
            
        # resolve path
        dir_path = os.path.dirname(filepath)
        img_path_on_disk = os.path.abspath(os.path.join(dir_path, src))
        
        if not os.path.exists(img_path_on_disk):
            continue

        # Check for automatic recompression if size > 50KB
        file_size = os.path.getsize(img_path_on_disk)
        if file_size > 50 * 1024 and not src.endswith('-mobile.webp') and '-700w.webp' not in src:
            # Only recompress once per session (check if we already recorded this image)
            recompress_image(img_path_on_disk, quality=60)

        # skip if it's already a mobile or intermediate image
        if '-mobile.' in src or '-700w.' in src:
            continue
            
        try:
            with Image.open(img_path_on_disk) as img:
                width, height = img.size
                
                # Cleanup existing srcset/sizes to avoid duplication
                clean_img_tag = re.sub(r'\s+srcset=["\'][^"\']*["\']', '', img_tag)
                clean_img_tag = re.sub(r'\s+sizes=["\'][^"\']*["\']', '', clean_img_tag)
                
                # We only create responsive sources if width >= 500
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
                        mobile_img.save(mobile_path_on_disk, 'WEBP', quality=65)

                    # Intermediate desktop width for ~686px display (often cited in Lighthouse)
                    mid_w = 700
                    if width >= 750: # Use 750 so we don't upscale too much if width=800
                        mid_h = int(height * (700 / width))
                        mid_src = f"{base}-700w.webp"
                        mid_path_on_disk = os.path.join(dir_path, mid_src)
                        
                        if not os.path.exists(mid_path_on_disk):
                            print(f"  Creating {mid_src} from {src}")
                            mid_img = img.resize((mid_w, mid_h), Image.Resampling.LANCZOS)
                            mid_img.save(mid_path_on_disk, 'WEBP', quality=60)
                        
                        srcset_str = f' srcset="{mobile_src} 412w, {mid_src} 700w, {src} {width}w" sizes="(max-width: 600px) 412px, (max-width: 1200px) 700px, {width}px"'
                    else:
                        srcset_str = f' srcset="{mobile_src} 412w, {src} {width}w" sizes="(max-width: 600px) 412px, {width}px"'
                    
                    if clean_img_tag.endswith('/>'):
                        new_img_tag = clean_img_tag[:-2] + srcset_str + ' />'
                    else:
                        new_img_tag = clean_img_tag[:-1] + srcset_str + '>'
                        
                    unique_tags[img_tag] = new_img_tag
        except Exception as e:
            print(f"  Error processing {img_path_on_disk}: {e}")

    # Replace all gathered tags
    for old_tag, new_tag in unique_tags.items():
        content = content.replace(old_tag, new_tag)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Specific re-compression of large background/hero images
processed_images = set()

def recompress_image(filepath, quality=55):
    if filepath in processed_images:
        return
        
    if os.path.exists(filepath):
        print(f"Recompressing {filepath} (quality={quality})")
        try:
            with Image.open(filepath) as img:
                img.save(filepath, 'WEBP', quality=quality)
            processed_images.add(filepath)
        except Exception as e:
            print(f"  Error recompressing {filepath}: {e}")

base_dir = '/Users/meetshah/Downloads/public_html 2'

# Recompress specific large files flagged in the research
high_impact_images = [
    'images/s46.webp',
    'images/s57.webp',
    'images/scuba9.webp',
    'images/scuba10.webp',
    'images/s56.webp',
    'images/s70.webp',
    'images/scuba13.webp',
    'images/Andaman/havelock-island-andamans-_73_11zon.webp',
    'images/goa-tour/Parasailing_in_Prasonisi._Rhodes,_Greece_71_11zon.webp',
    'images/goa-tour/4680252_15_11zon.webp',
    'images/watersports monsoon.webp'
]

for img_rel_path in high_impact_images:
    recompress_image(os.path.join(base_dir, img_rel_path), quality=55)

for root_dir, dirs, files in os.walk(base_dir):
    # skip temp or .git
    if 'temp' in root_dir or '.git' in root_dir:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root_dir, file)
            process_html_file(filepath)
            
print("Done optimizing images and adding srcset.")
