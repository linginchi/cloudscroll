from __future__ import annotations

import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "video" / "cloudscroll-home-art-source.png"
OUT_VIDEO = ROOT / "assets" / "video" / "cloudscroll-home-art-preview.mp4"
OUT_POSTER = ROOT / "assets" / "video" / "cloudscroll-home-art-poster.jpg"
OUT_CONTACT = ROOT / "assets" / "video" / "cloudscroll-home-art-contact.jpg"

WIDTH = 1280
HEIGHT = 720
FPS = 24
DURATION = 14
FRAMES = FPS * DURATION


def ease_loop(t: float) -> float:
    return 0.5 - 0.5 * math.cos(t * math.tau)


def fit_cover(img: Image.Image, scale: float, x_shift: float, y_shift: float) -> Image.Image:
    src_w, src_h = img.size
    base_scale = max(WIDTH / src_w, HEIGHT / src_h)
    final_scale = base_scale * scale
    new_size = (math.ceil(src_w * final_scale), math.ceil(src_h * final_scale))
    resized = img.resize(new_size, Image.Resampling.LANCZOS)

    max_x = max(0, new_size[0] - WIDTH)
    max_y = max(0, new_size[1] - HEIGHT)
    left = int(max_x * 0.5 + x_shift)
    top = int(max_y * 0.45 + y_shift)
    left = max(0, min(max_x, left))
    top = max(0, min(max_y, top))
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def draw_cloud_breath(draw: ImageDraw.ImageDraw, frame: int) -> None:
    drift = (frame / FRAMES) * 80
    alpha_wave = 28 + int(12 * math.sin(frame / FPS * 0.55))
    for i, (y, width, amp) in enumerate([(96, 300, 10), (142, 420, 8), (190, 240, 6)]):
        x0 = 330 + i * 170 + drift * (0.45 + i * 0.08)
        for k in range(4):
            x = (x0 + k * 160) % (WIDTH + 360) - 180
            y2 = y + math.sin(frame / FPS * 0.35 + k) * amp
            draw.arc(
                [x, y2, x + width, y2 + 42],
                start=188,
                end=348,
                fill=(255, 255, 248, max(0, alpha_wave - k * 3)),
                width=2,
            )


def draw_migrating_geese(draw: ImageDraw.ImageDraw, frame: int) -> None:
    t = frame / FRAMES
    x = -120 + t * (WIDTH + 240)
    y = 126 + 18 * math.sin(t * math.tau)
    count = 7
    for i in range(count):
        side = -1 if i % 2 else 1
        step = (i + 1) // 2
        gx = x - step * 34
        gy = y + side * step * 17
        wing = 5 + 2 * math.sin(frame / FPS * 5.0 + i)
        color = (45, 42, 35, 70)
        draw.line([(gx - 9, gy), (gx, gy - wing), (gx + 9, gy)], fill=color, width=2)


def draw_water_shimmer(frame_img: Image.Image, frame: int) -> Image.Image:
    arr = np.array(frame_img).astype(np.int16)
    y0 = int(HEIGHT * 0.70)
    water = arr[y0:, :, :]
    yy = np.arange(water.shape[0])[:, None]
    xx = np.arange(water.shape[1])[None, :]
    wave = (np.sin(xx / 42 + frame / FPS * 1.3) + np.sin(yy / 13 + frame / FPS * 0.8)) * 2.2
    tint = np.zeros_like(water)
    tint[:, :, 2] = np.clip(wave + 1.8, 0, 5)
    tint[:, :, 1] = np.clip(wave * 0.45, 0, 3)
    water = np.clip(water + tint, 0, 255)
    arr[y0:, :, :] = water
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def add_paper_air(img: Image.Image, frame: int) -> Image.Image:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # A slow rice-paper mist layer that keeps the homepage text readable.
    mist_alpha = 14 + int(5 * math.sin(frame / FPS * 0.42))
    draw.rectangle([0, int(HEIGHT * 0.36), WIDTH, HEIGHT], fill=(255, 252, 243, mist_alpha))

    # Very soft edge warmth, like a printed page rather than a screen.
    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    vg = ImageDraw.Draw(vignette)
    for i in range(34):
        a = int(32 * (i / 34) ** 1.7)
        vg.rectangle([i * 3, i * 2, WIDTH - i * 3, HEIGHT - i * 2], outline=a, width=5)
    warm = Image.new("RGBA", (WIDTH, HEIGHT), (250, 244, 230, 18))
    overlay = Image.composite(overlay, warm, vignette)

    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def render_frame(base: Image.Image, frame: int) -> Image.Image:
    t = frame / (FRAMES - 1)
    loop = ease_loop(t)
    scale = 1.035 + 0.018 * loop
    x_shift = -18 + 36 * loop
    y_shift = -8 + 10 * math.sin(t * math.tau)

    img = fit_cover(base, scale, x_shift, y_shift)
    img = ImageEnhance.Color(img).enhance(0.96)
    img = ImageEnhance.Contrast(img).enhance(0.98)
    img = draw_water_shimmer(img, frame)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_cloud_breath(draw, frame)
    draw_migrating_geese(draw, frame)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img = add_paper_air(img, frame)
    return img.filter(ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=4))


def make_contact_sheet(frames: list[Image.Image]) -> None:
    thumb_w = 320
    thumb_h = round(thumb_w * HEIGHT / WIDTH)
    sheet = Image.new("RGB", (thumb_w * len(frames), thumb_h), (250, 246, 238))
    for i, frame in enumerate(frames):
        sheet.paste(frame.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS), (i * thumb_w, 0))
    sheet.save(OUT_CONTACT, quality=92)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    base = Image.open(SOURCE).convert("RGB")
    ffmpeg = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-crf",
        "19",
        str(OUT_VIDEO),
    ]

    contact_frames: list[Image.Image] = []
    poster = None
    with subprocess.Popen(ffmpeg, stdin=subprocess.PIPE) as proc:
        assert proc.stdin is not None
        for frame in range(FRAMES):
            img = render_frame(base, frame)
            if frame == FPS * 3:
                poster = img.copy()
            if frame in [0, FPS * 3, FPS * 6, FPS * 10, FRAMES - 1]:
                contact_frames.append(img.copy())
            proc.stdin.write(img.tobytes())
        proc.stdin.close()
        code = proc.wait()
        if code != 0:
            raise RuntimeError(f"ffmpeg failed with exit code {code}")

    (poster or render_frame(base, 0)).save(OUT_POSTER, quality=92)
    make_contact_sheet(contact_frames)
    print(f"Wrote {OUT_VIDEO}")
    print(f"Wrote {OUT_POSTER}")
    print(f"Wrote {OUT_CONTACT}")


if __name__ == "__main__":
    main()
