"""
generate_og_image.py — render a 1200x630 social-preview image (og.png) by
designing it as HTML+CSS and screenshotting via Playwright. This gives us
real Korean web fonts (Pretendard + Hahmlet from CDN), CSS gradients,
shadows, and proper kerning that PIL can't match.

Usage: python generate_og_image.py
Writes: ./og.png  (1200x630)

Requires: pip install playwright && playwright install chromium
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "og.png"

OG_HTML = """<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css">
<style>
  :root {
    --bg: #fbfaf6;
    --bg-soft: #f4f1e8;
    --ink: #2a2418;
    --ink-2: #5a5140;
    --ink-3: #8a7f68;
    --teal: #2d7d6e;
    --orange: #d88a3a;
    --rust: #c4593f;
    --purple: #9b7eb7;
    --green: #4a7c59;
    --serif: "Hahmlet", "Pretendard Variable", serif;
    --sans: "Pretendard Variable", "Inter", sans-serif;
    --mono: "JetBrains Mono", monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1200px; height: 630px; overflow: hidden; }
  body {
    font-family: var(--sans);
    color: var(--ink);
    background:
      radial-gradient(ellipse at 90% 10%, rgba(216,138,58,0.18), transparent 50%),
      radial-gradient(ellipse at 10% 90%, rgba(45,125,110,0.12), transparent 50%),
      var(--bg);
    position: relative;
    -webkit-font-smoothing: antialiased;
  }

  /* corner ornament — top right */
  .corner {
    position: absolute;
    top: 36px;
    right: 48px;
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: var(--orange);
    text-transform: uppercase;
  }
  .corner::before { content: "✦  "; color: var(--teal); }

  /* main 60/40 grid */
  .grid {
    display: grid;
    grid-template-columns: 690px 1fr;
    gap: 60px;
    padding: 96px 60px 0 72px;
    height: 100%;
  }

  /* Left text column */
  .left {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  .kicker {
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: var(--ink-3);
    text-transform: uppercase;
    margin-bottom: 20px;
  }
  .kicker .badge {
    background: var(--teal);
    color: #fff;
    padding: 3px 10px;
    border-radius: 3px;
    margin-right: 8px;
  }
  h1 {
    font-family: var(--serif);
    font-weight: 800;
    font-size: 78px;
    line-height: 1.05;
    letter-spacing: -0.025em;
    color: var(--ink);
    margin-bottom: 14px;
  }
  .sub {
    font-family: var(--serif);
    font-weight: 600;
    font-size: 30px;
    line-height: 1.2;
    color: var(--teal);
    margin-bottom: 18px;
    letter-spacing: -0.01em;
  }
  .accent-bar {
    width: 88px;
    height: 4px;
    background: linear-gradient(90deg, var(--teal), var(--orange));
    border-radius: 2px;
    margin-bottom: 26px;
  }
  .deck {
    font-family: var(--sans);
    font-size: 18px;
    font-weight: 400;
    line-height: 1.55;
    color: var(--ink-2);
    max-width: 540px;
    word-break: keep-all;
  }
  .deck strong { color: var(--ink); font-weight: 700; }

  /* stats row */
  .stats {
    display: flex;
    gap: 0;
    margin-top: 38px;
    border-top: 1px solid #d8cfb8;
    border-bottom: 1px solid #d8cfb8;
    padding: 18px 0;
    max-width: 600px;
  }
  .stat {
    flex: 1;
    border-right: 1px dashed #d8cfb8;
    padding: 0 18px;
  }
  .stat:first-child { padding-left: 0; }
  .stat:last-child { border-right: none; }
  .stat .label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-3);
    font-weight: 700;
    margin-bottom: 4px;
  }
  .stat .value {
    font-family: var(--serif);
    font-size: 28px;
    font-weight: 700;
    color: var(--teal);
  }

  /* author row */
  .author {
    position: absolute;
    bottom: 36px;
    left: 72px;
    right: 60px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 13px;
    color: var(--ink-2);
  }
  .author .by-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-3);
    font-weight: 700;
    margin-right: 10px;
  }
  .author .name {
    font-family: var(--serif);
    font-weight: 700;
    font-size: 18px;
    color: var(--ink);
    margin-right: 12px;
  }
  .author .aff {
    font-style: italic;
    color: var(--ink-2);
  }
  .author .url {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--orange);
    font-weight: 500;
  }

  /* Right column — 7-day timeline as visual */
  .right {
    position: relative;
    padding-top: 28px;
  }
  .right-label {
    position: absolute;
    top: 0;
    right: 0;
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: var(--ink-3);
    text-transform: uppercase;
  }
  .right-label::before { content: "↘ "; color: var(--orange); margin-right: 4px; }

  .days {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 50px;
  }
  .day {
    display: grid;
    grid-template-columns: 56px 1fr;
    gap: 14px;
    align-items: center;
    padding: 7px 14px;
    background: #fff;
    border-radius: 10px;
    border: 1px solid rgba(60,45,20,.08);
    box-shadow: 0 4px 14px rgba(60,45,20,.04);
  }
  .day .num {
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #fff;
    background: var(--teal);
    padding: 6px 10px;
    border-radius: 6px;
    text-align: center;
  }
  .day:nth-child(2) .num { background: var(--orange); }
  .day:nth-child(3) .num { background: var(--purple); }
  .day:nth-child(4) .num { background: var(--ink); }
  .day:nth-child(5) .num { background: var(--green); }
  .day:nth-child(6) .num { background: var(--rust); }
  .day:nth-child(7) .num { background: #e8a770; }
  .day .name {
    font-family: var(--serif);
    font-size: 18px;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.01em;
  }
  .day .name .desc {
    font-family: var(--sans);
    font-size: 12px;
    font-weight: 400;
    color: var(--ink-3);
    margin-left: 8px;
  }
</style>
</head>
<body>

<div class="corner">VOL.01 · 2026 SPRING</div>

<div class="grid">
  <div class="left">
    <div class="kicker"><span class="badge">FIELD GUIDE</span>OBSIDIAN × CLAUDE CODE</div>
    <h1>연구보조 시스템</h1>
    <div class="sub">박사·연구자용 7일 셋업</div>
    <div class="accent-bar"></div>
    <div class="deck">매일 1-2시간씩 일주일이면 본인 vault에 작동하는 시스템 셋업. <strong>로컬 우선</strong>, <strong>월 비용 $1-2</strong>, <strong>BYOK</strong>. 차근차근 그림과 함께.</div>

    <div class="stats">
      <div class="stat"><div class="label">총 단계</div><div class="value">7일</div></div>
      <div class="stat"><div class="label">일일</div><div class="value">1-2h</div></div>
      <div class="stat"><div class="label">월 비용</div><div class="value">$1-2</div></div>
      <div class="stat"><div class="label">형태</div><div class="value">로컬</div></div>
    </div>
  </div>

  <div class="right">
    <div class="right-label">JOURNEY</div>
    <div class="days">
      <div class="day"><div class="num">D1</div><div class="name">Vault<span class="desc">첫 entity</span></div></div>
      <div class="day"><div class="num">D2</div><div class="name">Today.md<span class="desc">진입점</span></div></div>
      <div class="day"><div class="num">D3</div><div class="name">Hook<span class="desc">자동 기록</span></div></div>
      <div class="day"><div class="num">D4</div><div class="name">Tracker<span class="desc">매 2시간</span></div></div>
      <div class="day"><div class="num">D5</div><div class="name">Ontology<span class="desc">지식 그래프</span></div></div>
      <div class="day"><div class="num">D6</div><div class="name">Watcher<span class="desc">변화 감지</span></div></div>
      <div class="day"><div class="num">D7</div><div class="name">/slides<span class="desc">발표자료</span></div></div>
    </div>
  </div>
</div>

<div class="author">
  <div>
    <span class="by-label">BY</span>
    <span class="name">문제웅</span>
    <span class="aff">The University of Alabama · jmoon19@ua.edu</span>
  </div>
  <div class="url">educatian.github.io/research-assistant-ai-workflow-ko</div>
</div>

</body></html>
"""


def main() -> None:
    from playwright.sync_api import sync_playwright
    template = HERE / ".og_template.html"
    template.write_text(OG_HTML, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # device_scale_factor=1 keeps file size reasonable; 1200x630 is already
        # the max recommended OG dimension. Web fonts at 1x still look crisp.
        ctx = browser.new_context(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(template.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(1200)  # web fonts settle
        # JPG with 88% quality is the OG sweet spot — Facebook/LinkedIn/Twitter
        # all support JPG and it's ~5x smaller than equivalent PNG for this content.
        jpg_out = OUT.with_suffix(".jpg")
        page.screenshot(path=str(jpg_out), type="jpeg", quality=90,
                        clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()
    # Also produce a PNG (in case someone wants lossless) but keep JPG as primary
    try:
        from PIL import Image
        Image.open(jpg_out).save(OUT, "PNG", optimize=True)
    except Exception:
        pass
    template.unlink(missing_ok=True)
    print(f"[done] {jpg_out}  ({jpg_out.stat().st_size // 1024} KB)")
    if OUT.exists():
        print(f"[done] {OUT}    ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
