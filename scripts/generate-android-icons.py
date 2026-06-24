"""Generate Android app icons from pre-generated app-icon.png.
Uses simple PNG mipmap approach — deletes ALL adaptive icon XMLs so
Android is forced to use our PNG icons on every version.
"""
import os, sys, shutil
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(PROJECT_ROOT, 'app-icon.png')
ANDROID_BASE = os.path.join(PROJECT_ROOT, 'android', 'app', 'src', 'main', 'res')

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

    # === Purge ALL adaptive icon resources (anydpi XMLs) ===
    # These take priority over our PNG mipmaps and cause icons to not display.
    dirs_to_clean = [
        os.path.join(ANDROID_BASE, 'mipmap-anydpi-v26'),
        os.path.join(ANDROID_BASE, 'drawable-anydpi-v24'),
    ]
    for d in dirs_to_clean:
        if os.path.exists(d):
            for f in os.listdir(d):
                if 'ic_launcher' in f.lower():
                    os.remove(os.path.join(d, f))
                    print(f'  Deleted: {os.path.basename(d)}/{f}')
            # If directory is now empty, remove it
            try:
                os.rmdir(d)
            except OSError:
                pass

    # === Purge foreground PNGs from all density folders ===
    # Capacitor generates ic_launcher_foreground.png in mipmap-* and drawable-*
    for parent in [ANDROID_BASE] + [os.path.join(ANDROID_BASE, d) for d in os.listdir(ANDROID_BASE) if os.path.isdir(os.path.join(ANDROID_BASE, d))]:
        if not os.path.isdir(parent):
            continue
        for f in os.listdir(parent):
            fp = os.path.join(parent, f)
            if os.path.isfile(fp) and 'ic_launcher_foreground' in f.lower():
                os.remove(fp)
                print(f'  Deleted: {os.path.basename(parent)}/{f}')

    # === Purge adaptive background XMLs ===
    bg_files = [
        os.path.join(ANDROID_BASE, 'drawable', 'ic_launcher_background.xml'),
        os.path.join(ANDROID_BASE, 'values', 'ic_launcher_background.xml'),
    ]
    for bf in bg_files:
        if os.path.exists(bf):
            os.remove(bf)
            print(f'  Deleted: {os.path.relpath(bf, ANDROID_BASE)}')

    # === Generate fresh PNG mipmap icons ===
    for dir_name, px in MIPMAP_SIZES.items():
        dir_path = os.path.join(ANDROID_BASE, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        resized = img.resize((px, px), Image.LANCZOS)
        resized.save(os.path.join(dir_path, 'ic_launcher.png'), 'PNG')
        resized.save(os.path.join(dir_path, 'ic_launcher_round.png'), 'PNG')
        print(f'  {dir_name}/ic_launcher.png + ic_launcher_round.png  ({px}x{px})')

    print('\nAll Android icons regenerated (PNG-only, no adaptive XMLs)!')

if __name__ == '__main__':
    main()
