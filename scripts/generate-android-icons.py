"""Generate Android app icon sizes from source image for Capacitor project."""
import os
import sys
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(PROJECT_ROOT, 'back-yushi.png')
ANDROID_BASE = os.path.join(PROJECT_ROOT, 'android', 'app', 'src', 'main', 'res')

# Android density buckets → required pixel sizes for launcher icons
MIPMAP_SIZES = {
    'mipmap-mdpi':    48,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}

# Adaptive icon foreground (108dp) per density: ratio = target_dpi / 160
# 108dp × (density / 160)
FOREGROUND_SIZES = {
    'drawable-mdpi':    108,   # 108dp @ 160dpi → 108px
    'drawable-hdpi':    162,   # 108dp @ 240dpi → 162px
    'drawable-xhdpi':   216,   # 108dp @ 320dpi → 216px
    'drawable-xxhdpi':  324,   # 108dp @ 480dpi → 324px
    'drawable-xxxhdpi': 432,   # 108dp @ 640dpi → 432px
}

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

    # Generate regular launcher icons (mipmap)
    for dir_name, px in MIPMAP_SIZES.items():
        dir_path = os.path.join(ANDROID_BASE, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        resized = img.resize((px, px), Image.LANCZOS)
        out = os.path.join(dir_path, 'ic_launcher.png')
        resized.save(out, 'PNG')
        print(f'  {dir_name}/ic_launcher.png  ({px}×{px})')

    # Generate adaptive foreground (with padding for safe zone; 66.67% of the 108dp viewport)
    # The inner content should be within the center 66.67% so nothing gets clipped
    # We use the full image scaled, which will be masked by the adaptive icon XML
    for dir_name, px in FOREGROUND_SIZES.items():
        dir_path = os.path.join(ANDROID_BASE, dir_name)
        os.makedirs(dir_path, exist_ok=True)

        # Add 33% padding so content is within safe zone of adaptive icon
        pad = int(px * 0.1667)  # ~16.67% on each side → 33.34% total
        canvas = Image.new('RGBA', (px, px), (0, 0, 0, 0))
        inner_size = px - 2 * pad
        resized = img.resize((inner_size, inner_size), Image.LANCZOS)
        canvas.paste(resized, (pad, pad))
        out = os.path.join(dir_path, 'ic_launcher_foreground.png')
        canvas.save(out, 'PNG')
        print(f'  {dir_name}/ic_launcher_foreground.png  ({px}×{px})')

    # Generate round icon (mipmap)
    for dir_name, px in MIPMAP_SIZES.items():
        dir_path = os.path.join(ANDROID_BASE, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        resized = img.resize((px, px), Image.LANCZOS)
        out = os.path.join(dir_path, 'ic_launcher_round.png')
        resized.save(out, 'PNG')
        print(f'  {dir_name}/ic_launcher_round.png  ({px}×{px})')

    # Create adaptive icon XMLs
    anydpi_dir = os.path.join(ANDROID_BASE, 'mipmap-anydpi-v26')
    os.makedirs(anydpi_dir, exist_ok=True)

    ic_launcher_xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>'''

    with open(os.path.join(anydpi_dir, 'ic_launcher.xml'), 'w') as f:
        f.write(ic_launcher_xml)
    print(f'  mipmap-anydpi-v26/ic_launcher.xml')

    # Also create round variant for launchers that prefer it
    with open(os.path.join(anydpi_dir, 'ic_launcher_round.xml'), 'w') as f:
        f.write(ic_launcher_xml)
    print(f'  mipmap-anydpi-v26/ic_launcher_round.xml')

    # Always create/overwrite background color (even if Capacitor didn't create it)
    values_dir = os.path.join(ANDROID_BASE, 'values')
    os.makedirs(values_dir, exist_ok=True)
    bg_file = os.path.join(values_dir, 'ic_launcher_background.xml')
    bg_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#8B1A1A</color>
</resources>'''
    with open(bg_file, 'w') as f:
        f.write(bg_xml)
    print(f'  values/ic_launcher_background.xml (#8B1A1A)')

    print('\nAll Android icon sizes generated successfully!')

if __name__ == '__main__':
    main()
