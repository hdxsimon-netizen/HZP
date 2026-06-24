"""Generate iOS app icon sizes from source image for Capacitor project."""
import os
import sys
import json
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(PROJECT_ROOT, 'app-icon.png')
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'ios', 'App', 'App', 'Assets.xcassets', 'AppIcon.appiconset')

# iOS icon sizes (idiom × scale × size in points → pixels)
ICON_SPECS = [
    # iPhone
    ('iphone', '2x', 20,  40),
    ('iphone', '3x', 20,  60),
    ('iphone', '2x', 29,  58),
    ('iphone', '3x', 29,  87),
    ('iphone', '2x', 40,  80),
    ('iphone', '3x', 40, 120),
    ('iphone', '2x', 60, 120),
    ('iphone', '3x', 60, 180),
    # iPad
    ('ipad',  '1x', 20,  20),
    ('ipad',  '2x', 20,  40),
    ('ipad',  '1x', 29,  29),
    ('ipad',  '2x', 29,  58),
    ('ipad',  '1x', 40,  40),
    ('ipad',  '2x', 40,  80),
    ('ipad',  '2x', 76, 152),
    ('ipad',  '2x', 83.5, 167),
    # App Store
    ('ios-marketing', '1x', 1024, 1024),
]

def main():
    if not os.path.exists(SOURCE):
        print(f"ERROR: Source image not found: {SOURCE}")
        sys.exit(1)

    img = Image.open(SOURCE).convert('RGBA')
    w, h = img.size
    # Crop to square from center
    size = min(w, h)
    left = (w - size) // 2
    top = (h - size) // 2
    img = img.crop((left, top, left + size, top + size))

    os.makedirs(ASSETS_DIR, exist_ok=True)

    images = []
    for idiom, scale, pt, px in ICON_SPECS:
        filename = f'icon-{idiom}-{pt}x{pt}@{scale}x.png'
        resized = img.resize((px, px), Image.LANCZOS)
        out = os.path.join(ASSETS_DIR, filename)
        resized.save(out, 'PNG')
        print(f'  {filename} ({px}×{px})')

        size_str = f'{pt}x{pt}' if pt == int(pt) else f'{pt}x{pt}'
        images.append({
            'idiom': idiom,
            'scale': scale,
            'size': size_str,
            'filename': filename,
        })

    # Generate Contents.json
    contents = {
        'images': images,
        'info': {
            'version': 1,
            'author': 'xcode',
        },
    }
    contents_path = os.path.join(ASSETS_DIR, 'Contents.json')
    with open(contents_path, 'w') as f:
        json.dump(contents, f, indent=2)
    print(f'  Contents.json')

    print('\nAll iOS icon sizes generated successfully!')

if __name__ == '__main__':
    main()
