"""Generate Android app icons from pre-generated app-icon.png.
Simple PNG-only approach — no adaptive icons (most reliable across all Android versions).
"""
import os, sys, shutil
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(PROJECT_ROOT, 'app-icon.png')
ANDROID_BASE = os.path.join(PROJECT_ROOT, 'android', 'app', 'src', 'main', 'res')

# Android launcher icon sizes per density bucket
MIPMAP_SIZES = {
    'mipmap-mdpi':    48,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}

def main():
    if not os.path.exists(SOURCE):
        print(f"ERROR: Source image not found: {SOURCE}")
        sys.exit(1)

    img = Image.open(SOURCE).convert('RGBA')

    # --- 1. Delete anydpi adaptive icon folder ---
    anydpi_dir = os.path.join(ANDROID_BASE, 'mipmap-anydpi-v26')
    if os.path.exists(anydpi_dir):
        shutil.rmtree(anydpi_dir)
        print(f'  Deleted mipmap-anydpi-v26/ (using PNG icons only)')

    # --- 2. Generate standard launcher icons (mipmap) ---
    for dir_name, px in MIPMAP_SIZES.items():
        dir_path = os.path.join(ANDROID_BASE, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        resized = img.resize((px, px), Image.LANCZOS)
        resized.save(os.path.join(dir_path, 'ic_launcher.png'), 'PNG')
        resized.save(os.path.join(dir_path, 'ic_launcher_round.png'), 'PNG')
        print(f'  {dir_name}/ic_launcher.png + ic_launcher_round.png  ({px}x{px})')

    # --- 3. Clean up foreground drawables from previous builds ---
    for d in os.listdir(ANDROID_BASE):
        if d.startswith('drawable-'):
            fg = os.path.join(ANDROID_BASE, d, 'ic_launcher_foreground.png')
            if os.path.exists(fg):
                os.remove(fg)
                print(f'  Removed stale: {d}/ic_launcher_foreground.png')

    # --- 4. Ensure background color exists (for any leftover adaptive refs) ---
    values_dir = os.path.join(ANDROID_BASE, 'values')
    os.makedirs(values_dir, exist_ok=True)
    bg_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#8B1A1A</color>
</resources>'''
    bg_file = os.path.join(values_dir, 'ic_launcher_background.xml')
    with open(bg_file, 'w') as f:
        f.write(bg_xml)
    print(f'  values/ic_launcher_background.xml (#8B1A1A)')

    print('\nAll Android icons generated (PNG-only, no adaptive icons)!')

if __name__ == '__main__':
    main()
