# -*- coding: utf-8 -*-
"""
Generate a Cloudscroll homepage preview video.

This produces an original, generated scene rather than using copyrighted film
footage: autumn sky, cirrus clouds, geese, modern city, forest, and distant
mountains. The output is for review only and is not wired into index.html.
"""

import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "video"
OUT_MP4 = OUT_DIR / "cloudscroll-home-preview.mp4"
OUT_POSTER = OUT_DIR / "cloudscroll-home-preview-poster.jpg"

WIDTH = 1280
HEIGHT = 720
FPS = 24
DURATION = 14
FRAMES = FPS * DURATION


def lerp(a, b, t):
    return a + (b - a) * t


def ease(t):
    return t * t * (3 - 2 * t)


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def color_lerp(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def draw_gradient(draw, top, bottom):
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        draw.line([(0, y), (WIDTH, y)], fill=color_lerp(top, bottom, t))


def polygon_wave(base_y, amp, points, phase=0):
    coords = []
    for i in range(points + 1):
        x = WIDTH * i / points
        n = (
            math.sin(i * 1.37 + phase) * 0.55
            + math.sin(i * 2.61 + phase * 0.7) * 0.35
            + math.sin(i * 4.23 + 1.7) * 0.18
        )
        y = base_y + n * amp
        coords.append((x, y))
    return [(0, HEIGHT), *coords, (WIDTH, HEIGHT)]


def draw_cirrus(layer, x, y, scale, opacity, drift):
    d = ImageDraw.Draw(layer, "RGBA")
    for k in range(9):
        yy = y + math.sin(k * 0.9) * 8 * scale
        xx = x + k * 74 * scale + drift
        width = 170 * scale * (1 - k * 0.035)
        col = (255, 255, 255, int(opacity * (0.52 - k * 0.025)))
        d.arc(
            [xx - width, yy - 18 * scale, xx + width, yy + 22 * scale],
            start=184,
            end=356,
            fill=col,
            width=max(1, int(2 * scale)),
        )


def draw_goose(draw, x, y, s, alpha):
    col = (54, 67, 63, alpha)
    w = max(1, int(2 * s))
    draw.line([(x, y), (x - 9 * s, y - 5 * s)], fill=col, width=w)
    draw.line([(x, y), (x + 9 * s, y - 5 * s)], fill=col, width=w)


def draw_city(draw, y_base, reveal, haze):
    # Quiet modern skyline tucked to the left. It recedes into the distance
    # instead of spanning the whole frame, leaving the right side to forest.
    rng = np.random.default_rng(7)
    x = 48
    max_x = WIDTH * 0.34
    while x < max_x:
        recede = 1 - (x / max_x) * 0.45
        bw = int(rng.integers(20, 52) * recede)
        bh = int(rng.integers(82, 205) * reveal * recede)
        top = y_base - bh
        body = (56, 72, 78, int(130 * reveal * haze * recede))
        edge = (218, 228, 224, int(38 * reveal * haze * recede))
        draw.rectangle([x, top, x + bw, y_base], fill=body)
        if bw > 36:
            draw.line([(x + bw * 0.72, top + 12), (x + bw * 0.72, y_base)], fill=edge, width=1)
        for wy in range(int(top + 18), int(y_base - 8), 26):
            draw.line([(x + 7, wy), (x + bw - 8, wy)], fill=(230, 236, 228, int(20 * reveal)), width=1)
        x += bw + int(rng.integers(8, 22))


def draw_forest_depth(draw, base_y, camera):
    # Near forest occupies most of the frame, with three tonal bands to create
    # a clear city/forest/mountain depth relationship.
    rng = np.random.default_rng(12)

    # Back tree line: soft, pale, sits behind city and blends with mountain mist.
    for i in range(56):
        x = -40 + i * 28 + math.sin(i) * 3
        h = 30 + 14 * math.sin(i * 1.23 + 0.4)
        col = (83, 124, 98, 70)
        draw.polygon([(x, base_y - 46), (x + 14, base_y - 46 - h), (x + 30, base_y - 46)], fill=col)

    # Middle forest: more visible, covers the right two-thirds.
    start_x = WIDTH * 0.25
    for i in range(48):
        x = start_x - 20 + i * 26
        h = 48 + 26 * (0.5 + 0.5 * math.sin(i * 1.75))
        col = (42, 91, 67, 125)
        draw.polygon([(x, base_y), (x + 13, base_y - h), (x + 28, base_y)], fill=col)

    # Near foreground forest: darker and denser, mainly on the lower right.
    for i in range(42):
        x = WIDTH * 0.35 + i * 27
        h = 68 + 38 * rng.random()
        col = (22, 62, 43, 178)
        draw.polygon([(x, HEIGHT), (x + 15, HEIGHT - h), (x + 34, HEIGHT)], fill=col)

    # A low shadow mass gives the forest a quiet, grounded base.
    draw.polygon(
        [
            (WIDTH * 0.18, HEIGHT),
            (WIDTH * 0.36, HEIGHT - 78),
            (WIDTH * 0.56, HEIGHT - 112),
            (WIDTH * 0.78, HEIGHT - 86),
            (WIDTH, HEIGHT - 118),
            (WIDTH, HEIGHT),
        ],
        fill=(18, 56, 39, 135),
    )


def render_frame(frame):
    p = frame / (FRAMES - 1)
    camera = ease(clamp((p - 0.08) / 0.72))

    img = Image.new("RGB", (WIDTH, HEIGHT), (236, 241, 238))
    draw = ImageDraw.Draw(img, "RGBA")

    sky_top = color_lerp((42, 114, 178), (71, 139, 192), 0.35)
    sky_bottom = color_lerp((215, 229, 224), (184, 205, 192), camera * 0.55)
    draw_gradient(draw, sky_top, sky_bottom)

    # Gentle autumn sunlight.
    sun = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun, "RGBA")
    sx, sy = WIDTH * 0.75, HEIGHT * 0.18
    for r, a in [(180, 22), (120, 28), (66, 50), (38, 86)]:
        sd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(246, 226, 174, a))
    img = Image.alpha_composite(img.convert("RGBA"), sun)
    draw = ImageDraw.Draw(img, "RGBA")

    cloud_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    drift = p * 95
    draw_cirrus(cloud_layer, 70, 82, 1.0, 82, drift)
    draw_cirrus(cloud_layer, 555, 118, 0.72, 68, drift * 0.55)
    draw_cirrus(cloud_layer, 850, 70, 0.85, 55, -drift * 0.35)
    cloud_layer = cloud_layer.filter(ImageFilter.GaussianBlur(0.45))
    img = Image.alpha_composite(img, cloud_layer)
    draw = ImageDraw.Draw(img, "RGBA")

    # Geese appear in the opening and slowly leave the frame.
    goose_alpha = int(220 * (1 - clamp((p - 0.36) / 0.25)))
    if goose_alpha > 0:
        gx = lerp(-120, WIDTH * 0.72, ease(clamp(p / 0.42)))
        gy = lerp(138, 82, ease(clamp(p / 0.42)))
        offsets = [(0, 0, 1.0), (-34, 15, 0.78), (34, 15, 0.78), (-67, 31, 0.62), (67, 31, 0.62)]
        for ox, oy, ss in offsets:
            draw_goose(draw, gx + ox, gy + oy, 1.45 * ss, goose_alpha)

    # Distant mountains: three layers, with the deepest layer spanning the
    # horizon and stronger contrast in the foreground for depth.
    m_shift = lerp(70, 0, camera)
    far = polygon_wave(356 + m_shift, 48, 15, phase=0.6)
    mid = polygon_wave(422 + m_shift * 0.66, 70, 15, phase=2.1)
    near = polygon_wave(500 + m_shift * 0.32, 58, 18, phase=3.0)
    draw.polygon(far, fill=(128, 156, 143, 100))
    draw.polygon(mid, fill=(78, 119, 102, 145))
    draw.polygon(near, fill=(36, 78, 61, 188))

    # City is visible but quiet, softened by mist and limited to the left.
    city_reveal = ease(clamp((p - 0.18) / 0.35))
    mist = 1 - 0.25 * camera
    draw_city(draw, int(565 + m_shift * 0.25), city_reveal, mist)

    # Forest owns the foreground and right two-thirds.
    draw_forest_depth(draw, 610, camera)

    # Low mist and ink-wash water/ground surface.
    mist_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    md = ImageDraw.Draw(mist_layer, "RGBA")
    for y in range(455, HEIGHT):
        t = (y - 455) / (HEIGHT - 455)
        md.line([(0, y), (WIDTH, y)], fill=(235, 240, 229, int(72 * (1 - abs(t - 0.34)))))
    for k in range(11):
        yy = 625 + k * 10 + math.sin(p * math.tau + k) * 2
        md.line(
            [(80 + k * 16, yy), (WIDTH - 160 - k * 8, yy + math.sin(k) * 3)],
            fill=(215, 226, 217, 32),
            width=1,
        )
    img = Image.alpha_composite(img, mist_layer)

    # Paper/film tone.
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (247, 241, 226, 18))
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="cloudscroll-video-"))
    try:
        for frame in range(FRAMES):
            img = render_frame(frame)
            img.save(tmp / f"frame_{frame:04d}.jpg", quality=92)
            if frame == int(FRAMES * 0.68):
                img.save(OUT_POSTER, quality=92)

        cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(tmp / "frame_%04d.jpg"),
            "-vf",
            "format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "19",
            "-movflags",
            "+faststart",
            str(OUT_MP4),
        ]
        subprocess.run(cmd, check=True)
        print(f"Wrote {OUT_MP4}")
        print(f"Wrote {OUT_POSTER}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
