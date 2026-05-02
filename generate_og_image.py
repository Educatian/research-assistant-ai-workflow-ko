"""
generate_og_image.py — generate the 1200x630 social-preview image (og.png)
that Facebook, Discord, Twitter/X, and LinkedIn use as the link thumbnail.

Style: course-module aesthetic (warm cream paper, teal accent, Hahmlet-like
display, mono kicker). No external assets — pure PIL drawing.

Usage: python generate_og_image.py
Writes: ./og.png  (1200x630, ~80-150KB)
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "og.png"

W, H = 1200, 630

# Course-module palette
BG = "#fbfaf6"
BG_SOFT = "#f4f1e8"
INK = "#2a2418"
INK_2 = "#5a5140"
INK_3 = "#8a7f68"
ACCENT = "#2d7d6e"
ACCENT_2 = "#d88a3a"
ACCENT_3 = "#c4593f"


def find_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    """Try candidate font paths/names; fall back to default on failure."""
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Right halo (subtle)
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse((W - 500, -200, W + 200, 500), fill=(216, 138, 58, 28))
    img.paste(halo, (0, 0), halo)

    # Korean serif candidates (Hahmlet not bundled, fall back gracefully)
    serif_l = find_font([
        "C:/Windows/Fonts/malgunbd.ttf",      # Malgun Gothic Bold
        "C:/Windows/Fonts/batang.ttc",        # Batang
        "C:/Windows/Fonts/seguisb.ttf",       # Segoe UI Semibold
        "DejaVuSans-Bold.ttf",
    ], 92)
    serif_m = find_font([
        "C:/Windows/Fonts/malgunbd.ttf",
        "C:/Windows/Fonts/batang.ttc",
        "C:/Windows/Fonts/seguisb.ttf",
        "DejaVuSans-Bold.ttf",
    ], 56)
    sans_m = find_font([
        "C:/Windows/Fonts/malgun.ttf",        # Malgun Gothic Regular
        "C:/Windows/Fonts/segoeui.ttf",
        "DejaVuSans.ttf",
    ], 28)
    mono_s = find_font([
        "C:/Windows/Fonts/consolab.ttf",      # Consolas Bold
        "C:/Windows/Fonts/cour.ttf",
        "DejaVuSansMono-Bold.ttf",
    ], 22)
    mono_xs = find_font([
        "C:/Windows/Fonts/consolab.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "DejaVuSansMono-Bold.ttf",
    ], 18)
    sans_s = find_font([
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "DejaVuSans.ttf",
    ], 22)

    # Top kicker
    d.text((72, 64), "✦  VOL.01  ·  BEGINNER FIELD GUIDE  ·  2026 SPRING",
           fill=ACCENT_2, font=mono_xs)

    # Title (two lines, Korean)
    d.text((72, 140), "연구보조 시스템", fill=INK, font=serif_l)
    d.text((72, 244), "초심자 7-day 가이드", fill=INK, font=serif_l)

    # Underline accent
    d.rectangle((72, 358, 200, 364), fill=ACCENT)

    # Subtitle (1 line)
    d.text((72, 384),
           "Obsidian × Claude Code · 박사·연구자용 셋업",
           fill=INK_2, font=serif_m)

    # Stats row (4 columns)
    stats_y = 472
    stats = [
        ("총 단계", "7일"),
        ("일일", "1-2시간"),
        ("월 비용", "$1-2"),
        ("형태", "로컬 우선"),
    ]
    col_w = 220
    col_x = 72
    for i, (label, value) in enumerate(stats):
        x = col_x + i * col_w
        d.text((x, stats_y), label, fill=INK_3, font=mono_xs)
        d.text((x, stats_y + 30), value, fill=ACCENT, font=serif_m)

    # Bottom left: author byline
    d.line((72, 592, 1128, 592), fill="#d0c8b3", width=1)
    d.text((72, 580 - 12 + 30),
           "by  문제웅  ·  The University of Alabama  ·  jmoon19@ua.edu",
           fill=INK_2, font=sans_s)

    # Bottom right: URL
    url = "educatian.github.io/research-assistant-ai-workflow-ko"
    bbox = d.textbbox((0, 0), url, font=mono_xs)
    url_w = bbox[2] - bbox[0]
    d.text((W - 72 - url_w, 580 - 12 + 32), url,
           fill=ACCENT_2, font=mono_xs)

    # Right side: 7 day milestones (mini timeline)
    icon_y = 160
    icon_x_start = 760
    icon_spacing = 50
    milestones = [
        ("D1", "Vault", ACCENT),
        ("D2", "Today", ACCENT_2),
        ("D3", "Hook", "#9b7eb7"),
        ("D4", "Track", ACCENT_2),
        ("D5", "Onto", "#4a7c59"),
        ("D6", "LLM",  ACCENT_3),
        ("D7", "PT",   "#e8a770"),
    ]
    for i, (lbl, name, color) in enumerate(milestones):
        x = icon_x_start
        y = icon_y + i * icon_spacing
        d.ellipse((x, y, x + 26, y + 26), fill=BG, outline=color, width=2)
        d.text((x + 32, y - 2), lbl, fill=INK_3, font=mono_xs)
        d.text((x + 78, y - 2), name, fill=INK, font=sans_s)

    # Top-right corner mark
    mark_x, mark_y = W - 100, 64
    d.text((mark_x, mark_y), "GUIDE", fill=ACCENT, font=mono_s)

    img.save(OUT, "PNG", optimize=True)
    print(f"[done] {OUT}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
