"""
Generate all icon sizes from APP_icon.jpg.
Source: src/images/APP_icon.jpg
Output:
  - dist/favicon.ico               (16/32/48 multi-size)
  - dist/apple-touch-icon.png      (180x180)
  - dist/icon-192.png              (192x192, PWA)
  - dist/icon-512.png              (512x512, PWA)
  - dist/og-image.png              (1200x630, Open Graph / WeChat)
"""
import os, sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_APP_ICON = os.path.join(ROOT, 'src', 'images', 'APP_icon.jpg')
DIST_DIR = os.path.join(ROOT, 'dist')


def resize_to_square(img, size):
    """Resize image to a square of `size`x`size`, cropped from center."""
    # Crop to square first
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    img = img.crop((left, top, left + s, top + s))
    return img.resize((size, size), Image.LANCZOS)


def generate_icons():
    if not os.path.exists(SRC_APP_ICON):
        print(f'ERROR: APP_icon.jpg not found at {SRC_APP_ICON}')
        sys.exit(1)

    print('Generating icons from APP_icon.jpg...\n')
    os.makedirs(DIST_DIR, exist_ok=True)

    src = Image.open(SRC_APP_ICON).convert('RGBA')
    print(f'  Source: {src.size[0]}x{src.size[1]}')

    # 1. favicon.ico (16, 32, 48)
    icons = []
    for s in [16, 32, 48]:
        icons.append(resize_to_square(src, s))
    ico_path = os.path.join(DIST_DIR, 'favicon.ico')
    icons[0].save(ico_path, format='ICO', sizes=[(s, s) for s in [16, 32, 48]])
    print('  Generated favicon.ico (16/32/48)')

    # 2. Apple touch icon (180x180)
    apple = resize_to_square(src, 180)
    apple.save(os.path.join(DIST_DIR, 'apple-touch-icon.png'), 'PNG')
    print('  Generated apple-touch-icon.png (180x180)')

    # 3. PWA icons
    for s in [192, 512]:
        icon = resize_to_square(src, s)
        icon.save(os.path.join(DIST_DIR, f'icon-{s}.png'), 'PNG')
        print(f'  Generated icon-{s}.png ({s}x{s})')

    # 4. OG image (1200x630) — letterboxed from app icon
    og = Image.new('RGBA', (1200, 630), (245, 240, 230, 255))
    # Fit the icon into the OG image maintaining aspect ratio
    icon_fit = src.copy()
    icon_fit.thumbnail((400, 400), Image.LANCZOS)
    iw, ih = icon_fit.size
    # Center it
    og.paste(icon_fit, ((1200 - iw) // 2, (630 - ih) // 2), icon_fit if icon_fit.mode == 'RGBA' else None)
    og = og.convert('RGB')
    og.save(os.path.join(DIST_DIR, 'og-image.png'), 'PNG', quality=92)
    print('  Generated og-image.png (1200x630)')

    # Also place a copy of the source as favicon.png for fallback
    fav_png = resize_to_square(src, 192)
    fav_png.save(os.path.join(DIST_DIR, 'favicon.png'), 'PNG')
    print('  Generated favicon.png (192x192)')

    print('\nDone. All icons generated from APP_icon.jpg.')


if __name__ == '__main__':
    generate_icons()
