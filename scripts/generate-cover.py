"""
Generate elegant ink-wash landscape cover images.
Each cover: 800x1200px, ink-wash landscape + title + author + seal.
Three volumes share a unified layout with distinct themes:
  V1: Seascape, distant sails (靛青 + light gold) — 向世界出發
  V2: Mountains, ancient city (朱砂深紅 + warm gold) — 神州大地之行
  V3: Cloud sea, ridges (松綠 + copper gold) — 中外覽勝錄
  V4: Misty bamboo, pavilion (紫霞 + warm ivory) — 旅遊天地
"""
import json, os, sys, math
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(ROOT, 'dist', 'book')
IMAGES_DIR = os.path.join(BOOK_DIR, 'images')
COVER_W, COVER_H = 800, 1200

# Volume theme data
# (bg_base_rgb, accent_rgb, mountain_rgb, sky_top_rgb, sky_bot_rgb)
VOLUME_THEMES = {
    0: {  # 第一輯 向世界出發 — 靛青 + 淡金，海天意象
        'bg':       (42, 56, 70),
        'accent':   (200, 180, 130),
        'mountain': (58, 78, 90),
        'sky_top':  (78, 100, 120),
        'sky_bot':  (145, 165, 160),
        'water':    (110, 130, 140),
    },
    1: {  # 第二輯 神州大地之行 — 朱砂深紅 + 暖金，山河意象
        'bg':       (60, 28, 22),
        'accent':   (195, 160, 100),
        'mountain': (80, 45, 32),
        'sky_top':  (100, 55, 40),
        'sky_bot':  (175, 130, 95),
        'water':    (130, 90, 70),
    },
    2: {  # 第三輯 中外覽勝錄 — 松綠 + 銅金，雲海意象
        'bg':       (35, 52, 44),
        'accent':   (185, 140, 95),
        'mountain': (48, 68, 55),
        'sky_top':  (65, 88, 75),
        'sky_bot':  (140, 165, 140),
        'water':    (110, 130, 115),
    },
    3: {  # 第四輯 旅遊天地 — 紫霞 + 暖象牙，竹亭意象
        'bg':       (55, 38, 58),
        'accent':   (225, 200, 155),
        'mountain': (72, 52, 72),
        'sky_top':  (90, 60, 92),
        'sky_bot':  (165, 140, 160),
        'water':    (140, 120, 135),
    },
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


def lerp_color(c1, c2, t):
    """Linear interpolate between two RGB tuples."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def blend_alpha(fg_rgb, bg_rgb, alpha):
    """Alpha-blend fg over bg."""
    a = alpha
    return tuple(int(fg_rgb[i] * a + bg_rgb[i] * (1 - a)) for i in range(3))


def draw_sky_gradient(draw, w, h, top_color, bot_color):
    """Draw a soft sky gradient from top to bottom."""
    for y in range(h):
        t = y / h
        c = lerp_color(top_color, bot_color, t * t)
        draw.line([(0, y), (w, y)], fill=c)


def draw_mountains(draw, w, h, mountain_color, accent_color, base_y, count=4):
    """Draw layered mountain silhouettes."""
    import random
    rng = random.Random(42)  # deterministic seed for reproducibility

    for i in range(count):
        alpha = 0.35 + (i / count) * 0.35
        offset_y = base_y + i * 25 - count * 8
        mc = blend_alpha(mountain_color, accent_color, 0.15)

        points = [(0, h)]
        segs = 10
        for x in range(segs + 1):
            px = int(w * x / segs)
            # Generate a smooth mountain ridge
            peak_y = offset_y - rng.randint(40, 140)
            # Cubic bezier-ish: use sine for smooth peaks
            sin_val = math.sin(x / segs * math.pi)
            height_var = rng.randint(30, 120) * sin_val
            py = int(offset_y - height_var)
            points.append((px, py))

        points.append((w, h))

        # Draw filled polygon
        flat = []
        for pt in points:
            flat.extend(pt)
        draw.polygon(flat, fill=mc)


def draw_clouds(draw, w, h, accent_color):
    """Draw horizontal cloud bands in the lower landscape area only."""
    import random
    rng = random.Random(73)

    for i in range(4):
        y_center = int(h * 0.78) + i * 30
        alpha = 0.04 + i * 0.03
        c = blend_alpha(accent_color, (255, 255, 255), 0.6)
        c = blend_alpha(c, (0, 0, 0), 1 - alpha * 6)

        for seg in range(8):
            sx = rng.randint(0, int(w * 0.25))
            ex = sx + rng.randint(100, 350)
            for y_off in range(-8, 9, 2):
                y = max(0, min(h - 1, y_center + y_off))
                draw.line([(sx, y), (min(ex, w), y)], fill=c, width=1)


def draw_water(draw, w, h, water_color, start_y):
    """Draw water/sea reflection area with horizontal ripples."""
    for y in range(start_y, h):
        t = (y - start_y) / (h - start_y)
        c = lerp_color(water_color, tuple(int(x * 0.6) for x in water_color), t)
        draw.line([(0, y), (w, y)], fill=c)

    # Ripple lines
    import random
    rng = random.Random(99)
    for i in range(8):
        y = start_y + rng.randint(15, h - start_y - 30)
        alpha = rng.uniform(0.06, 0.15)
        ripple_c = blend_alpha((220, 210, 190), water_color, alpha)
        for seg in range(5):
            sx = rng.randint(0, int(w * 0.2))
            ex = sx + rng.randint(120, 400)
            y_off = rng.randint(-1, 1)
            draw.line([(sx, y + y_off), (min(ex, w), y + y_off)], fill=ripple_c, width=1)


def draw_sails(draw, w, h, accent_color, start_y, count=3):
    """Draw simple distant sailboat silhouettes (V1 only)."""
    import random
    rng = random.Random(77)
    sail_c = blend_alpha(accent_color, (240, 230, 210), 0.5)

    for i in range(count):
        sx = rng.randint(int(w * 0.15), int(w * 0.8))
        sy = start_y + rng.randint(-10, 15)

        # Mast
        draw.line([(sx, sy - 30), (sx, sy + 8)], fill=sail_c, width=2)

        # Left sail
        draw.polygon([(sx, sy - 28), (sx - 16, sy - 12), (sx, sy - 12)], fill=sail_c)

        # Right sail
        draw.polygon([(sx, sy - 28), (sx + 16, sy - 12), (sx, sy - 12)], fill=sail_c)

        # Hull
        draw.arc([(sx - 12, sy + 4), (sx + 12, sy + 14)], 0, 180, fill=sail_c, width=2)


def draw_great_wall(draw, w, h, accent_color, y_base):
    """Draw a minimal Great Wall silhouette (V2 only)."""
    wall_c = blend_alpha(accent_color, (200, 150, 100), 0.6)
    import random
    rng = random.Random(55)

    points = []
    x = -20
    while x < w + 20:
        y = y_base + rng.randint(-25, 15)
        points.append((int(x), y))
        x += rng.randint(20, 45)
        if rng.random() < 0.35:
            # Watchtower bump
            points.append((int(x - 5), y - rng.randint(10, 20)))

    flat = [(w, h), (0, h)]
    for pt in points:
        flat.insert(0, (pt[0], pt[1] + 6))

    draw.polygon([p for pair in flat for p in pair], fill=wall_c)
    # Ridge line
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=accent_color, width=2)


def draw_pine_branches(draw, w, h, accent_color, y_base):
    """Draw simple pine branch silhouettes at edges (V3 only)."""
    pine_c = blend_alpha(accent_color, (100, 120, 90), 0.55)
    import random
    rng = random.Random(88)

    for side in ['left', 'right']:
        if side == 'left':
            bx, angle = 20, 30
        else:
            bx, angle = w - 20, -30

        for i in range(3):
            py = y_base + rng.randint(-30, 30)
            rad = math.radians(angle)
            ex = bx + rng.randint(40, 80) * math.cos(rad)
            ey = py - rng.randint(40, 80) * math.sin(rad)
            draw.line([(bx, py), (int(ex), int(ey))], fill=pine_c, width=3)
            # Sub-branches
            for j in range(2):
                mx = (bx + ex) / 2 + rng.randint(-10, 10)
                my = (py + ey) / 2 + rng.randint(-10, 10)
                sx = mx + rng.randint(15, 30) * math.cos(rad + math.radians(60))
                sy = my - rng.randint(15, 30) * math.sin(rad + math.radians(60))
                draw.line([(int(mx), int(my)), (int(sx), int(sy))], fill=pine_c, width=1)


def draw_circle_moon(draw, w, accent_color):
    """Draw a faint full moon / sun disk."""
    radius = 65
    cx, cy = int(w * 0.68), 240
    moon_c = blend_alpha(accent_color, (255, 248, 235), 0.7)
    for r in range(radius, radius - 8, -1):
        a = 0.08 + (radius - r) * 0.04
        c = blend_alpha(moon_c, (255, 255, 255), a * 2)
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=c)
    # Soft glow
    for r in range(radius + 5, radius + 40, 3):
        glow_c = (*accent_color,)
        a = max(0.01, (45 - (r - radius)) / 45 * 0.12)
        c = blend_alpha(glow_c, (0, 0, 0), 0)
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=c, width=1)


def draw_bamboo_and_pavilion(draw, w, h, accent_color, y_base):
    """Draw slender bamboo stalks and a distant pavilion silhouette."""
    import random
    rng = random.Random(66)
    bamboo_c = blend_alpha(accent_color, (140, 160, 120), 0.5)
    leaf_c = blend_alpha(accent_color, (160, 180, 140), 0.35)

    # Bamboo stalks on the left
    for i in range(4):
        bx = 40 + i * 35
        stalk_top = y_base - rng.randint(80, 200)
        stalk_bottom = h - rng.randint(20, 60)
        draw.line([(bx, stalk_top), (bx, stalk_bottom)], fill=bamboo_c, width=3 + i % 2)

        # Nodes
        for seg_y in range(stalk_top + 30, stalk_bottom - 10, rng.randint(40, 70)):
            draw.line([(bx - 5, seg_y), (bx + 5, seg_y)], fill=bamboo_c, width=2)

        # Leaves
        for j in range(3):
            lx = bx + rng.randint(-15, 15)
            ly = stalk_top + j * 40 + rng.randint(-10, 10)
            for k in range(2):
                ang = math.radians(rng.randint(20, 60) * (-1 if k == 0 else 1))
                tip_x = lx + rng.randint(20, 40) * math.cos(ang)
                tip_y = ly - rng.randint(20, 40) * math.sin(ang)
                draw.line([(int(lx), ly), (int(tip_x), int(tip_y))], fill=leaf_c, width=1)

    # Distant pavilion on the right
    pav_c = blend_alpha(accent_color, (180, 160, 120), 0.45)
    px = int(w * 0.73)
    py = y_base + 20

    # Base
    draw.rectangle([(px - 22, py + 15), (px + 22, py + 18)], fill=pav_c)
    # Pillars
    for px_off in [-18, 18]:
        draw.line([(px + px_off, py + 15), (px + px_off, py - 30)], fill=pav_c, width=2)
    # Roof: three-tier pagoda roof
    roof_c = blend_alpha(accent_color, (210, 190, 140), 0.6)
    draw.polygon([(px - 32, py - 20), (px, py - 55), (px + 32, py - 20)], fill=roof_c)
    # Upper tier
    draw.polygon([(px - 18, py - 45), (px, py - 70), (px + 18, py - 45)], fill=roof_c)
    # Spire
    draw.line([(px, py - 70), (px, py - 90)], fill=roof_c, width=2)


def draw_birds(draw, w, h, accent_color):
    """Draw a few V-shape birds in the sky."""
    bird_c = blend_alpha(accent_color, (180, 170, 150), 0.6)
    import random
    rng = random.Random(123)

    for i in range(5):
        bx = rng.randint(80, int(w * 0.7))
        by = rng.randint(100, 280)
        size = rng.randint(6, 14)
        pitch = rng.uniform(-15, 15)

        # Simple V bird
        rad = math.radians(pitch)
        lx = bx - size * math.cos(math.radians(20 + pitch))
        ly = by - size * math.sin(math.radians(20 + pitch))
        rx = bx + size * math.cos(math.radians(20 - pitch))
        ry = by - size * math.sin(math.radians(20 - pitch))

        draw.line([(int(lx), int(ly)), (bx, by)], fill=bird_c, width=1)
        draw.line([(rx, ry), (bx, by)], fill=bird_c, width=1)


def draw_seal(draw, w, h, accent_color):
    """Draw a small red seal (朱印) with '雲箋' at the bottom center."""
    seal_size = 50
    sx, sy = w // 2 - seal_size // 2, h - 120
    seal_c = (180, 55, 45)  # Vermillion red

    # Outer border
    draw.rectangle([(sx - 3, sy - 3), (sx + seal_size + 3, sy + seal_size + 3)],
                   outline=seal_c, width=2)

    # Inner characters (approximated)
    seal_font = find_font(20, bold=True)
    draw.text((sx + 3, sy + 2), '雲', font=seal_font, fill=seal_c)
    draw.text((sx + 3, sy + 24), '箋', font=seal_font, fill=seal_c)


def draw_volume_specific(draw, w, h, volume_idx, theme):
    """Draw volume-specific landscape elements in the bottom third."""
    accent = theme['accent']
    mountain = theme['mountain']
    water_c = theme['water']

    # Birds in the sky (upper zone, safe from text)
    draw_birds(draw, w, 680, accent)

    if volume_idx == 0:  # V1: seascape + distant sails + moon
        draw_circle_moon(draw, w, accent)
        draw_mountains(draw, w, 680, mountain, accent, 760, count=3)
        draw_water(draw, w, h, water_c, 840)
        draw_sails(draw, w, h, accent, 850, count=3)

    elif volume_idx == 1:  # V2: mountains + great wall
        draw_mountains(draw, w, 680, mountain, accent, 740, count=5)
        draw_great_wall(draw, w, h, accent, 720)
        draw_water(draw, w, h, water_c, 880)

    elif volume_idx == 2:  # V3: cloud sea + pine
        draw_clouds(draw, w, COVER_H, accent)
        draw_mountains(draw, w, 680, mountain, accent, 760, count=4)
        draw_water(draw, w, h, water_c, 900)
        draw_pine_branches(draw, w, 680, accent, 740)

    elif volume_idx == 3:  # V4: misty bamboo + pavilion silhouette
        draw_clouds(draw, w, COVER_H, accent)
        draw_mountains(draw, w, 680, mountain, accent, 760, count=3)
        draw_water(draw, w, h, water_c, 880)
        draw_bamboo_and_pavilion(draw, w, 680, accent, 780)


def create_cover(title_zh, subtitle_zh, author, output_path, volume_idx):
    """Create an elegant ink-wash landscape cover.
    Layout:
      Upper 62% (0..740): sky gradient + centered title text
      Lower 38% (740..1200): landscape imagery + seal
    """
    theme = VOLUME_THEMES.get(volume_idx, VOLUME_THEMES[0])
    canvas = Image.new('RGB', (COVER_W, COVER_H), theme['bg'])
    draw = ImageDraw.Draw(canvas)

    # --- Sky gradient (upper zone, no landscape here) ---
    sky_bottom = 740
    draw_sky_gradient(draw, COVER_W, sky_bottom, theme['sky_top'], theme['sky_bot'])

    # --- Title text (centered in upper zone) ---
    accent = theme['accent']
    center_x = COVER_W // 2

    # Volume subtitle: "向世界出發" / "神州大地之行" / "中外覽勝錄"
    sub_font = find_font(28)
    sub_w = draw.textbbox((0, 0), subtitle_zh, font=sub_font)[2]
    draw.text(
        ((COVER_W - sub_w) // 2, 200),
        subtitle_zh,
        font=sub_font,
        fill=(*accent, 170),
    )

    # Subtle top decorative line
    draw.rectangle([180, 260, COVER_W - 180, 261], fill=(*accent, 60))

    # Main title: "我的人生旅行"
    title_font = find_font(54, bold=True)
    title_text = '我的人生旅行'
    title_w = draw.textbbox((0, 0), title_text, font=title_font)[2]
    draw.text(
        ((COVER_W - title_w) // 2, 295),
        title_text,
        font=title_font,
        fill=(*accent, 245),
    )

    # Volume label: "第一輯" / "第二輯" / "第三輯"
    vol_label = title_zh.split(' ', 1)[0] if ' ' in title_zh else title_zh
    label_font = find_font(36, bold=True)
    label_w = draw.textbbox((0, 0), vol_label, font=label_font)[2]
    draw.text(
        ((COVER_W - label_w) // 2, 395),
        vol_label,
        font=label_font,
        fill=(*accent, 215),
    )

    # Author
    author_font = find_font(26)
    author_text = author + ' 著'
    au_w = draw.textbbox((0, 0), author_text, font=author_font)[2]
    draw.text(
        ((COVER_W - au_w) // 2, 470),
        author_text,
        font=author_font,
        fill=(*accent, 155),
    )

    # Bottom decorative line before landscape
    draw.rectangle([200, 530, COVER_W - 200, 531], fill=(*accent, 50))

    # --- Landscape imagery (lower zone) ---
    # Darken the lower zone for the landscape to read clearly
    landscape_y = 560
    overlay_start = landscape_y
    for y in range(overlay_start, COVER_H):
        t = (y - overlay_start) / (COVER_H - overlay_start)
        bg = theme['bg']
        # Gradually transition from sky_bot to bg + darker
        transition = lerp_color(theme['sky_bot'], tuple(int(c * 0.55) for c in theme['bg']), min(t * 2.5, 1.0))
        draw.line([(0, y), (COVER_W, y)], fill=transition)

    draw_volume_specific(draw, COVER_W, COVER_H, volume_idx, theme)

    # --- Red seal at bottom ---
    draw_seal(draw, COVER_W, COVER_H, accent)

    canvas.save(output_path, 'JPEG', quality=94)
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

    skipped = 0
    generated = 0
    for idx, chapter in enumerate(chapters):
        title = chapter.get('zh', f'第{idx+1}輯')
        subtitle = title.split(' ', 1)[-1] if ' ' in title else title
        output_path = os.path.join(IMAGES_DIR, f'cover_v{idx + 1}.jpg')

        # Skip if cover already exists and is not a placeholder (has actual content)
        if os.path.exists(output_path):
            try:
                existing = Image.open(output_path)
                existing.verify()
                existing.close()
                print(f'  Cover v{idx + 1} already exists — skipping (preserve custom cover)')
                skipped += 1
                continue
            except Exception:
                pass

        create_cover(title, subtitle, author, output_path, idx)
        print(f'Cover {idx + 1}: {title}')
        generated += 1

    if skipped > 0:
        print(f'Preserved {skipped} existing cover(s), generated {generated} new cover(s).')

    # Update data.json with cover paths (don't overwrite if covers already exist in JSON)
    if 'covers' not in data or not data.get('covers'):
        data['covers'] = {
            f'v{idx+1}': f'images/cover_v{idx+1}.jpg'
            for idx in range(len(chapters))
        }
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('Updated data.json with cover paths.')
    else:
        print('Covers already registered in data.json — skipping.')

    print('Done.')


if __name__ == '__main__':
    main()
