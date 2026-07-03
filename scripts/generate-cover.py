"""
Generate simple placeholder cover images.
Each cover: 800x1200px, solid background, title + subtitle + author text only.
No photo collage — the user will replace these with custom covers later.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(ROOT, 'dist', 'book')
IMAGES_DIR = os.path.join(BOOK_DIR, 'images')
COVER_W, COVER_H = 800, 1200

# Volume theme: (bg_color_rgb, title_color_rgb)
VOLUME_THEMES = {
    0: ((26, 42, 58),  (200, 169, 96)),     # deep navy blue + gold
    1: ((74, 21, 21),  (184, 148, 62)),      # chinese red + dark gold
    2: ((26, 47, 31),  (184, 115, 81)),      # dark forest green + copper
}


def find_font(size, bold=False):
    candidates = [
        'C:/Windows/Fonts/msjh.ttc',
        'C:/Windows/Fonts/msyh.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    try:
        return ImageFont.truetype('C:/Windows/Fonts/msjh.ttc', size)
    except Exception:
        return ImageFont.load_default()


def create_simple_cover(title_zh, subtitle_zh, author, output_path, bg_color, accent_color):
    """Create a simple cover with solid background and centered text."""
    canvas = Image.new('RGB', (COVER_W, COVER_H), bg_color)
    draw = ImageDraw.Draw(canvas)

    # Large decorative circle (subtle backdrop)
    circle_color = tuple(min(255, c + 18) for c in bg_color)
    draw.ellipse(
        (COVER_W // 2 - 220, 200, COVER_W // 2 + 220, 640),
        outline=circle_color,
        width=2,
    )
    draw.ellipse(
        (COVER_W // 2 - 235, 185, COVER_W // 2 + 235, 655),
        outline=circle_color,
        width=1,
    )

    title_font = find_font(52, bold=True)
    subtitle_font = find_font(28)
    author_font = find_font(24)

    # Series name
    series_text = subtitle_zh
    ser_bbox = draw.textbbox((0, 0), series_text, font=subtitle_font)
    ser_w = ser_bbox[2] - ser_bbox[0]
    draw.text(
        ((COVER_W - ser_w) // 2, 340),
        series_text,
        font=subtitle_font,
        fill=(*accent_color, 160),
    )

    # Decorative line
    draw.rectangle([160, 410, COVER_W - 160, 412], fill=(*accent_color, 80))

    # Main title
    title_text = f'我的人生旅行'
    title_w = draw.textbbox((0, 0), title_text, font=title_font)[2]
    draw.text(
        ((COVER_W - title_w) // 2, 440),
        title_text,
        font=title_font,
        fill=(*accent_color, 255),
    )

    # Volume number label: extract the volume part before the space
    vol_label = title_zh.split(' ', 1)[0] if ' ' in title_zh else title_zh

    label_font = find_font(36, bold=True)
    label_w = draw.textbbox((0, 0), vol_label, font=label_font)[2]
    draw.text(
        ((COVER_W - label_w) // 2, 520),
        vol_label,
        font=label_font,
        fill=(*accent_color, 220),
    )

    # Decorative line 2
    draw.rectangle([200, 590, COVER_W - 200, 591], fill=(*accent_color, 50))

    # Author
    author_text = author + ' 著'
    au_w = draw.textbbox((0, 0), author_text, font=author_font)[2]
    draw.text(
        ((COVER_W - au_w) // 2, 640),
        author_text,
        font=author_font,
        fill=(*accent_color, 180),
    )

    # Bottom decorative element
    bottom_font = find_font(16)
    bottom_text = '封面待補 · Cover Placeholder'
    bot_w = draw.textbbox((0, 0), bottom_text, font=bottom_font)[2]
    draw.text(
        ((COVER_W - bot_w) // 2, 1100),
        bottom_text,
        font=bottom_font,
        fill=(*accent_color, 60),
    )

    canvas.save(output_path, 'JPEG', quality=92)
    print(f'  Cover saved: {output_path}')


def main():
    data_path = os.path.join(BOOK_DIR, 'data.json')
    if not os.path.exists(data_path):
        print('ERROR: data.json not found. Run extract-book.py first.')
        sys.exit(1)

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    author = data.get('author', '林樺')
    chapters = data.get('chapters', [])

    for idx, chapter in enumerate(chapters):
        title = chapter.get('zh', f'第{idx+1}輯')
        subtitle = title.split(' ', 1)[-1] if ' ' in title else title
        output_path = os.path.join(IMAGES_DIR, f'cover_v{idx + 1}.jpg')
        bg_color, accent_color = VOLUME_THEMES.get(idx, ((30, 35, 50), (200, 180, 160)))
        create_simple_cover(title, subtitle, author, output_path, bg_color, accent_color)
        print(f'Cover {idx + 1}: {title}')

    # Update data.json with cover paths
    data['covers'] = {
        f'v{idx+1}': f'images/cover_v{idx+1}.jpg'
        for idx in range(len(chapters))
    }
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Updated data.json with cover paths.')
    print('Done.')


if __name__ == '__main__':
    main()
